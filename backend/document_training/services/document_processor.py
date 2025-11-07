"""
Document processor: chunking and preparing for training
"""
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Process documents for training"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize processor
        
        Args:
            chunk_size: Size of each chunk in characters
            chunk_overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
    
    def chunk_text(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Split text into chunks
        
        Args:
            text: Input text to chunk
            metadata: Additional metadata to attach to chunks
            
        Returns:
            List of chunk dicts with 'content', 'index', 'metadata'
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for chunking")
            return []
        
        try:
            # Split text
            chunks = self.text_splitter.split_text(text)
            
            # Prepare chunk objects
            chunk_objects = []
            for idx, chunk in enumerate(chunks):
                chunk_obj = {
                    'content': chunk,
                    'chunk_index': idx,
                    'metadata': metadata or {},
                }
                chunk_objects.append(chunk_obj)
            
            logger.info(f"Created {len(chunk_objects)} chunks from text")
            return chunk_objects
            
        except Exception as e:
            logger.error(f"Chunking failed: {str(e)}")
            return []
    
    def process_document(self, raw_text: str, document_id: str = None) -> List[Dict[str, Any]]:
        """
        Process full document: clean, chunk, and prepare metadata
        
        Args:
            raw_text: Raw extracted text
            document_id: Optional document ID for metadata
            
        Returns:
            List of processed chunks
        """
        # Clean text (basic cleaning)
        cleaned_text = self._clean_text(raw_text)
        
        # Prepare metadata
        metadata = {
            'document_id': document_id,
            'total_length': len(cleaned_text),
        }
        
        # Chunk
        chunks = self.chunk_text(cleaned_text, metadata)
        
        return chunks
    
    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Basic text cleaning
        
        Args:
            text: Input text
            
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        lines = [line.strip() for line in text.split('\n')]
        lines = [line for line in lines if line]
        cleaned = '\n'.join(lines)
        
        # Remove multiple spaces
        import re
        cleaned = re.sub(r' +', ' ', cleaned)
        
        return cleaned.strip()
