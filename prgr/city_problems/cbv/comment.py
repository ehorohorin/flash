from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views.generic import CreateView
# noinspection PyUnresolvedReferences
from city_problems.models import Comment


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    http_method_names = ['post']
    fields = ['text', 'problem']

    def form_valid(self, form):
        self.success_url = reverse('city:problem_detail', kwargs={'pk':form.cleaned_data['problem'].id})
        form.instance.date_created = datetime.now()
        return super().form_valid(form)



