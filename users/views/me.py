from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.serializers import MeSerializer

from post.models import Post,PostViewHistory
from post.serializers import LifePostListSerializer

#上传头像、修改昵称
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = MeSerializer(
            request.user,
            context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = MeSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request):
        serializer = MeSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


#我发过的帖子（不区分生活区学习区，前端需要做区分）
class MyPostListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Post.objects.filter(
            author=request.user,
            target__in=['life', 'study']
        ).order_by('-created_at')

        serializer = LifePostListSerializer(qs, many=True)
        return Response(serializer.data)

#浏览记录
class MyViewHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        histories = PostViewHistory.objects.filter(
            user=request.user,
            post__target__in=['life', 'study']
        ).select_related('post')

        posts = [h.post for h in histories]
        serializer = LifePostListSerializer(posts, many=True)
        return Response(serializer.data)