from rest_framework import serializers
from .models import Post,Comment,PostImage


#图片序列化器
class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'image', 'order']


class LifePostListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(
        source='author.username',
        read_only=True
    )
    images = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'author_name',
            'like_count',
            'view_count',
            'created_at',
            'images'
        ]

#详情页
class LifePostDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(
        source='author.username',
        read_only=True
    )
    images = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'author_name',
            'images',
            'like_count',
            'view_count',
            'created_at'
        ]

#返回评论数量
comment_count = serializers.IntegerField(
    source='comments.count',
    read_only=True
)

#辅助前端判断点赞按钮是否高亮，可否点击
is_liked = serializers.SerializerMethodField()

def get_is_liked(self, obj):
    user = self.context['request'].user
    if not user.is_authenticated:
        return False
    return obj.likes.filter(user=user).exists()

#评论序列化器
class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(
        source='author.username',
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


