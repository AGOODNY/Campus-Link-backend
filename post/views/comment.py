from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from post.models import Post, Comment
from post.serializers import CommentSerializer

#获取评论列表
class CommentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=404)

        comments = post.comments.order_by('created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

#发表评论
class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=404)

        content = request.data.get('content')
        if not content:
            return Response(
                {"detail": "Content is required"},
                status=400
            )

        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=content
        )

        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=201)
