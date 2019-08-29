from django.contrib.auth.models import AbstractUser
from django.db import models
from . import Problem

class User(AbstractUser):
    problems = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
    )
