from django.urls import path
from .views import (
    OrderListCreateView, 
    OrderDetailView, 
    ProductListView, 
    CategoryListView, 
    OrderChatView,
    OrderChatResetView,
    OrderChatInfoView
)

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('order-chat/', OrderChatView.as_view(), name='order-chat'),
    path('order-chat/reset/', OrderChatResetView.as_view(), name='order-chat-reset'),
    path('order-chat/info/', OrderChatInfoView.as_view(), name='order-chat-info'),
]
