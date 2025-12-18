from django.db import models
from django.conf import settings


class Issue(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('solved', 'Solved'),
    )

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#节点追踪，教职工可以更新问题解决节点
class IssueProgress(models.Model):
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name='progress_list'
    )

    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

#节点模型
class IssueNode(models.Model):
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name='nodes'
    )

    node_title = models.CharField(max_length=50)
    node_status = models.CharField(max_length=50)
    description = models.TextField()

    #节点图片
    image = models.ImageField(
        upload_to='issue_nodes/',
        null=True,
        blank=True
    )

    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.issue.title} - {self.node_title}"

