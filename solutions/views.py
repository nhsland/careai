from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django import forms
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.conf import settings
from nbconvert import HTMLExporter
import nbformat

from .models import Challenge
from .models import Solution


def notebookconverthtml(nbfile):
    html_exporter = HTMLExporter()
    nb = nbformat.reads(nbfile.read(), as_version=4)
    (body, resources) = html_exporter.from_notebook_node(nb)
    htmlfile = nbfile.name.replace(".ipynb", ".html")
    html_file_writer = open(settings.MEDIA_ROOT + "/" + htmlfile, 'w')
    print(settings.MEDIA_ROOT + "/" + htmlfile)
    html_file_writer.write(body)
    html_file_writer.close()
    return htmlfile


class SolutionMainView(ListView):
    model = Solution
    template_name = 'solutions/solution_list.html'
    context_object_name = 'solutions'
    ordering = ['-date_created']
    paginate_by = 5


class SolutionDetailView(DetailView):
    model = Solution


class SolutionForm(forms.ModelForm):
    class Meta:
        model=Solution
        fields=['title', 'description', 'challenge', 'solution_notebook', 'solution_data']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        challengepk = kwargs.pop('challengepk')
        super(SolutionForm, self).__init__(*args, **kwargs)
        self.fields['challenge'].queryset = user.developer.challenge_set.all()
        if challengepk != "BasePage":
            self.fields['challenge'].initial = Challenge.objects.get(pk=challengepk)


class SolutionEvaluationForm(forms.ModelForm):
    class Meta:
        model=Solution
        fields=['title', 'description', 'challenge', 'solution_data', 'accuracy']

    def __init__(self, *args, **kwargs):
        super(SolutionEvaluationForm, self).__init__(*args, **kwargs)
        self.fields['title'].disabled = True
        self.fields['description'].disabled = True
        self.fields['challenge'].disabled = True
        self.fields['solution_data'].disabled = True


class SolutionCreateView(SuccessMessageMixin, CreateView):
    template_name = 'solutions/solution_form.html'
    form_class = SolutionForm
    success_message = "The solution has been successfully created."

    def get_form_kwargs(self):
        kwargs = super(SolutionCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['challengepk'] = self.kwargs['challengepk']
        return kwargs

    def form_valid(self, form):
        form.instance.developer = self.request.user.developer
        form.instance.solution_notebook_htmlver = notebookconverthtml(form.instance.solution_notebook)
        return super(SolutionCreateView, self).form_valid(form)


class SolutionUpdateView(SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Solution
    fields = ['title', 'description', 'solution_notebook', 'solution_data']
    success_message = "The solution has been successfully updated."

    def form_valid(self, form):
        form.instance.developer = self.request.user.developer
        form.instance.solution_notebook_htmlver = notebookconverthtml(form.instance.solution_notebook)
        return super(SolutionUpdateView, self).form_valid(form)

    def test_func(self):
        solution = self.get_object()
        try:
            if self.request.user.developer == solution.developer:
                return True
        except AttributeError:
            return False


class SolutionEvaluateView(UserPassesTestMixin, UpdateView):
    model = Solution
    template_name_suffix = "_evaluate_form"
    form_class = SolutionEvaluationForm

    def test_func(self):
        solution = self.get_object()
        try:
            if self.request.user.clinician == solution.challenge.clinician:
                return True
        except AttributeError:
            return False


class SolutionDeleteView(UserPassesTestMixin, DeleteView):
    model = Solution
    success_url = '/'
    success_message = 'The solution has been successfully deleted.'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(SolutionDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        solution = self.get_object()
        try:
            if self.request.user.developer == solution.developer:
                return True
        except AttributeError:
            return False
