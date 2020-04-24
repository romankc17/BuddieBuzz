from django.urls import path
from django.contrib.auth import views as auth_views

from . import views,ajax
from .views import PostUpdateView, PostDeleteView

urlpatterns=[
    path('<str:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('p/create/', views.post_create, name='post_create'),
    path('<str:slug>/update/', PostUpdateView.as_view(), name='post_update'),
    path('<str:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('p/like/', ajax.like, name = 'post_like'),
    path('p/comment/', ajax.post_comment, name='post_comment'),
    path('comment/delete', ajax.post_comment_delete, name = 'post_comment_delete')
]