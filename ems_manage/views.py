from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ems.models import Item, Category, Flag
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

def manage(request):
    return render(request, 'ems_manage/manage.html')

class UsersView(ListView):
    model = get_user_model()
    template_name = 'ems_manage/user_list.html'  # Custom otherwise auth/user_list.html

class FlagsView(ListView):
    model = Flag  # TODO we also need Item later on to show al the current flagged items.
    template_name = 'ems_manage/flags_list.html'

class CategoriesView(ListView):
    model = Category  # TODO we also need Item later on to show al the current flagged items.
    template_name = 'ems_manage/categories_list.html'

class UserCreateView(LoginRequiredMixin, CreateView):
    model = get_user_model()
    success_url = reverse_lazy('manage-users')  # not even needed for CreateView
    fields = ['first_name', 'last_name', 'email', 'is_staff']
    template_name = 'ems_manage/user_form.html'

    def form_valid(self, form):
        form.instance.username = f"{form.instance.first_name.lower()}{form.instance.last_name.lower()}"
        return super(UserCreateView, self).form_valid(form)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()  # get_user_model() will work in more cases, when Auth model has changed. User will otherwise work.
    success_url = reverse_lazy('manage-users')  # not even needed for CreateView
    fields = ['first_name', 'last_name', 'email', 'is_staff', 'is_active']
    template_name = 'ems_manage/user_form.html'

    def form_valid(self, form):
        if (form.instance.is_superuser is False):  # TODO prevent edit of superuser find better way for this
            return super(UserUpdateView, self).form_valid(form)
        else:
            return HttpResponseRedirect(reverse('manage-users'))