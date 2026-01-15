from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
