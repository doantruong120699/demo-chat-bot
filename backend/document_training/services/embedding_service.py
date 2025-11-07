"""
Document Chunking and Embedding Service
"""
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from django.conf import settings
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class DocumentEmbeddingService:
    """Service for chunking documents and creating embeddings"""
    
    def __init__(self):
        """Initialize embedding service"""
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-ada-002",
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Text splitter configuration
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # Characters per chunk
            chunk_overlap=200,  # Overlap between chunks
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def chunk_document(self, content: str) -> List[str]:
        """
        Split document into chunks
        
        Args:
            content: Full document text
            
        Returns:
            List of text chunks
        """
        try:
            logger.info(f"📄 Chunking document (length: {len(content)} chars)")
            
            chunks = self.text_splitter.split_text(content)
            
            logger.info(f"✅ Created {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            logger.error(f"❌ Chunking failed: {str(e)}")
            raise
    
    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings for text chunks
        
        Args:
            texts: List of text strings
            
        Returns:
            List of embedding vectors
        """
        try:
            logger.info(f"🔮 Creating embeddings for {len(texts)} chunks")
            
            embeddings = self.embeddings.embed_documents(texts)
            
            logger.info(f"✅ Created {len(embeddings)} embeddings (dim: {len(embeddings[0])})")
            return embeddings
            
        except Exception as e:
            logger.error(f"❌ Embedding creation failed: {str(e)}")
            raise
    
    def process_document(self, content: str) -> List[Dict]:
        """
        Process document: chunk + embed
        
        Args:
            content: Full document text
            
        Returns:
            List of dicts with 'content' and 'embedding'
        """
        try:
            # Split into chunks
            chunks = self.chunk_document(content)
            
            # Create embeddings
            embeddings = self.create_embeddings(chunks)
            
            # Combine
            results = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                results.append({
                    'chunk_index': i,
                    'content': chunk,
                    'embedding': embedding,
                    'token_count': len(chunk) // 4  # Rough estimate
                })
            
            logger.info(f"✅ Processed document into {len(results)} chunks with embeddings")
            return results
            
        except Exception as e:
            logger.error(f"❌ Document processing failed: {str(e)}")
            raise
