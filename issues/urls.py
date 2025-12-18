from django.urls import path
from .views import IssueNodeCreateView, IssueListView, MyIssuesView

urlpatterns = [
    path(
        'issues/<int:issue_id>/nodes/',
        IssueNodeCreateView.as_view()
    ),
    path('issues/', IssueListView.as_view()),
    path('issues/my/', MyIssuesView.as_view()),
]