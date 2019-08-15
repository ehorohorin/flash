from django.urls import path
from django.views.generic import TemplateView

from .views import ProblemListView

urlpatterns = [
    path('', ProblemListView.as_view(), name='index_list'),
    path('about/', TemplateView.as_view(template_name="city_problems/problem_list.html")),
]