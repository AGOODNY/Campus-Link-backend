from rest_framework import serializers
from .models import Post, Comment, PostImage

class LifePostListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(
        source='author.nickname',
        read_only=True
    )

    avatar = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    create_time = serializers.DateTimeField(
        source='created_at',
        read_only=True
    )

    category = serializers.CharField(
        source='life_category',
        read_only=True
    )

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'images',
            'user_name',
            'avatar',
            'like_count',
            'comment_count',
            'create_time',
            'category',
        ]

    def get_images(self, obj):
        request = self.context.get('request')
        urls = []
        for img in obj.images.all().order_by("order"):
            try:
                url = img.image.url
                if request:
                    url = request.build_absolute_uri(url)
                urls.append(url)
            except Exception:
                continue
        return urls

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_avatar(self, obj):
        avatar = getattr(obj.author, 'avatar', None)
        if avatar:
            try:
                url = avatar.url
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(url)
                return url
            except Exception:
                return None
        return None



class LifePostDetailSerializer(LifePostListSerializer):
    pass


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(
        source='author.nickname',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = [
            'id',
            'author_name',
            'content',
            'created_at'
        ]


class PostViewHistorySerializer:
    pass