from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from post.models import Post, PostLike
from django.db import IntegrityError

class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        user = request.user

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=404)

        try:
            PostLike.objects.create(user=user, post=post)
        except IntegrityError:
            return Response(
                {"detail": "You have already liked this post"},
                status=400
            )

        # 点赞数从数据库统计
        post.like_count = post.likes.count()
        post.save(update_fields=['like_count'])

        return Response({
            "like_count": post.like_count
        })
