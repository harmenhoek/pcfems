from django.shortcuts import render
from .models import Lab, Cabinet, Setup, Item, Flag, Category
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# for using fnct-decorator as class decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
# for function-based views, decorator: staff_member_required @staff_member_required

# @login_required
# def home(request):
#    content = {
#        'posts': Item.objects.all()
#    }
#    return render(request, 'ems/home.html', content)


def about(request):
   return render(request, 'ems/about.html', {'title': 'About'})

class ItemListView(ListView):
   model = Item
   template_name = 'ems/home.html'  # <app>/<model>_<viewtype>.html
   ordering = ['-added_on']  # minus sign to get oldest first.


class ItemDetailView(DetailView):
   model = Item

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    # form_class = ItemForm
    # fields = ['title', 'content']
    # fields = '__all__'
    fields = ['brand', 'model', 'serial', 'category', 'description', 'purchased_by', 'purchased_on', 'purchased_price', 'storage_location', 'image']
    # no need to add template_name since we use default names django expects.

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class ItemStaffUpdateView(LoginRequiredMixin, UpdateView): # TODO different update views for general users and managers. UserPassesTestMixin
    model = Item
    fields = ['brand', 'model', 'serial', 'category', 'description', 'purchased_by', 'purchased_on', 'purchased_price',
              'storage_location', 'image']

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class ItemUserUpdateView(LoginRequiredMixin, UpdateView): # TODO different update views for general users and managers. UserPassesTestMixin
    model = Item
    fields = ['description', 'flag', 'image']

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    # def test_func(self):
    #     post = self.get_object()
    #     if self.request.user == post.author:
    #         return True
    #     return False

class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): # TODO only for managers allow delete
    model = Item
    success_url = '/'

    # def test_func(self):
    #     post = self.get_object()
    #     if self.request.user == post.author:
    #         return True
    #     return False

def about(request):
    return render(request, 'ems/about.html', {'title': 'About'})

def test(request):
    return render(request, 'ems/test.html')