from django.db import models


class PushToken(models.Model):
    user_id = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=150, blank=True, null=True)

    token = models.TextField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.token