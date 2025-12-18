from django.urls import path
from .views import UnifiedPostView

urlpatterns = [
    path('posts/', UnifiedPostView.as_view()),
]
