from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView, TemplateView
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required

from .models import User
from .forms import DeveloperRegisterForm, ClinicianRegisterForm, UserUpdateForm, ProfileUpdateForm
from challenges.models import Challenge


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    if request.user.is_developer:
        interests = request.user.developer.challenge_set.all()
    elif request.user.is_clinician:  # user is clinician
        interests = Challenge.objects.filter(clinician=request.user.clinician)
    else:
        interests = None
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'interests': interests,
        'req_user': request.user
    }
    return render(request, 'users/profile.html', context)


def specific_profile(request, username):
    user = User.objects.get(username=username)
    if user.is_developer:
        interests = user.developer.challenge_set.all()
    elif user.is_clinician:  # user is clinician
        interests = Challenge.objects.filter(clinician=user.clinician)
    else:
        interests = None
    return render(request, 'users/profile.html', {"req_user": user, "interests": interests})


class RegisterView(TemplateView):
    template_name = "users/register.html"


class DeveloperRegisterView(SuccessMessageMixin, CreateView):
    model = User
    form_class = DeveloperRegisterForm
    template_name = 'users/registration_form.html'
    success_message = "Successfully registered!"

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'developer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        user = form.save()
        return redirect('login')


class ClinicianRegisterView(SuccessMessageMixin, CreateView):
    model = User
    form_class = ClinicianRegisterForm
    template_name = 'users/registration_form.html'
    success_message = "Successfully registered! Please wait for authorisation."

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'clinician'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        user = form.save()
        return redirect('login')
