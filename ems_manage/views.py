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
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class ManageView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'ems_manage/manage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['openflags'] = Item.objects.all().filter(flag__isnull=False)
        context['assgineditems'] = Item.objects.all().filter(status=False).order_by('date_return')
        context['warrantyitems'] = Item.objects.all().filter(warranty=True).order_by('warranty_expiration')
        context['scanneditems'] = Item.objects.all().order_by('last_scanned')[:100]
        return context

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
class FlagsCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Flag
    success_message = "Flag <b><i class='fas fa-%(icon)s'></i> %(flag)s</b> was created successfully."
    success_url = reverse_lazy('manage-flags')
    fields = ['flag', 'description', 'icon']
    template_name = 'ems_manage/flag_form.html'

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class FlagsUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Flag
    success_message = "Flag <b><i class='fas fa-%(icon)s'></i> %(flag)s</b> was updated successfully."
    success_url = reverse_lazy('manage-flags')
    fields = ['flag', 'description', 'icon']
    template_name = 'ems_manage/flag_form.html'

@staff_member_required
def flagresolve(request, pk):
    item = get_object_or_404(Item, pk=pk)
    messages.success(request, f'Item <b>{item.brand} {item.model}</b> (flagged as "<i class="fas fa-{item.flag.icon}"></i> {item.flag.flag}") was <b>unflagged</b>.')
    item.flag = None
    item.save()
    return HttpResponseRedirect(reverse('manage-home'))

@staff_member_required
def assignremove(request, pk):  # note that this function is similar to assignremove in ems/views, but with different response. In future combine.
    item = get_object_or_404(Item, pk=pk)
    messages.success(request, f'Item <b>{item.brand} {item.model}</b> (assigned to {item.user} at {item.location}) was <b>unassigned.</b> Make sure it is in storage cabinet <b>{item.storage_location}</b>.')
    item.status = True
    item.user = None
    item.date_return = timezone.now()
    item.save()
    return HttpResponseRedirect(reverse('manage-home'))

@staff_member_required
def warrantyremove(request, pk):  # note that this function is similar to assignremove in ems/views, but with different response. In future combine.
    item = get_object_or_404(Item, pk=pk)
    messages.success(request, f'The warranty of item <b>{item.brand} {item.model}</b> (warranty till {item.warranty_expiration}) was <b>removed</b>.')
    item.warranty = False
    item.warranty_expiration = None
    item.next_service_date = None
    item.save()
    return HttpResponseRedirect(reverse('manage-home'))

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
class SetupCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Setup
    success_message = "Setup <b>%(lab)s - %(name)s</b> was created successfully."
    success_url = reverse_lazy('manage-locations')
    fields = ['lab', 'name', 'manager']
    template_name = 'ems_manage/setup_form.html'

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class SetupUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Setup
    success_message = "Setup <b>%(lab)s - %(name)s</b> was updated successfully."
    success_url = reverse_lazy('manage-locations')
    fields = ['lab', 'name', 'manager']
    template_name = 'ems_manage/setup_form.html'

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class LabCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Lab
    success_message = "Lab <b>%(number)s (%(nickname)s)</b> was created successfully."
    success_url = reverse_lazy('manage-locations')
    fields = ['number', 'manager', 'nickname']
    template_name = 'ems_manage/lab_form.html'

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class LabUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Lab
    success_message = "Lab <b>%(number)s (%(nickname)s)</b> was updated successfully."
    success_url = reverse_lazy('manage-locations')
    fields = ['number', 'manager', 'nickname']
    template_name = 'ems_manage/lab_form.html'

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class CabinetCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Cabinet
    success_message = "Cabinet <b>%(number)s</b> in lab %(lab)s was created successfully."
    success_url = reverse_lazy('manage-locations')
    fields = ['lab', 'number']
    template_name = 'ems_manage/cabinet_form.html'

class CabinetUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Cabinet
    success_message = "Cabinet <b>%(number)s</b> in lab %(lab)s was updated successfully."
    success_url = reverse_lazy('manage-locations')
    fields = ['lab', 'number']
    template_name = 'ems_manage/cabinet_form.html'

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class CategoryCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Category
    success_message = "Category <b>%(name)s</b> was created successfully."
    success_url = reverse_lazy('manage-categories')
    fields = ['name']
    template_name = 'ems_manage/category_form.html'

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class CategoryUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Category
    success_message = "Category <b>%(name)s</b> was updated successfully."
    success_url = reverse_lazy('manage-categories')
    fields = ['name']
    template_name = 'ems_manage/category_form.html'

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class UserCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = get_user_model()
    success_message = "User <b>%(first_name)s %(last_name)s (%(email)s)</b> was created successfully."
    success_url = reverse_lazy('manage-users')  # not even needed for CreateView
    fields = ['first_name', 'last_name', 'email', 'is_staff']
    template_name = 'ems_manage/user_form.html'

    def form_valid(self, form):
        form.instance.username = f"{form.instance.first_name.lower()}{form.instance.last_name.lower()}"
        return super(UserCreateView, self).form_valid(form)

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class UserUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = get_user_model()  # get_user_model() will work in more cases, when Auth model has changed. User will otherwise work.
    success_message = "User <b>%(first_name)s %(last_name)s (%(email)s)</b> was updated successfully."
    success_url = reverse_lazy('manage-users')  # not even needed for CreateView
    fields = ['first_name', 'last_name', 'email', 'is_staff', 'is_active']
    template_name = 'ems_manage/user_form.html'

    def form_valid(self, form):
        if (form.instance.is_superuser is False):  # TODO prevent edit of superuser find better way for this
            return super(UserUpdateView, self).form_valid(form)
        else:
            return HttpResponseRedirect(reverse('manage-users'))