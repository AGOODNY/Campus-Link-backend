from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Issue, IssueNode, IssueImage
from .serializers import IssueNodeSerializer, IssueListSerializer, IssueDetailSerializer

class IssueNodeCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, issue_id):
        user = request.user
        if not user.is_staff:
            return Response({"detail": "Permission denied"}, status=403)

        try:
            issue = Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)

        node_title = request.data.get("node_title", "").strip()
        description = request.data.get("description", "").strip()
        image = request.FILES.get("image")

        # 节点状态逻辑: pending -> accepted -> resolved
        if issue.status == "pending":
            new_status = "accepted"
        elif issue.status == "accepted":
            new_status = "resolved"
        else:
            return Response({"detail": "Already resolved"}, status=400)

        node = IssueNode.objects.create(
            issue=issue,
            node_title=node_title,
            node_status=new_status,
            description=description,
            image=image,
            operator=user
        )

        issue.status = new_status
        issue.save(update_fields=["status"])

        serializer = IssueDetailSerializer(issue, context={"request": request})
        return Response(serializer.data, status=201)

class IssueListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        issues = Issue.objects.all().order_by('-created_at')
        serializer = IssueListSerializer(issues, many=True, context={"request": request})
        return Response(serializer.data)

class MyIssuesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        my_issues = Issue.objects.filter(creator=request.user).order_by('-created_at')
        serializer = IssueListSerializer(my_issues, many=True, context={"request": request})
        return Response(serializer.data)

class IssueDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, issue_id):
        try:
            issue = Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            return Response({"detail":"Issue not found"}, status=404)
        serializer = IssueDetailSerializer(issue, context={"request": request})
        return Response(serializer.data, status=200)

class IssueCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        user = request.user
        title = request.data.get("title", "")
        description = request.data.get("description", "")

        if not description:
            return Response({"detail": "description required"}, status=400)

        issue = Issue.objects.create(
            creator=user,
            title=title if title else "未命名问题",
            description=description,
            status="pending"
        )

        files = request.FILES.getlist("images")
        for i, f in enumerate(files):
            IssueImage.objects.create(
                issue=issue,
                image=f,
                order=i,
            )

        return Response({"id": issue.id, "detail": "created"}, status=201)

    class IssueImageUploadView(APIView):
        permission_classes = [IsAuthenticated]
        parser_classes = [MultiPartParser, FormParser]

        def post(self, request, issue_id):
            try:
                issue = Issue.objects.get(id=issue_id)
            except Issue.DoesNotExist:
                return Response({"detail": "Issue not found"}, status=404)

            file = request.FILES.get("image")
            order = request.data.get("order", 0)
            IssueImage.objects.create(issue=issue, image=file, order=order)
            return Response({"detail": "uploaded"}, status=201)
