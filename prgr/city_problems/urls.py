from django.urls import path
from django.views.generic import TemplateView, CreateView

from .views import ProblemListView, ProblemCreate
from .views import ContactView

urlpatterns = [
    path('', ProblemListView.as_view(), name='index_list'),
    path('about/', TemplateView.as_view(template_name="city_problems/problem_list.html")),
    path('contact/', ContactView.as_view(template_name="city_problems/contact.html")),
    path('add_problem/', ProblemCreate.as_view(template_name="city_problems/add_problem.html"))
]