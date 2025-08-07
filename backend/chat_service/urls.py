from django.urls import path
from chat_service.views import ChatView, CreateDocumentEmbeddingView


urlpatterns = [
    path("chat", ChatView.as_view(), name="chat"),
    path("create-document-embedding", CreateDocumentEmbeddingView.as_view(), name="create-document-embedding"),
]
