from django.db import models


class Status(models.Model):
    name = models.CharField(50)

    def __str__(self):
        return self.name
