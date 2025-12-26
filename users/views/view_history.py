# post/views/view_history.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from post.models import Post, PostViewHistory
from post.serializers import PostViewHistorySerializer


class PostViewRecordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)

        PostViewHistory.objects.update_or_create(
            user=request.user,
            post=post
        )

        return Response({'msg': 'view recorded'})

class ViewHistoryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = request.user.view_history.select_related('post', 'post__author')
        serializer = PostViewHistorySerializer(
            qs,
            many=True,
            context={'request': request}  # ⚠️ 记得传 request
        )
        return Response(serializer.data)
