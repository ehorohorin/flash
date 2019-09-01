from django.db import models

from django.conf import settings
from django.urls import reverse

from .status import Status


class Problem(models.Model):
    creation_date = models.DateTimeField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    image = models.ImageField() #TODO production ready deployment - nginx
    short_name = models.CharField(max_length=140)
    description = models.CharField(max_length=3000)
    votes = models.ManyToManyField(settings.AUTH_USER_MODEL,through='Vote')


    class Meta:
        ordering = ['-creation_date']

    def __str__(self):
        return self.short_name

    def get_absolute_url(self):
        return reverse('city:problem_detail', kwargs={'pk': self.pk})