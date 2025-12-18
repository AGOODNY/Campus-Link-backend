from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Issue, IssueNode
from .serializers import IssueNodeSerializer,IssueListSerializer

class IssueNodeCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, issue_id):
        user = request.user

        # 只有staff可以更新节点
        if not user.is_staff:
            return Response(
                {"detail": "Only staff can update issue nodes"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            issue = Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            return Response({"detail": "Issue not found"}, status=404)

        # 如果 Issue 已完成，禁止再更新
        if issue.status == 'solved':
            return Response(
                {"detail": "Issue is already completed"},
                status=400
            )

        serializer = IssueNodeSerializer(data=request.data)
        if serializer.is_valid():
            node_status = serializer.validated_data['node_status']

            IssueNode.objects.create(
                issue=issue,
                node_title=serializer.validated_data['node_title'],
                node_status=node_status,
                description=serializer.validated_data['description'],
                image=serializer.validated_data.get('image'),
                operator=user
            )

            # 自动更新 Issue 状态
            if node_status == '已完成':
                issue.status = 'solved'
            else:
                issue.status = 'processing'

            issue.save()

            return Response({"detail": "Node added"}, status=201)

        return Response(serializer.errors, status=400)

class IssueListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        issues = Issue.objects.all().order_by('-created_at')
        serializer = IssueListSerializer(issues, many=True)
        return Response(serializer.data)

#顶部显示我的问题--我发布的问题
class MyIssuesView(APIView):
    permission_classes = [IsAuthenticated]  # 必须登录

    def get(self, request):
        user = request.user
        my_issues = Issue.objects.filter(creator=user).order_by('-created_at')  # 按时间倒序
        serializer = IssueListSerializer(my_issues, many=True)
        return Response(serializer.data)