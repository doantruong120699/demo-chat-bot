"""
Vector Store Service using PostgreSQL with pgvector
"""
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from django.conf import settings
import logging
from typing import List, Dict, Any
import os

logger = logging.getLogger(__name__)


class VectorStoreService:
    """Manage vector storage and retrieval"""
    
    def __init__(self, collection_name: str = "document_training"):
        """
        Initialize vector store
        
        Args:
            collection_name: Name of the collection/table
        """
        self.collection_name = collection_name
        
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=settings.OPENAI_API_KEY,
        )
        
        # Connection string for PostgreSQL
        self.connection_string = self._get_connection_string()
        
        # Initialize vector store
        self.vector_store = None
        self._init_vector_store()
    
    def _get_connection_string(self) -> str:
        """Build PostgreSQL connection string"""
        db_config = settings.DATABASES['default']
        
        return (
            f"postgresql+psycopg://{db_config['USER']}:{db_config['PASSWORD']}"
            f"@{db_config['HOST']}:{db_config['PORT']}/{db_config['NAME']}"
        )
    
    def _init_vector_store(self):
        """Initialize PGVector store"""
        try:
            self.vector_store = PGVector(
                embeddings=self.embeddings,
                collection_name=self.collection_name,
                connection=self.connection_string,
                use_jsonb=True,
            )
            logger.info(f"Vector store initialized: {self.collection_name}")
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {str(e)}")
            raise
    
    def add_chunks(self, chunks: List[Dict[str, Any]], document_id: str) -> bool:
        """
        Add document chunks to vector store
        
        Args:
            chunks: List of chunk dicts with 'content' and 'metadata'
            document_id: Document ID for metadata
            
        Returns:
            Success boolean
        """
        try:
            # Prepare texts and metadatas
            texts = []
            metadatas = []
            
            for chunk in chunks:
                texts.append(chunk['content'])
                
                metadata = chunk.get('metadata', {})
                metadata['document_id'] = document_id
                metadata['chunk_index'] = chunk['chunk_index']
                metadatas.append(metadata)
            
            # Add to vector store
            ids = self.vector_store.add_texts(
                texts=texts,
                metadatas=metadatas,
            )
            
            logger.info(f"Added {len(ids)} chunks to vector store for document {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add chunks to vector store: {str(e)}")
            return False
    
    def search(self, query: str, document_id: str = None, k: int = 4) -> List[Dict[str, Any]]:
        """
        Search for relevant chunks
        
        Args:
            query: Search query
            document_id: Optional filter by document ID
            k: Number of results to return
            
        Returns:
            List of relevant chunks with metadata and scores
        """
        try:
            # Build filter
            filter_dict = {}
            if document_id:
                filter_dict['document_id'] = document_id
            
            # Perform similarity search
            results = self.vector_store.similarity_search_with_score(
                query=query,
                k=k,
                filter=filter_dict if filter_dict else None,
            )
            
            # Format results
            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    'content': doc.page_content,
                    'metadata': doc.metadata,
                    'score': float(score),
                })
            
            logger.info(f"Found {len(formatted_results)} relevant chunks for query")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            return []
    
    def delete_document_chunks(self, document_id: str) -> bool:
        """
        Delete all chunks for a document
        
        Args:
            document_id: Document ID
            
        Returns:
            Success boolean
        """
        try:
            # PGVector doesn't have direct delete by filter
            # Need to implement manual deletion via SQL
            from sqlalchemy import create_engine, text
            
            engine = create_engine(self.connection_string)
            with engine.connect() as conn:
                query = text(
                    f"DELETE FROM langchain_pg_embedding "
                    f"WHERE cmetadata->>'document_id' = :doc_id "
                    f"AND collection_id = (SELECT uuid FROM langchain_pg_collection WHERE name = :collection)"
                )
                conn.execute(query, {"doc_id": document_id, "collection": self.collection_name})
                conn.commit()
            
            logger.info(f"Deleted chunks for document {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete chunks: {str(e)}")
            return False
