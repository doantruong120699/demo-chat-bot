from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import StreamingHttpResponse
import time
from .services import ChatService
from .serializers import ChatRequestSerializer, ChatHistoryListSerializer, ChatHistoryDetailSerializer
from rest_framework.response import Response
from rest_framework import status
from agents.text2sql import Text2SQL
from agents.chat import ChatBot
from rest_framework.viewsets import ModelViewSet
from .models import Chat
class ChatHistoryView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    lookup_field = "uuid"
    ordering = ["-created_at"]

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user, is_deleted=False)

    def get_serializer(self, *args, **kwargs):
        if self.action == "list":
            return ChatHistoryListSerializer(*args, **kwargs)
        elif self.action == "retrieve":
            return ChatHistoryDetailSerializer(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    

class ChatView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatRequestSerializer

    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     chat_service = ChatService()
    #     return chat_service.chat(request, serializer.validated_data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        chat_service = ChatService()
        return chat_service.chat_interact_db(request, serializer.validated_data)
        

class CreateDocumentEmbeddingView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        chat_service = ChatService()
        chat_service._create_documents_from_text()
        return Response(status=status.HTTP_200_OK)