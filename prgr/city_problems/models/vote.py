from django.conf import settings
from django.db import models

from prgr.city_problems.models import Problem


class Vote(models.Model):
    vote_date = models.DateTimeField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE())