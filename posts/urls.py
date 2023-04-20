from django.urls import path

from posts.views import IndexView, CreatePostView, like_post, unlike_post, PostDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('post/add', CreatePostView.as_view(), name='post_add'),
    path('post/<int:pk>/like_post', like_post, name='like_post'),
    path('post/<int:pk>/unlike_post', unlike_post, name='unlike_post'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
]
