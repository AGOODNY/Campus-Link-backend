from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from common.serializers import UnifiedPostSerializer
from issues.models import Issue, IssueImage
from post.models import Post, PostImage

class UnifiedPostView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = UnifiedPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user = request.user
        target = data['target']

        # 生活区 / 学习区
        if target in ['study', 'life']:
            post = Post.objects.create(
                author=user,
                title=data['title'],
                content=data['content'],
                target=target,
                life_category=data.get('life_category')
            )

            image = request.FILES.get("image")
            if image:
                PostImage.objects.create(post=post, image=image)

            return Response({"detail": "created", "id": post.id}, status=201)

        # 问题追踪区（Issue）
        if target == 'issue':
            issue = Issue.objects.create(
                creator=user,
                title=data['title'],
                description=data['description'],
                status="pending"
            )

            image = request.FILES.get("image")
            if image:
                IssueImage.objects.create(issue=issue, image=image, order=0)

            return Response({"detail": "created", "id": issue.id}, status=201)
