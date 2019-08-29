from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from .models import Problem
from django.utils import timezone


class ProblemListView(ListView):

    model = Problem
    paginate_by = 100
    template_name = "city_problems/problem_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


from .forms import ContactForm
from django.views.generic.edit import FormView, CreateView


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)

class ProblemCreate(CreateView):
    model = Problem
    fields = ['short_name', 'description', 'image']