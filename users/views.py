from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileUpdateForm

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile
from ems.models import Item

# def register(request):
#    if request.method == 'POST':
#        form = UserCreationForm(request.POST)
#        if form.is_valid():
#            form.save()
#            username = form.cleaned_data.get('username')
#            messages.success(request, f'Account created for {username}!')
#            return redirect('ems-home')
#    else:
#        form = UserCreationForm()
#    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
   return render(request, 'users/profile.html')

@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)  # from users/models.py
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'users/user.html'

    def get_slug_field(self):
        """Get the name of a slug field to be used to look up by slug."""
        return 'user__username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Item.objects.filter(user__username=self.kwargs['slug'])
        return context
