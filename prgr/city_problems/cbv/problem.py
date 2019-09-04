from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

# noinspection PyUnresolvedReferences
from city_problems.models import Comment
from ..models import Problem

class ProblemListView(ListView):

    model = Problem
 #   template_name = "city_problems/problem_list.html"

class ProblemCreate(LoginRequiredMixin, CreateView):
    model = Problem
    fields = ['short_name', 'description', 'image', 'status']
    template_name = "city_problems/add_problem.html"

    def form_valid(self, form):
        form.instance.creation_date = datetime.now()
        return super().form_valid(form)

#добавить форму в view
#форма добавления коментария
# в action прописать адрес view для добавления коментария. CommentCreate, get - None
# в ProblemDetail добавить обвес для создания коментария
    # код форма от модели, миксин для создания коментария?
from django.forms import ModelForm, Textarea, models, HiddenInput


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['text', 'problem']
        widgets = {
            'text': Textarea(attrs={'cols': 100, 'rows': 4}),
            'problem': HiddenInput()
        }



class ProblemDetail(DetailView):
    model = Problem

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['comments'] = Comment.objects.filter(problem__id=self.kwargs['pk'])
        context['form'] = CommentForm(initial={'problem':self.kwargs['pk']})
        return context

class ProblemUpdate(LoginRequiredMixin, UpdateView):
    model = Problem
    fields = ['short_name', 'description', 'image', 'status', 'creation_date']

class ProblemDelete(LoginRequiredMixin, DeleteView):
    model = Problem
    success_url = reverse_lazy('city:index_list')
