from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from .models import Problem
from django.utils import timezone


class ProblemListView(ListView):

    model = Problem
    paginate_by = 100
    template_name = "city_problems/problem_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


