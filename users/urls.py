from django.urls import path
from users.views.login import LoginView
from users.views.me import (
    MeView,
    MyPostListView,
    MyViewHistoryView,
)


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('me/', MeView.as_view()),
    path('me/posts/', MyPostListView.as_view()),
    path('me/history/', MyViewHistoryView.as_view()),
]
