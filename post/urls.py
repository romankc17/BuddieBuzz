from django.urls import path
from django.contrib.auth import views as auth_views

from . import views,ajax
from .views import PostUpdateView, PostDeleteView

urlpatterns=[
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('create/', views.post_create, name='post_create'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('p/like/', ajax.like, name = 'post_like'),
    path('comment/', ajax.post_comment, name='post_comment')
]