from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm, HiddenInput
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, CreateView
from ..models import Vote

from django.http import HttpResponse, HttpResponseRedirect


class CreateVote(LoginRequiredMixin, CreateView):
    model = Vote
    http_method_names = ['post']
    fields = ['problem']
    def form_valid(self, form):
        self.success_url = reverse('city:problem_detail', kwargs={'pk': form.cleaned_data['problem'].id})
        if Vote.objects.filter(problem__id=form.cleaned_data['problem'].id, user__id=self.request.user.id).exists():
            return HttpResponseRedirect(reverse('city:problem_detail', kwargs={'pk': form.cleaned_data['problem'].id}))

        form.instance.vote_date = datetime.now()
        form.instance.user = self.request.user
        return super().form_valid(form)

class VoteForm(ModelForm):

    class Meta:
        model = Vote
        fields = ['problem']
        widgets = {
            'problem': HiddenInput()
        }