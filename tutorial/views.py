from .models import Tutorial
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


class TutorialMainView(ListView):
    model = Tutorial
    template_name = 'tutorial/tutorial_list.html'
    context_object_name = 'tutorials'
    ordering = ['-date_created']
    paginate_by = 5


class TutorialCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tutorial
    fields = ['title',  'prerequisites', 'description', 'data']
    success_message = "The tutorial has been successfully created."

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.save()
        return super(TutorialCreateView, self).form_valid(form)


class TutorialOverviewView(DetailView):
    model = Tutorial
    template_name = 'tutorial/tutorial_overview.html'


class TutorialDataView(DetailView):
    model = Tutorial
    template_name = 'tutorial/tutorial_data.html'


class TutorialUpdateView(SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Tutorial
    fields = ['title', 'prerequisites', 'description', 'data']
    success_message = "The tutorial has been successfully updated."

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(TutorialUpdateView, self).form_valid(form)

    def test_func(self):
        tutorial = self.get_object()
        if self.request.user == tutorial.creator:
            return True
        return False


class TutorialDeleteView(UserPassesTestMixin, DeleteView):
    model = Tutorial
    success_url = '/'
    success_message = 'The tutorial has been successfully deleted.'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(TutorialDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        tutorial = self.get_object()
        if self.request.user == tutorial.creator:
            return True
        return False
