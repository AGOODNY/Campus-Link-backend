from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

from post.models import Post, PostViewHistory
from post.serializers import (
    LifePostListSerializer,
    LifePostDetailSerializer,
)

class PostListView(APIView):
    def get(self, request, target):
        order = request.query_params.get('order', 'time')
        category = request.query_params.get('category')

        qs = Post.objects.filter(target=target)

        if target == 'life' and category:
            qs = qs.filter(life_category=category)

        if order == 'hot':
            qs = qs.order_by('-like_count', '-created_at')
        else:
            qs = qs.order_by('-created_at')

        serializer = LifePostListSerializer(qs, many=True, context={'request': request})

        return Response({
            'code': 200,
            'message': 'ok',
            'data': {
                'list': serializer.data,
                'hasMore': False
            }
        })

class PostDetailView(APIView):
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=404)

        post.view_count += 1
        post.save(update_fields=['view_count'])

        if request.user.is_authenticated:
            PostViewHistory.objects.update_or_create(
                user=request.user,
                post=post
            )

        serializer = LifePostDetailSerializer(
            post,
            context={'request': request}
        )
        return Response(serializer.data)

#生活区搜索
#不限制life_category,自动搜索两个分区里的内容
class LifePostSearchView(APIView):
    def get(self, request):
        keyword = request.query_params.get('q', '').strip()

        if not keyword:
            return Response([])

        qs = Post.objects.filter(
            target='life'
        ).filter(
            Q(title__icontains=keyword) |  #支持标题命中或内容命中
            Q(content__icontains=keyword)
        ).order_by('-created_at')

        serializer = LifePostListSerializer(qs, many=True)
        return Response({
            'code': 200,
            'message': 'ok',
            'data': {
                'list': serializer.data,
                'hasMore': False
            }
        })

#学习区搜索
class StudyPostSearchView(APIView):
    def get(self, request):
        keyword = request.query_params.get('q', '').strip()

        if not keyword:
            return Response([])

        qs = Post.objects.filter(
            target='study'
        ).filter(
            Q(title__icontains=keyword) |
            Q(content__icontains=keyword)
        ).order_by('-created_at')

        serializer = LifePostListSerializer(qs, many=True)
        return Response(serializer.data)