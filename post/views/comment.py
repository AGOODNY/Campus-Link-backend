from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from post.models import Post, Comment
from post.serializers import CommentSerializer


# 获取评论列表
class CommentListView(APIView):
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"detail": "Post not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        comments = post.comments.order_by('created_at')
        serializer = CommentSerializer(comments, many=True)

        return Response(
            {
                'code': 200,
                'message': 'ok',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )


# 发表评论
class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"detail": "Post not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        content = request.data.get('content')
        if not content:
            return Response(
                {"detail": "Content is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 创建评论
        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=content
        )

        # 关键：用和列表一模一样的 serializer 返回
        serializer = CommentSerializer(comment)

        return Response(
            {
                'code': 200,
                'message': 'ok',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
