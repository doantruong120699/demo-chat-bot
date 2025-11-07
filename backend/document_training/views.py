from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.http import StreamingHttpResponse
import uuid
import json
import traceback
import logging

from .models import Document, ChatHistory, ChatSession, DocumentChunk
from .serializers import (
    DocumentSerializer,
    ChatRequestSerializer,
    ChatHistorySerializer,
    ChatSessionSerializer,
    ChatSessionDetailSerializer,
    ChatWithFileSerializer,
)
from .services.chat_service import DocumentChatService
from .services.embedding_service import DocumentEmbeddingService
from .services.pdf_extractor import PDFExtractor

logger = logging.getLogger(__name__)


class DocumentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing documents"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = DocumentSerializer
    
    def get_queryset(self):
        """Filter documents by user"""
        return Document.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Save document and automatically chunk + embed"""
        logger.info(f"=" * 60)
        logger.info(f"📄 Creating new document")
        
        # Save document
        document = serializer.save(user=self.request.user)
        logger.info(f"✅ Document saved: {document.title} (ID: {document.id})")
        
        # Process document: chunk and create embeddings
        try:
            embedding_service = DocumentEmbeddingService()
            processed_chunks = embedding_service.process_document(document.content)
            
            # Save chunks to database
            chunks_to_create = []
            for chunk_data in processed_chunks:
                chunks_to_create.append(
                    DocumentChunk(
                        document=document,
                        content=chunk_data['content'],
                        chunk_index=chunk_data['chunk_index'],
                        embedding=chunk_data['embedding'],
                        token_count=chunk_data['token_count']
                    )
                )
            
            # Bulk create for efficiency
            DocumentChunk.objects.bulk_create(chunks_to_create)
            logger.info(f"✅ Saved {len(chunks_to_create)} chunks to database")
            logger.info(f"=" * 60)
            
        except Exception as e:
            logger.error(f"❌ Failed to process document chunks: {str(e)}")
            logger.error(traceback.format_exc())
            # Document is still saved, just without chunks


class DocumentChatView(viewsets.ViewSet):
    """ViewSet for document Q&A chat"""
    
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]  # Support both JSON and file upload
    
    @action(detail=False, methods=['post'], url_path='chat')
    def chat(self, request):
        """
        Single chat endpoint - handles 3 cases:
        1. With document_id: use existing document from DB
        2. With file_content: use file content directly (temporary, not saved)
        3. Without both: general chat
        """
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        document_id = data.get('document_id')
        file_content = data.get('file_content')
        file_name = data.get('file_name')
        user_message = data['message']
        chat_history = data.get('chat_history', [])
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        # 🔍 LOG: Check what was sent from FE
        logger.info(f"=" * 60)
        logger.info(f"📨 Chat request received:")
        logger.info(f"  - user_message: {user_message[:100]}")
        logger.info(f"  - document_id: {document_id}")
        logger.info(f"  - file_name: {file_name}")
        logger.info(f"  - file_content length: {len(file_content) if file_content else 0} chars")
        if file_content:
            logger.info(f"  - file_content preview: {file_content[:200]}...")
        logger.info(f"  - session_id: {session_id}")
        logger.info(f"=" * 60)
        
        document = None
        document_content = None
        
        # Get or create ChatSession
        session, created = ChatSession.objects.get_or_create(
            session_id=session_id,
            user=request.user,
            defaults={
                'document_id': document_id,
            }
        )
        
        # 🔍 LOG: Session info
        logger.info(f"📋 Session info:")
        logger.info(f"   Created new: {created}")
        logger.info(f"   Session has document: {session.document_id}")
        logger.info(f"   Session has content: {bool(session.document_content)}")
        
        # Priority: document_id > file_content > session's document > none
        if document_id:
            # Case 1: Use existing document from DB
            try:
                document = Document.objects.get(id=document_id, user=request.user)
                
                # If session was just created, snapshot the document content
                if created:
                    session.document = document
                    session.document_title = document.title
                    session.document_content = document.content
                    session.language = document.language
                    session.title = user_message[:50] + ('...' if len(user_message) > 50 else '')
                    session.save()
                    logger.info(f"Session {session_id} created with document: {document.title}")
                
                # Use snapshot content from session (immutable)
                document_content = session.document_content
                document = session.document
                
            except Document.DoesNotExist:
                return Response(
                    {'error': 'Document not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        elif file_content:
            # Case 2: Use file content directly (not saved to DB)
            document_content = file_content
            
            # 🔍 LOG: File content is being used
            logger.info(f"✅ Using file_content from payload")
            logger.info(f"   File: {file_name or 'unnamed'}")
            logger.info(f"   Content length: {len(file_content)} chars")
            logger.info(f"   Content preview: {file_content[:300]}...")
            
            if created:
                # Save file content to session snapshot
                session.document_title = file_name or "Uploaded File"
                session.document_content = file_content
                session.title = user_message[:50] + ('...' if len(user_message) > 50 else '')
                session.save()
                logger.info(f"💾 Session {session_id} created with file content: {file_name or 'unnamed'}")
            else:
                # Use snapshot from session (if exists)
                if session.document_content:
                    document_content = session.document_content
                    logger.info(f"📋 Using snapshot from existing session")
                else:
                    # Update session with new file content
                    session.document_content = file_content
                    session.document_title = file_name or "Uploaded File"
                    session.save()
                    logger.info(f"💾 Updated session with new file content")
            
        else:
            # Case 3: Check if session already has a document
            if session.document or session.document_content:
                # Use existing document from session
                document = session.document
                document_content = session.document_content
                logger.info(f"📋 Using document from existing session:")
                logger.info(f"   Document: {session.document_title}")
                logger.info(f"   Document ID: {session.document_id}")
                logger.info(f"   Content length: {len(document_content) if document_content else 0} chars")
            else:
                # Case 4: General chat without document
                if created:
                    session.title = user_message[:50] + ('...' if len(user_message) > 50 else '')
                    session.save()
                logger.info(f"💬 Session {session_id} - general chat without document")
        
        # 🔍 LOG: Final document_content status
        logger.info(f"🎯 Final document_content for AI:")
        if document_content:
            logger.info(f"   ✅ HAS CONTENT: {len(document_content)} chars")
            logger.info(f"   Preview: {document_content[:200]}...")
        else:
            logger.info(f"   ❌ NO CONTENT - will use general chat mode")
        
        # Save user message to history
        ChatHistory.objects.create(
            session=session,
            document=document,
            user=request.user,
            role='user',
            content=user_message,
        )
        
        # Initialize chat service with document_id for vector search
        doc_id = document.id if document else None
        chat_service = DocumentChatService(
            document_id=str(doc_id) if doc_id else None,
            document_content=document_content
        )
        
        def generate_response():
            """Generator for streaming response"""
            try:
                full_response = []
                
                for chunk in chat_service.chat(user_message, chat_history):
                    full_response.append(chunk)
                    yield f"data: {json.dumps({'type': 'token', 'content': chunk})}\n\n"
            
                complete_response = ''.join(full_response)
                ChatHistory.objects.create(
                    session=session,
                    document=document,
                    user=request.user,
                    role='assistant',
                    content=complete_response,
                )
                
                # Update session timestamp
                session.save(update_fields=['updated_at'])
                
                # Send completion signal
                yield f"data: {json.dumps({'type': 'done', 'content': complete_response})}\n\n"
                
            except Exception as e:
                logger.error(f"Chat streaming error: {str(e)}")
                logger.error(traceback.format_exc())
                error_msg = f"Stream error: {str(e)}"
                yield f"data: {json.dumps({'type': 'error', 'content': error_msg})}\n\n"
        
        # Return streaming response
        response = StreamingHttpResponse(
            generate_response(),
            content_type='text/event-stream',
        )
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response
    
    @action(detail=False, methods=['post'], url_path='chat-with-file')
    def chat_with_file(self, request):
        """
        Chat endpoint with file upload (multipart/form-data)
        Frontend gửi file qua form-data:
        - file: File upload
        - message: Text message
        - session_id: Optional session ID
        """
        # 🔍 LOG: Raw request data
        logger.info(f"=" * 60)
        logger.info(f"📤 File upload request received:")
        logger.info(f"  - Content-Type: {request.content_type}")
        logger.info(f"  - FILES: {list(request.FILES.keys())}")
        logger.info(f"  - DATA keys: {list(request.data.keys())}")
        
        serializer = ChatWithFileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        uploaded_file = data.get('file')
        user_message = data['message']
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        # 🔍 LOG: Uploaded file info
        if uploaded_file:
            logger.info(f"  - File name: {uploaded_file.name}")
            logger.info(f"  - File size: {uploaded_file.size} bytes")
            logger.info(f"  - File type: {uploaded_file.content_type}")
        else:
            logger.info(f"  - ⚠️ No file uploaded")
        logger.info(f"=" * 60)
        
        document_content = None
        file_name = None
        
        # Extract file content
        if uploaded_file:
            file_name = uploaded_file.name
            try:
                # Read file content based on type
                if PDFExtractor.is_pdf(uploaded_file):
                    # Extract text from PDF
                    logger.info(f"📄 Processing PDF file: {file_name}")
                    document_content = PDFExtractor.extract_text(uploaded_file)
                    
                    if not document_content:
                        return Response(
                            {'error': 'Failed to extract text from PDF. The PDF might be empty or image-based.'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    logger.info(f"✅ PDF extracted successfully:")
                    logger.info(f"   File: {file_name}")
                    logger.info(f"   Content length: {len(document_content)} chars")
                    logger.info(f"   Content preview: {document_content[:300]}...")
                    
                elif uploaded_file.content_type == 'text/plain':
                    document_content = uploaded_file.read().decode('utf-8')
                    logger.info(f"✅ Text file read: {len(document_content)} chars")
                    
                elif uploaded_file.content_type == 'application/json':
                    document_content = uploaded_file.read().decode('utf-8')
                    logger.info(f"✅ JSON file read: {len(document_content)} chars")
                    
                else:
                    # Try to decode as text
                    try:
                        document_content = uploaded_file.read().decode('utf-8')
                        logger.info(f"✅ File decoded as text: {len(document_content)} chars")
                    except UnicodeDecodeError:
                        return Response(
                            {'error': f'Unsupported file type: {uploaded_file.content_type}. Supported types: PDF, TXT, JSON'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                
                # 🔍 LOG: Successfully extracted content
                logger.info(f"✅ File content extracted successfully:")
                logger.info(f"   File: {file_name}")
                logger.info(f"   Content length: {len(document_content)} chars")
                logger.info(f"   Content preview: {document_content[:300]}...")
                
            except Exception as e:
                logger.error(f"❌ Failed to read file: {str(e)}")
                logger.error(traceback.format_exc())
                return Response(
                    {'error': f'Failed to read file: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Get or create session
        session, created = ChatSession.objects.get_or_create(
            session_id=session_id,
            user=request.user,
        )
        
        # 🔍 LOG: Session info
        logger.info(f"📋 Session status:")
        logger.info(f"   Session ID: {session_id}")
        logger.info(f"   Created new: {created}")
        logger.info(f"   Has existing content: {bool(session.document_content)}")
        
        # Save document and process chunks if this is a new file
        document = None
        if created or not session.document_content:
            # Create Document object to store permanently
            document = Document.objects.create(
                user=request.user,
                title=file_name or "Uploaded File",
                content=document_content or "",
                language='vi'
            )
            logger.info(f"📄 Document created: {document.title} (ID: {document.id})")
            
            # Process document: chunk and create embeddings
            if document_content:
                try:
                    embedding_service = DocumentEmbeddingService()
                    processed_chunks = embedding_service.process_document(document_content)
                    
                    # Save chunks to database
                    chunks_to_create = []
                    for chunk_data in processed_chunks:
                        chunks_to_create.append(
                            DocumentChunk(
                                document=document,
                                content=chunk_data['content'],
                                chunk_index=chunk_data['chunk_index'],
                                embedding=chunk_data['embedding'],
                                token_count=chunk_data['token_count']
                            )
                        )
                    
                    # Bulk create for efficiency
                    DocumentChunk.objects.bulk_create(chunks_to_create)
                    logger.info(f"✅ Saved {len(chunks_to_create)} chunks to database")
                    
                except Exception as e:
                    logger.error(f"❌ Failed to process document chunks: {str(e)}")
                    logger.error(traceback.format_exc())
            
            # Snapshot to session
            session.document = document
            session.document_title = file_name or "Uploaded File"
            session.document_content = document_content
            session.title = user_message[:50] + ('...' if len(user_message) > 50 else '')
            session.save()
            logger.info(f"💾 Session snapshot saved:")
            logger.info(f"   Title: {session.document_title}")
            logger.info(f"   Content length: {len(document_content) if document_content else 0} chars")
        else:
            # Use existing session snapshot
            document = session.document
            document_content = session.document_content
            logger.info(f"📋 Using existing session snapshot:")
            logger.info(f"   Content length: {len(document_content) if document_content else 0} chars")
        
        # Save user message
        ChatHistory.objects.create(
            session=session,
            user=request.user,
            role='user',
            content=user_message,
        )
        
        # Chat service with document_id for vector search
        doc_id = document.id if document else None
        chat_service = DocumentChatService(
            document_id=str(doc_id) if doc_id else None,
            document_content=document_content
        )
        
        def generate_response():
            try:
                full_response = []
                for chunk in chat_service.chat(user_message, []):
                    full_response.append(chunk)
                    yield f"data: {json.dumps({'type': 'token', 'content': chunk})}\n\n"
                
                complete_response = ''.join(full_response)
                ChatHistory.objects.create(
                    session=session,
                    user=request.user,
                    role='assistant',
                    content=complete_response,
                )
                
                session.save(update_fields=['updated_at'])
                yield f"data: {json.dumps({'type': 'done', 'content': complete_response, 'session_id': session_id})}\n\n"
                
            except Exception as e:
                logger.error(f"Chat streaming error: {str(e)}")
                error_msg = f"Error: {str(e)}"
                yield f"data: {json.dumps({'type': 'error', 'content': error_msg})}\n\n"
        
        response = StreamingHttpResponse(
            generate_response(),
            content_type='text/event-stream',
        )
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response
    
    @action(detail=False, methods=['get'], url_path='history')
    def history(self, request):
        """
        Get chat history - filter by query params:
        - session_id: specific session
        - document_id: specific document
        """
        session_id = request.query_params.get('session_id')
        document_id = request.query_params.get('document_id')
        
        # Get chat history
        history_qs = ChatHistory.objects.filter(user=request.user)
        
        if session_id:
            history_qs = history_qs.filter(session__session_id=session_id)
        
        if document_id:
            history_qs = history_qs.filter(document_id=document_id)
        
        serializer = ChatHistorySerializer(history_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='sessions')
    def sessions(self, request):
        """
        Get list of chat sessions - filter by query param:
        - document_id: sessions for specific document (optional)
        """
        from django.db.models import Max, Count
        
        document_id = request.query_params.get('document_id')
        
        # Query sessions
        sessions_qs = ChatSession.objects.filter(user=request.user)
        
        if document_id:
            sessions_qs = sessions_qs.filter(document_id=document_id)
        
        # Annotate with message stats
        sessions_qs = sessions_qs.annotate(
            message_count=Count('messages'),
            last_message_time=Max('messages__created_at'),
        )
        
        # Get first user message as preview
        session_list = []
        for session in sessions_qs:
            first_message = session.messages.filter(role='user').first()
            
            serializer = ChatSessionSerializer(session)
            data = serializer.data
            data['preview'] = first_message.content[:100] if first_message else session.title or ''
            session_list.append(data)
        
        return Response(session_list, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='sessions/(?P<session_id>[^/.]+)')
    def session_detail(self, request, session_id=None):
        """Get session detail with document content snapshot"""
        try:
            session = ChatSession.objects.get(session_id=session_id, user=request.user)
            serializer = ChatSessionDetailSerializer(session)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ChatSession.DoesNotExist:
            return Response(
                {'error': 'Session not found'},
                status=status.HTTP_404_NOT_FOUND
            )
