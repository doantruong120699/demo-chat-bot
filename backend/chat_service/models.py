from django.db import models
from pgvector.django import VectorField
from typing import List, Any
from langchain_community.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
import openai
import time
from langchain_postgres import PGVector
from common.models.base import DateTimeModel, UuidModel, SoftDeleteModel
from accounts.models.user import User

# Create your models here.

class DocumentEmbedding(models.Model):
    embedding = VectorField(null=True)
    content = models.TextField()
    metadata = models.JSONField(null=True)

    def __str__(self):
        return self.content
    
def get_pgvector_client() -> PGVector:    
    # connection = f"postgresql+psycopg2://admin:Aa123456localhost:5433/chat_ai"
    connection = "postgresql+psycopg2://admin:Aa123456%40@localhost:5433/chat_ai"

    
    return PGVector(
        embeddings=OpenAIEmbeddings(model="text-embedding-3-small"),
        collection_name="whitepaper_embeddings",
        connection=connection,
        use_jsonb=True,
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


class Chat(UuidModel, DateTimeModel, SoftDeleteModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)

class Message(UuidModel, DateTimeModel):
    class Sender(models.TextChoices):
        HUMAN = "HUMAN", "HUMAN"
        BOT = "BOT", "BOT"

    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    message = models.TextField(null=True, blank=True)
    sender = models.CharField(max_length=10, choices=Sender.choices, default=Sender.HUMAN)
    extra_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.message
