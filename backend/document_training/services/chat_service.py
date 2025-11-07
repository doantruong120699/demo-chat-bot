"""
Chat Service with RAG (Retrieval Augmented Generation)
"""
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, AIMessage
from django.conf import settings
import logging
from typing import List, Dict, Generator, Optional
from .vector_search_service import VectorSearchService

logger = logging.getLogger(__name__)


class DocumentChatService:
    """Chat service with semantic search for Q&A"""
    
    def __init__(self, document_id: str = None, document_content: str = None):
        """
        Initialize chat service
        
        Args:
            document_id: Optional document ID for vector search
            document_content: Optional full document content (fallback for non-chunked docs)
        """
        self.document_id = document_id
        self.document_content = document_content
        self.vector_search = VectorSearchService() if document_id or document_content else None
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4.1",
            temperature=0.7,
            openai_api_key=settings.OPENAI_API_KEY,
            streaming=True,
        )
        
        # System prompt with RAG context
        if document_id or document_content:
            self.system_prompt = """Bạn là trợ lý AI thông minh, hỗ trợ người dùng trả lời câu hỏi dựa trên tài liệu được cung cấp.

            CÁC ĐOẠN VĂN BẢN LIÊN QUAN:
            {context}

            NHIỆM VỤ:
            - Đọc kỹ các đoạn văn bản được cung cấp ở trên
            - Trả lời câu hỏi dựa trên thông tin từ các đoạn văn bản
            - Nếu câu hỏi KHÔNG liên quan đến nội dung các đoạn văn bản, hãy trả lời dựa trên kiến thức chung
            - Trả lời một cách tự nhiên, rõ ràng và hữu ích
            - Nếu thông tin trong các đoạn văn bản không đủ để trả lời, hãy nói rõ và đưa ra câu trả lời tốt nhất có thể
            - Khi trích dẫn thông tin, hãy ghi rõ đến từ [Đoạn X]

            Hãy trả lời câu hỏi của người dùng."""
                    else:
                        self.system_prompt = """Bạn là trợ lý AI thông minh và thân thiện.

            NHIỆM VỤ:
            - Trả lời câu hỏi của người dùng một cách chính xác và hữu ích
            - Giải thích rõ ràng, dễ hiểu
            - Thân thiện và lịch sự
            - Nếu không biết câu trả lời, hãy thừa nhận và đề xuất hướng giải quyết

            Hãy trả lời câu hỏi của người dùng."""
    
    def chat(
        self, 
        user_message: str, 
        chat_history: List[Dict[str, str]] = None,
    ) -> Generator[str, None, None]:
        """
        Chat with streaming response using RAG
        
        Args:
            user_message: User's question
            chat_history: Previous chat messages
            
        Yields:
            Chunks of response text
        """
        # Build messages
        messages = []
        
        # Get relevant context if document exists
        context = ""
        if self.document_id or self.document_content:
            try:
                # Try vector search first (if document has chunks)
                if self.document_id:
                    logger.info(f"🔍 Searching for relevant chunks for: '{user_message[:100]}'")
                    relevant_chunks = self.vector_search.search_similar_chunks(
                        query=user_message,
                        document_id=self.document_id,
                        top_k=3  # Get top 3 most relevant chunks
                    )
                    
                    if relevant_chunks:
                        context = self.vector_search.get_context_from_chunks(relevant_chunks)
                        logger.info(f"✅ Found {len(relevant_chunks)} relevant chunks")
                    else:
                        logger.info(f"⚠️ No chunks found, using full document content")
                        context = self.document_content[:3000] if self.document_content else ""
                else:
                    # No document_id, use full content
                    logger.info(f"📄 Using full document content (no vector search)")
                    context = self.document_content[:3000] if self.document_content else ""
                    
            except Exception as e:
                logger.error(f"❌ Context retrieval failed: {str(e)}")
                # Fallback to full document
                context = self.document_content[:3000] if self.document_content else ""
        
        # Add system prompt with context
        if context:
            messages.append(("system", self.system_prompt.format(context=context)))
        else:
            messages.append(("system", self.system_prompt))
        
        # Add chat history if provided
        if chat_history:
            for msg in chat_history[-6:]:  # Last 3 exchanges
                if msg['role'] == 'user':
                    messages.append(("human", msg['content']))
                elif msg['role'] == 'assistant':
                    messages.append(("assistant", msg['content']))
        
        # Add current user message
        messages.append(("human", user_message))
        
        # Create prompt
        prompt = ChatPromptTemplate.from_messages(messages)
        
        # Stream response
        try:
            for chunk in self.llm.stream(prompt.format_messages()):
                if chunk.content:
                    yield chunk.content
        except Exception as e:
            logger.error(f"Chat streaming failed: {str(e)}")
            yield f"Xin lỗi, đã có lỗi xảy ra: {str(e)}"
