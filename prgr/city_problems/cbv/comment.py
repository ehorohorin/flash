from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views.generic import CreateView
# noinspection PyUnresolvedReferences
from city_problems.models import Comment

from django.forms import ModelForm, Textarea, models, HiddenInput


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['text', 'problem']
        widgets = {
            'text': Textarea(attrs={'cols': 100, 'rows': 4}),
            'problem': HiddenInput()
        }


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    http_method_names = ['post']
    fields = ['text', 'problem']

    def form_valid(self, form):
        self.success_url = reverse('city:problem_detail', kwargs={'pk':form.cleaned_data['problem'].id})
        form.instance.date_created = datetime.now()
        form.instance.user = self.request.user
        return super().form_valid(form)



