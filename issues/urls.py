from django.urls import path
from .views import IssueCreateView,IssueNodeCreateView, IssueListView, MyIssuesView,IssueDetailView

urlpatterns = [
    path('issues/', IssueListView.as_view()),              # 列表
    path('issues/my/', MyIssuesView.as_view()),            # 我的问题
    path('issues/create/', IssueCreateView.as_view()),          #创建问题
    path('issues/<int:issue_id>/', IssueDetailView.as_view()),  # 详情
    path("issues/<int:issue_id>/nodes/", IssueNodeCreateView.as_view()), # 添加节点
]