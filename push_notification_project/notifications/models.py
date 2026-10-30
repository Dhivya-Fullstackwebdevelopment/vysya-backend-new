from django.db import models


class PushToken(models.Model):
    token = models.CharField(
        max_length=255,  # 22-la irundhu 255-ku mathunga
        unique=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.token