# core/urls.py
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import signup_view
from django.urls import path
from .views import (
    PostListView, PostDetailView, PostCreateView,
    PostUpdateView, PostDeleteView, add_comment,
    ConversationUpdateView, ConversationDeleteView,
)

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', add_comment, name='add-comment'),
    path('signup/', signup_view, name='signup'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('conversations/', views.conversations_page, name='conversations'),
    path('conversations/edit/<int:pk>/', ConversationUpdateView.as_view(), name='edit-conversation'),
    path('conversations/delete/<int:pk>/', ConversationDeleteView.as_view(), name='delete-conversation'),
    
]
