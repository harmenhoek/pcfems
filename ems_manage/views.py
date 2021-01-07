from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ems.models import Item, Category, Flag, Lab, Setup, Cabinet
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from activity_log.models import ActivityLog


@staff_member_required
def manage(request):
    return render(request, 'ems_manage/manage.html')

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class UsersView(LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'ems_manage/user_list.html'  # Custom otherwise auth/user_list.html

    # def get_context_data(self, **kwargs): # to send extra data
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     logs = ActivityLog.objects.using('logs').all().order_by('-id')[:25]      # get from logs db  activity_log_activitylog: id, user_id, user, request_url, request_method, datetime, ip_address, extra_data, response_code
    #     context['logs'] = logs
    #     return context

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class UsersActivityView(LoginRequiredMixin, ListView):
    model = ActivityLog
    template_name = 'ems_manage/activity_list.html'
    paginate_by = 25
    ordering = ['-id']

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class FlagsView(LoginRequiredMixin, ListView):
    model = Flag  # TODO we also need Item later on to show al the current flagged items.
    template_name = 'ems_manage/flag_list.html'

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class FlagsCreateView(LoginRequiredMixin, CreateView):
    model = Flag
    success_url = reverse_lazy('manage-flags')
    fields = ['flag', 'description', 'icon']
    template_name = 'ems_manage/flag_form.html'

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class FlagsUpdateView(LoginRequiredMixin, UpdateView):
    model = Flag
    success_url = reverse_lazy('manage-flags')
    fields = ['flag', 'description', 'icon']
    template_name = 'ems_manage/flag_form.html'

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class CategoriesView(LoginRequiredMixin, ListView):
    model = Category  # TODO we also need Item later on to show al the current flagged items.
    template_name = 'ems_manage/category_list.html'

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class LocationsView(LoginRequiredMixin, ListView):
    model = Lab
    template_name = 'ems_manage/location_list.html'

    def get_context_data(self, **kwargs): # to send extra data
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        setups = Setup.objects.all()
        context['setups'] = setups
        cabinets = Cabinet.objects.all()
        context['cabinets'] = cabinets

        return context

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class SetupCreateView(LoginRequiredMixin, CreateView):
    model = Setup
    success_url = reverse_lazy('manage-locations')
    fields = ['lab', 'name', 'manager']
    template_name = 'ems_manage/setup_form.html'

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class SetupUpdateView(LoginRequiredMixin, UpdateView):
    model = Setup
    success_url = reverse_lazy('manage-locations')
    fields = ['lab', 'name', 'manager']
    template_name = 'ems_manage/setup_form.html'

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class LabCreateView(LoginRequiredMixin, CreateView):
    model = Lab
    success_url = reverse_lazy('manage-locations')
    fields = ['number', 'manager', 'nickname']
    template_name = 'ems_manage/lab_form.html'

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class LabUpdateView(LoginRequiredMixin, UpdateView):
    model = Lab
    success_url = reverse_lazy('manage-locations')
    fields = ['number', 'manager', 'nickname']
    template_name = 'ems_manage/lab_form.html'

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class CabinetCreateView(LoginRequiredMixin, CreateView):
    model = Cabinet
    success_url = reverse_lazy('manage-locations')
    fields = ['lab', 'number']
    template_name = 'ems_manage/cabinet_form.html'

class CabinetUpdateView(LoginRequiredMixin, UpdateView):
    model = Cabinet
    success_url = reverse_lazy('manage-locations')
    fields = ['lab', 'number']
    template_name = 'ems_manage/cabinet_form.html'

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    success_url = reverse_lazy('manage-categories')
    fields = ['name']
    template_name = 'ems_manage/category_form.html'

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    success_url = reverse_lazy('manage-categories')
    fields = ['name']
    template_name = 'ems_manage/category_form.html'

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class UserCreateView(LoginRequiredMixin, CreateView):
    model = get_user_model()
    success_url = reverse_lazy('manage-users')  # not even needed for CreateView
    fields = ['first_name', 'last_name', 'email', 'is_staff']
    template_name = 'ems_manage/user_form.html'

    def form_valid(self, form):
        form.instance.username = f"{form.instance.first_name.lower()}{form.instance.last_name.lower()}"
        return super(UserCreateView, self).form_valid(form)

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
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