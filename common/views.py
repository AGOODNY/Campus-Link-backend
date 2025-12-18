from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from common.serializers import UnifiedPostSerializer
from issues.models import Issue
from post.models import Post


class UnifiedPostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UnifiedPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user = request.user
        target = data['target']

        if target in ['study', 'life']:
            post = Post.objects.create(
                author=user,
                title=data['title'],
                content=data['content'],
                target=target,
                life_category=data.get('life_category')
            )
            return Response({
                'code': 0,
                'message': 'post created',
                'data': {'id': post.id, 'target': target}
            })

        if target == 'issue':
            issue = Issue.objects.create(
                creator=user,
                title=data['title'],
                description=data['description'],
                location=data['location']
            )
            return Response({
                'code': 0,
                'message': 'issue created',
                'data': {'id': issue.id, 'target': 'issue'}
            })

