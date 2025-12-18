from django.urls import path
from post.views.post import PostListView, PostDetailView,LifePostSearchView, StudyPostSearchView
from post.views.comment import CommentListView, CommentCreateView
from post.views.like import PostLikeView

urlpatterns = [
    # 帖子
    path('posts/<str:target>/', PostListView.as_view()),
    path('post/<int:post_id>/', PostDetailView.as_view()),

    # 评论
    path('post/<int:post_id>/comments/', CommentListView.as_view()),
    path('post/<int:post_id>/comment/', CommentCreateView.as_view()),

    # 点赞
    path('post/<int:post_id>/like/', PostLikeView.as_view()),

    #搜索
    path('life/search/', LifePostSearchView.as_view()),
    path('study/search/', StudyPostSearchView.as_view()),
]