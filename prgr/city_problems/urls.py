from django.shortcuts import redirect
from django.urls import path, include
from django.views.generic import TemplateView, CreateView, RedirectView
import django.contrib.auth.urls
# noinspection PyUnresolvedReferences
from city_problems.views import test_request
from .cbv import *


app_name = 'city'

urlpatterns = [
    path('', ProblemListView.as_view(), name='index_list'),
    path('add_problem/', ProblemCreate.as_view(), name='create_problem'),
    path('profile/', UserProfile.as_view(), name='user_profile'),
    #path('logout/', ProblemListView.as_view(), name='tester'),
    path('problem/<int:pk>', ProblemDetail.as_view(), name='problem_detail'),
    path('problem/<int:pk>/update', ProblemUpdate.as_view(), name='problem_update'),
    path('problem/<int:pk>/delete', ProblemDelete.as_view(), name='problem_delete'),
    path('test/', test_request, name='test'),
    path('accounts/profile/', RedirectView.as_view(url='/', permanent=False)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('add-comment/', CommentCreate.as_view(), name='create-comment'),
    path('create-vote/', CreateVote.as_view(), name='create-vote')
]