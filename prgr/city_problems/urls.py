from django.urls import path
from django.views.generic import TemplateView, CreateView


from .cbv import *


app_name = 'city'

urlpatterns = [
    path('', ProblemListView.as_view(), name='index_list'),
    path('add_problem/', ProblemCreate.as_view(), name='create_problem'),
    path('profile/', ProblemListView.as_view(), name='user_profile'),
    path('logout/', ProblemListView.as_view(), name='logout'),
    path('problem/<int:pk>', ProblemDetail.as_view(), name='problem_detail'),
    path('problem/<int:pk>/update', ProblemUpdate.as_view(), name='problem_update'),
    path('problem/<int:pk>/delete', ProblemDelete.as_view(), name='problem_delete')
]