from rest_framework import serializers

from posts.models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'is_deleted', 'created_at', 'updated_at')
        read_only_fields = ('author', 'post', 'is_deleted', 'created_at')


class PostSerializer(serializers.ModelSerializer):
    # comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(default=0, read_only=True, source='comments.count')
    class Meta:
        model = Post
        fields = ('id', 'description', 'image', 'author', 'is_deleted', 'created_at', 'updated_at', 'comments_count')
        read_only_fields = ('is_deleted', 'comments_count', 'author','image')


    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance