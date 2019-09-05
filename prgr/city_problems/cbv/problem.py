from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

# noinspection PyUnresolvedReferences
from city_problems.models import Comment

# noinspection PyUnresolvedReferences
from city_problems.cbv.comment import CommentForm
# noinspection PyUnresolvedReferences
from city_problems.cbv.vote import VoteForm

from ..models import Vote
from ..models import Status
from ..models import Problem

class ProblemListView(ListView):
    model = Problem


class ProblemCreate(LoginRequiredMixin, CreateView):
    model = Problem
    fields = ['short_name', 'description', 'image']
    template_name = "city_problems/add_problem.html"

    def form_valid(self, form):
        form.instance.creation_date = datetime.now()
        form.instance.user = self.request.user
        form.instance.status = Status.objects.filter(name='Открыто').first()
        return super().form_valid(form)


class ProblemDetail(DetailView):
    model = Problem

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(problem__id=self.kwargs['pk'])
        context['comment_form'] = CommentForm(initial={'problem':self.kwargs['pk']})
        if Vote.objects.filter(problem__id=self.kwargs['pk'], user__id=self.request.user.id).exists():
            context['vote_form'] = VoteForm()
            context['vote_exists'] = True
        else:
            context['vote_form'] = VoteForm(initial={'problem': self.kwargs['pk']})
            context['vote_exists'] = False
        context['votes'] = Vote.objects.filter(problem__id=self.kwargs['pk'])
        return context

class ProblemUpdate(LoginRequiredMixin, UpdateView):
    model = Problem
    fields = ['short_name', 'description', 'image', 'status', 'creation_date']

class ProblemDelete(LoginRequiredMixin, DeleteView):
    model = Problem
    success_url = reverse_lazy('city:index_list')
