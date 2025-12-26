from django.db import models
from django.conf import settings

class Issue(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('solved', 'Solved'),
    )

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# 发帖图片
class IssueImage(models.Model):
    issue = models.ForeignKey(
        Issue,
        related_name='issue_pic',   # 专用于“发帖图片”
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='issue/issue_pic/', null=True, blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

# 节点更新 tracking
class IssueNode(models.Model):
    issue = models.ForeignKey(
        Issue,
        related_name='nodes',       # “节点更新列表”
        on_delete=models.CASCADE
    )
    node_title = models.CharField(max_length=50)
    node_status = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='issue_nodes/', null=True, blank=True)
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.issue.title} - {self.node_title}"
