import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from api.serializers import PostSerializer
from posts.models import Post


# Create your views here.


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().exclude(is_deleted=True)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def like_post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        self.request.user.liked_posts.add(post)
        return JsonResponse({'status': 'ok'})

    @action(detail=True, methods=['get'])
    def unlike_post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        self.request.user.liked_posts.remove(post)
        return JsonResponse({'status': 'ok'})

