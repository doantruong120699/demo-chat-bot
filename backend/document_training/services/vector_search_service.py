"""
Vector Search Service for semantic similarity
"""
from langchain_openai import OpenAIEmbeddings
from django.conf import settings
from django.db.models import F
from ..models import DocumentChunk
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class VectorSearchService:
    """Service for semantic search using pgvector"""
    
    def __init__(self):
        """Initialize search service"""
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-ada-002",
            openai_api_key=settings.OPENAI_API_KEY
        )
    
    def search_similar_chunks(
        self, 
        query: str, 
        document_id: str = None,
        top_k: int = 3
    ) -> List[Dict]:
        """
        Search for similar chunks using semantic similarity
        
        Args:
            query: User's question
            document_id: Optional document ID to filter by
            top_k: Number of results to return
            
        Returns:
            List of relevant chunks with content and similarity scores
        """
        try:
            logger.info(f"🔍 Searching for: '{query[:100]}'")
            
            # Create query embedding
            query_embedding = self.embeddings.embed_query(query)
            logger.info(f"✅ Created query embedding (dim: {len(query_embedding)})")
            
            # Build queryset
            queryset = DocumentChunk.objects.all()
            if document_id:
                queryset = queryset.filter(document_id=document_id)
                logger.info(f"🎯 Filtering by document_id: {document_id}")
            
            # Perform vector similarity search using pgvector
            # Using cosine distance (1 - cosine_similarity)
            queryset = queryset.annotate(
                distance=F('embedding').cosine_distance(query_embedding)
            ).order_by('distance')[:top_k]
            
            # Format results
            results = []
            for chunk in queryset:
                results.append({
                    'content': chunk.content,
                    'chunk_index': chunk.chunk_index,
                    'similarity': 1 - float(chunk.distance),  # Convert distance to similarity
                    'document_title': chunk.document.title,
                })
            
            logger.info(f"✅ Found {len(results)} relevant chunks")
            for i, r in enumerate(results):
                logger.info(f"  {i+1}. Chunk {r['chunk_index']} (similarity: {r['similarity']:.3f})")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Search failed: {str(e)}")
            raise
    
    def get_context_from_chunks(self, chunks: List[Dict]) -> str:
        """
        Combine relevant chunks into context string
        
        Args:
            chunks: List of chunk dicts from search
            
        Returns:
            Combined text context
        """
        if not chunks:
            return ""
        
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            context_parts.append(f"[Đoạn {i}]:\n{chunk['content']}")
        
        return "\n\n".join(context_parts)
