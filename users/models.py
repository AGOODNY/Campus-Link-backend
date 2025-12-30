from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('staff', 'Staff'),
    )

    openid = models.CharField(max_length=64, unique=False, null=True, blank=True)
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='student'
    )

    avatar = models.ImageField(
        upload_to='avatar/',
        null=True,
        blank=True
    )
    nickname = models.CharField(
        max_length=50,
        blank=True
    )

    def save(self, *args, **kwargs):
        # 自动同步 Django 的 is_staff
        self.is_staff = (self.role == 'staff')
        super().save(*args, **kwargs)

