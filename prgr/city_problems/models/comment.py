from django.db import models

from .problem import Problem


class Comment(models.Model):
    date_created = models.DateTimeField()
    text = models.CharField(max_length=500)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.text}  {self.problem.short_name}"
