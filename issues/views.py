from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Issue, IssueNode
from .serializers import IssueNodeSerializer, IssueListSerializer, IssueDetailSerializer

class IssueNodeCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, issue_id):
        user = request.user
        if not user.is_staff:
            return Response({"detail": "Only staff can update issue issue_pic"}, status=403)

        try:
            issue = Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            return Response({"detail": "Issue not found"}, status=404)

        if issue.status == 'solved':
            return Response({"detail": "Issue is already completed"}, status=400)

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
            issue.status = "solved" if node_status == "已完成" else "processing"
            issue.save()
            return Response({"detail": "Node added"}, status=201)
        return Response(serializer.errors, status=400)

class IssueListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        issues = Issue.objects.all().order_by('-created_at')
        serializer = IssueListSerializer(issues, many=True)
        return Response(serializer.data)

class MyIssuesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        my_issues = Issue.objects.filter(creator=request.user).order_by('-created_at')
        serializer = IssueListSerializer(my_issues, many=True)
        return Response(serializer.data)

class IssueDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, issue_id):
        try:
            issue = Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            return Response({"detail":"Issue not found"}, status=404)
        serializer = IssueDetailSerializer(issue, context={"request": request})   # FIX HERE
        return Response(serializer.data, status=200)
