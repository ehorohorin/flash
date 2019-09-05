from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from ..models import Comment
from ..models import Problem
from ..models import Vote


class UserProfile(LoginRequiredMixin, ListView):
    context_object_name = 'problems'
    template_name = 'city_problems/user_profile.html'
    def get_queryset(self):
        return Problem.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(user=self.request.user)
        context['votes'] = Vote.objects.filter(user=self.request.user)
        return context
