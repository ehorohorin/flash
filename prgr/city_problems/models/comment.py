from django.db import models

from prgr.city_problems.models import Problem


class Comment(models.Model):
    date_created = models.DateTimeField()
    text = models.CharField(500)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
