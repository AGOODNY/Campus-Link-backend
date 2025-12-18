from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from common.serializers import UnifiedPostSerializer
from issues.models import Issue,IssueImage
from post.models import Post, PostImage


class UnifiedPostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UnifiedPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user = request.user
        target = data['target']

        # 发到生活区 / 学习区
        if target in ['study', 'life']:
            post = Post.objects.create(
                author=user,
                title=data['title'],
                content=data['content'],
                target=target,
                life_category=data.get('life_category')
            )

            # 多图上传
            images = request.FILES.getlist('images')
            for index, image in enumerate(images):
                PostImage.objects.create(
                    post=post,
                    image=image,
                    order=index
                )

            return Response({
                'code': 0,
                'message': 'post created',
                'data': {
                    'id': post.id,
                    'target': target
                }
            })

        # 发到问题追踪
        if target == 'issue':
            issue = Issue.objects.create(
                creator=user,
                title=data['title'],
                description=data['description'],
                location=data['location']
            )

            # 多图上传
            images = request.FILES.getlist('images')
            for index, image in enumerate(images):
                IssueImage.objects.create(
                    issue=issue,
                    image=image,
                    order=index
                )

            return Response({
                'code': 0,
                'message': 'issue created',
                'data': {
                    'id': issue.id,
                    'target': 'issue'
                }
            })