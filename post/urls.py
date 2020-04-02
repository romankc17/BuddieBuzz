from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import PostUpdateView, PostDeleteView

urlpatterns=[
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('create/', views.post_create, name='post_create'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]