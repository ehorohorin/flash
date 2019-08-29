from django.conf import settings
from django.db import models

from .problem import Problem


class Vote(models.Model):
    vote_date = models.DateTimeField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.problem.short_name}  {self.user.name}"