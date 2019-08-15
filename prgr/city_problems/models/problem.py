from django.db import models

from django.conf import settings


class Problem(models.Model):
    creation_date = models.DateField()
    status = models.CharField(max_length=20)
    image = models.ImageField()
    short_name = models.CharField(max_length=140)
    description = models.CharField(max_length=3000)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.short_name