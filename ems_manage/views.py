from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ems.models import Item, Category, Flag

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
