from django.contrib.auth.models import AbstractUser
from django.db import models
from .problem import Problem

class User(AbstractUser):
    problems = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        null=True
    )
