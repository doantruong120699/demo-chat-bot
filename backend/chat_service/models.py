from django.db import models
from pgvector.django import VectorField
from typing import List, Any
from langchain_community.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
import openai
import time
from langchain_community.vectorstores import PGVector

# Create your models here.

class DocumentEmbedding(models.Model):
    embedding = VectorField(null=True)
    content = models.TextField()
    metadata = models.JSONField(null=True)

    def __str__(self):
        return self.content
    
def get_pgvector_client() -> PGVector:
    return PGVector(
        connection_string="postgresql://postgres:postgres@localhost:5433/postgres",
        embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
    )


def create_document_embedding(
    docs: List[Document],
):
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
    for doc in docs:
        for retry in range(3):
            try:
                embedding = embedding_model.embed_documents([doc.page_content])
                print("================================================")
                print(embedding)
                print(doc.page_content)
                print(doc.metadata)
                print(getattr(doc, "content", getattr(doc, "page_content", "")))
                print(getattr(doc, "metadata", {}))
                DocumentEmbedding.objects.create(
                    embedding=embedding[0],
                    content = getattr(doc, "content", getattr(doc, "page_content", "")),
                    metadata = getattr(doc, "metadata", {}),
                )
                break
            except openai.RateLimitError:
                if retry < 2:
                    time.sleep(30)
                    continue
                raise

