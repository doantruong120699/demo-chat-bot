from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, DocumentChatView

router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='document')

app_name = 'document_training'

urlpatterns = [
    # Router URLs for documents CRUD
    path('', include(router.urls)),
    
    # Chat endpoints
    path('chat/', DocumentChatView.as_view({'post': 'chat'}), name='chat'),
    path('chat-with-file/', DocumentChatView.as_view({'post': 'chat_with_file'}), name='chat-with-file'),
    
    # Chat sessions
    path('sessions/', DocumentChatView.as_view({'get': 'sessions'}), name='sessions'),
    path('sessions/<str:session_id>/', DocumentChatView.as_view({'get': 'session_detail'}), name='session-detail'),
    
    # Chat history
    path('history/', DocumentChatView.as_view({'get': 'history'}), name='chat-history'),
]
