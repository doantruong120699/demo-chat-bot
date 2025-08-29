from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.http import StreamingHttpResponse
import time
from .services import ChatService
from .serializers import ChatRequestSerializer
from rest_framework.response import Response
from rest_framework import status
from agents.text2sql import Text2SQL
from agents.chat import ChatBot

class ChatView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ChatRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        chat_service = ChatService()
        return chat_service.chat(serializer.validated_data)

    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     chat_bot = ChatBot()
        
    #     # Create a streaming response from the generator
    #     def stream_response():
    #         for chunk in chat_bot.chat_handler(serializer.validated_data["message"]):
    #             yield chunk

    #     return StreamingHttpResponse(
    #         stream_response(),
    #         content_type='text/event-stream; charset=utf-8'
    #     )

    # def get(self, request):
    #     text2sql = Text2SQL()
    #     response = text2sql.chat_handler("How many users are there in the database?")
    #     return Response(response, status=status.HTTP_200_OK)

class CreateDocumentEmbeddingView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        chat_service = ChatService()
        chat_service._create_documents_from_text()
        return Response(status=status.HTTP_200_OK)