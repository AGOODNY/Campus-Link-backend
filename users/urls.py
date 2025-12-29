from django.urls import path
from users.views.login import LoginView
from users.views.me import (
    MeView,
    MyViewHistoryView, MyPostListView
)
from post.views.view_history import PostViewRecordView, ViewHistoryListView


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('me/', MeView.as_view()),
    path('me/posts/', MyPostListView.as_view()),
    path('me/history/', MyViewHistoryView.as_view()),
    path('posts/<int:post_id>/view/', PostViewRecordView.as_view()),
    path('me/history/', ViewHistoryListView.as_view()),
]
