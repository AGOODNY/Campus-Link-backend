from django.db import models
from django.conf import settings


class Post(models.Model):
    TARGET_CHOICES = (
        ('study', 'Study'),
        ('life', 'Life'),
    )

    LIFE_CATEGORY_CHOICES = (
        ('return_school', 'Alumni Corner'),
        ('campus_life', 'On Campus'),
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)
    content = models.TextField()

    # 决定发到哪个区
    target = models.CharField(
        max_length=10,
        choices=TARGET_CHOICES
    )

    # 只给生活区用
    life_category = models.CharField(
        max_length=20,
        choices=LIFE_CATEGORY_CHOICES,
        null=True,
        blank=True
    )

    # 统计字段
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

#图片模型
class PostImage(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(upload_to='post/images/')
    order = models.IntegerField(default=0)  # 第几张图（可选）

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Image of post {self.post.id}'

#点赞模型
class PostLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

#评论模型
class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

#浏览记录模型
class PostViewHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='view_history'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']
        unique_together = ('user', 'post')