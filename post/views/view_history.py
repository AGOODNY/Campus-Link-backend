from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from post.models import Post, PostViewHistory
from post.serializers import LifePostListSerializer, PostViewHistorySerializer
from django.shortcuts import get_object_or_404

class PostViewRecordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id=None, pk=None):
        post_id = post_id or pk
        post = get_object_or_404(Post, pk=post_id)

        PostViewHistory.objects.update_or_create(
            user=request.user,
            post=post,
            defaults={}
        )
        return Response({'msg': 'view recorded'})

class ViewHistoryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = (
            request.user.view_history
            .select_related('post', 'post__author')
            .prefetch_related('post__images')  # 预取图片，减少 N+1
        )
        serializer = PostViewHistorySerializer(
            qs, many=True, context={'request': request}
        )
        return Response(serializer.data)