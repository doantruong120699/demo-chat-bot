from django.urls import path
from chat_service.views import ChatView, CreateDocumentEmbeddingView, ChatHistoryView


urlpatterns = [
    # Chat
    path("chat", ChatView.as_view(), name="chat"),
    path("create-document-embedding", CreateDocumentEmbeddingView.as_view(), name="create-document-embedding"),
    # Chat History
    path("chat-history", ChatHistoryView.as_view({
        "get": "list",
    }), name="chat-history"),
    path("chat-history/<uuid:uuid>", ChatHistoryView.as_view({
        "get": "retrieve",
        "delete": "destroy",
    }), name="chat-history-detail"),
]
