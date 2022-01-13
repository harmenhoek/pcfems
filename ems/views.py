from django.shortcuts import render
from .models import Lab, Cabinet, Setup, Item, Flag, Category, ItemLog
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin

# for using fnct-decorator as class decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
# for function-based views, decorator: staff_member_required @staff_member_required
from .forms import ItemForm, AssignForm, AddStorageLocationForm
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.utils import timezone
from django.forms import modelformset_factory

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.conf import settings
from django.db.models import Count

import os

from django.contrib.auth.decorators import permission_required

class ItemListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'ems/home.html'
    ordering = ['-added_on']  # minus sign to get oldest first.

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # history = Item.history.filter(id=item.id).order_by('history_id')
    #
    #     return context

    # def get_context_data(self, **kwargs):  # for showing a message after users login after an update. Not sure how to do this without get_context_data
    #     context = super().get_context_data(**kwargs)
    #
    #     global_preferences = global_preferences_registry.manager()
    #     if (global_preferences['message__afterupdate_message_on'] and self.request.user.preferences.update_message):
    #         messages.info(self.request, global_preferences['message__afterupdate_message'])
    #         self.request.user.profile.update_message = False
    #         self.request.user.profile.save()
    #     return context


class LocationListView(LoginRequiredMixin, ListView):
    model = Cabinet
    queryset = Cabinet.objects.annotate(
        num_items=Count('item')
    )
    template_name = 'ems/storage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['setups'] = Setup.objects.all()
        context['labs'] = Lab.objects.all()
        # context['items_count'] = Cabinet.objects.filter(storage_location=self.kwargs['pk']).count()
        return context

class CabinetDetailView(LoginRequiredMixin, DetailView):
    model = Cabinet
    template_name = 'ems/cabinet_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Item.objects.filter(storage_location=self.kwargs['pk']).filter(status=True)
        context['items_inuse'] = Item.objects.filter(storage_location=self.kwargs['pk']).filter(status=False)
        return context

@method_decorator(staff_member_required, name='dispatch')
class ItemHistoryView(LoginRequiredMixin, DetailView):
    model = Item
    template_name = 'ems/item_history.html'

    def get_context_data(self, **kwargs): # to send extra data
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)


        # Get all the changes of this specific item.
        # What we create: [HistoricalRecord, ModelDelta]
        # The length of historicalrecord is adapted here to the length of the modeldelta.
        # this is because record can have multiple modeldelta (fields that are changed). Each of these
        # modeldelta have the same history_user. To iterate over them in the template, we create a history
        # record array with the same length as modeldelta (thus duplicates if modeldelta>1).
        history = Item.history.filter(id=self.kwargs['pk'])
        all_delta = []
        all_history = [] #[-1] not supported in Django
        for record in history:
            if record.prev_record: #i.e. first record (add) is not included
                delta = record.diff_against(record.prev_record)
                # for idx, val in enumerate(delta.changes):
                #     delta.changes[idx].new = 'test'
                all_delta.append(delta)
                all_history.append(record)

        context['history'] = history
        context['zipped_allhistory_alldelta'] = zip(all_history, all_delta)

        return context

class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item
    slug_url_kwarg = 'qrid'
    slug_field = 'qrid'

    def get_context_data(self, **kwargs):  # to send extra data
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        try:
            item = get_object_or_404(Item, pk=self.kwargs['pk'])
        except:
            item = get_object_or_404(Item, qrid=self.kwargs['qrid'])

        if item.storage_location is None and item.status is True and item.tracking is True:
            messages.warning(self.request, f'Something is wrong with this item. It is not in use and no storage location is set. Please set a storage location, or contact a staff member.')

        if item.image2:
            context['total_images'] = 2
        else:
            context['total_images'] = 1

        # update last_scanned in model if referred from scanner
        # TODO this needs some updating, now everything is done inside the get_context_data function, which is not needed.

        version = self.request.GET.get('v', None)
        if version:
            item.last_scanned = timezone.now()
            item.save()

            if version == 'harmen':
                messages.success(self.request, f'You found a rabbithole! WoW! Congrats! This app is made by Harmen Hoek.')
            elif item.version != int(version):
                messages.warning(self.request, f'The scanned label is not up-to-date, a staff member is notified to replace this label.')
                if item.labelstatus is None:
                    item.labelstatus = timezone.now()
                    item.save()
            else:
                if item.labelstatus:  # label (assuming only 1 is around) is up to date.
                    item.labelstatus = None
                    item.save()



        # Get all the changes of this specific item.
        # What we create: [HistoricalRecord, ModelDelta]
        # The length of historicalrecord is adapted here to the length of the modeldelta.
        # this is because record can have multiple modeldelta (fields that are changed). Each of these
        # modeldelta have the same history_user. To iterate over them in the template, we create a history
        # record array with the same length as modeldelta (thus duplicates if modeldelta>1).

        # dirty solution below!
        try:
            history = Item.history.filter(id=self.kwargs['pk'])
        except:
            history = Item.history.filter(qrid=self.kwargs['qrid'])

        all_delta = []
        all_history = []  # [-1] not supported in Django
        for record in history:
            if record.prev_record:  # i.e. first record (add) is not included
                delta = record.diff_against(record.prev_record)
                fields_changed = []
                for idx, val in enumerate(delta.changes):
                    fields_changed.append(delta.changes[idx].field)
                all_delta.append(fields_changed)
            all_history.append(record)

        context['history'] = history
        context['zipped_allhistory_alldelta'] = zip(all_history, all_delta)


        # return all images
        try:
            image_list = Item.objects.get(pk=self.kwargs['pk']).images.all()
        except:
            image_list = Item.objects.get(qrid=self.kwargs['qrid']).images.all()

        context['image_list'] = image_list

        # return logs
        try:
            log_list = Item.objects.get(pk=self.kwargs['pk']).logs.all().order_by('-added_on')
        except:
            log_list = Item.objects.get(qrid=self.kwargs['qrid']).logs.all().order_by('-added_on')

        context['log_list'] = log_list

        context['DEFAULT_IMAGE'] = settings.DEFAULT_IMAGE

        # get flag history information  (adapted from ems_manage/views)
        if item.flag:
            import numpy as np
            id = item.id
            history = Item.history.filter(id=id).order_by('history_id')  # for each of these items, get full history
            flag_ids = [i.flag_id for i in history]  # get list of the flag_id of that item (eg. 2 4 4 4 4)
            history_ids = [i.history_id for i in history]  # get similar list with history_ids (unique)
            # get locations in flag_ids list where the flag_id changed, e.g. [2 4 4 3 3] will give [1 3], from that get
            # last one, thus [3] (most recent flag change, since we order by history_id)
            history_flagged_loc = np.where(np.roll(flag_ids, 1) != flag_ids)[0][-1]
            history_flagged_id = history_ids[history_flagged_loc]  # get corresponding history_id

            # since history_id is unique we can get corresponding history_user and history_date from history
            context['flagged_by'] = history.get(history_id=history_flagged_id).history_user
            context['flagged_on'] = history.get(history_id=history_flagged_id).history_date

        # context['cabinet'] = Cabinet.objects.filter(pk)
        return context

@method_decorator(staff_member_required, name='dispatch') #only staff can add new
class ItemCreateView(PermissionRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, CreateView):
    permission_required = 'users.is_itemmoderator'
    model = Item
    success_message = "Item <b>%(brand)s %(model)s (%(qrid)s)</b> was created successfully."
    form_class = ItemForm
    success_url = None

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)

    # For ModelForms, if you need access to fields from the saved object override the get_success_message() method.
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            model=self.object.model,
            brand=self.object.brand,
            qrid=self.object.qrid,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = 'Add'
        context['fieldtype'] = 'Item'
        return context

class LogCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = ItemLog
    success_message = "Log was added successfully."
    success_url = None
    fields = ['log', 'file1', 'file1_name', 'file2', 'file2_name']

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        item = get_object_or_404(Item, pk=self.kwargs['pk'])  # TODO FIX! No pk is sent to add.
        form.instance.item = item
        # form.instance.item = self.item.get_object()

        # form.instance.added_on = timezone.now()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = 'Add'
        return context

class LogUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ItemLog
    success_message = "Log was updated successfully."
    fields = ['log', 'file1', 'file1_name', 'file2', 'file2_name']

    def test_func(self):
        # log = get_object_or_404(ItemLog, pk=self.kwargs['pk'])  # can also be specific pk_2 eg when url has multiple
        log = self.get_object()
        # logger.error(f'CUSTOM log: {log}, pk_2: {self.kwargs["pk"]}, log.added_by: {log.added_by} == {self.request.user}, check: {self.request.user == log.added_by}')
        if self.request.user == log.added_by:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = 'Update'
        return context

class LogDeleteView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ItemLog
    success_message = "Log was deleted successfully."

    def get_success_url(self):
        item = self.object.item
        return reverse_lazy('item-detail', args=[str(item.pk)])

    def test_func(self):
        log = self.get_object()
        if self.request.user == log.added_by:
            return True
        return False

class AssignCreateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Item
    form_class = AssignForm  # needed to add date selector widget
    success_message = "Item <b>%(brand)s %(model)s (%(qrid)s)</b> was assigned to user <b>%(user)s</b> at location <b>%(location)s</b> successfully."
    template_name = 'ems/assign_create.html'

    def get_initial(self):
        return {'user': self.request.user}

    def form_valid(self, form):
        form.instance.status = False
        form.instance.date_inuse = timezone.now()
        return super().form_valid(form)

    # For ModelForms, if you need access to fields from the saved object override the get_success_message() method.
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            model=self.object.model,
            brand=self.object.brand,
            qrid=self.object.qrid,
            user=self.object.user,
            location=self.object.location,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = 'Update'
        return context




@login_required
def assignremove(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if item.storage_location is None:  # no storage location set, this must be done first before item can be stored.
        if request.method == 'POST':
            form = AddStorageLocationForm(request.POST)
            if form.is_valid():
                item.storage_location = form.cleaned_data['storage_location']
        else:
            form = AddStorageLocationForm()
            return render(request, 'ems/storagelocation_form.html', {'form': form})

    messages.warning(request, f'Item <b>{item.brand} {item.model}</b> (assigned to {item.user} at {item.location}) was <b>unassigned.</b> Make sure it is in storage cabinet <b>{item.storage_location}</b>.')
    item.status = True
    item.user = None
    item.date_return = timezone.now()
    item.save()

    return HttpResponseRedirect(reverse('item-detail', args=(pk,)))



@login_required
def flagremove(request, pk):
    item = get_object_or_404(Item, pk=pk)
    messages.success(request, f'Flag resolved.')
    item.flag = None
    item.flag_comment = None
    item.save()
    return HttpResponseRedirect(reverse('item-detail', args=(pk,)))  # get pk from the url

class FlagCreateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Item
    success_message = "Item flagged as <b>%(flag)s</b> successfully."
    fields = ['flag', 'flag_comment']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = 'Add'
        context['fieldtype'] = 'Flag'
        return context

@method_decorator(staff_member_required, name='dispatch') #only staff can edit fully
class ItemStaffUpdateView(PermissionRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'users.is_itemmoderator'
    model = Item
    form_class = ItemForm
    success_message = "Item <b>%(brand)s %(model)s (%(qrid)s)</b> was updated successfully."

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        if {'brand', 'model', 'serial', 'tracking', 'parts'}.intersection(set(form.changed_data)):
            form.instance.version = self.object.version + 1
            form.instance.labelstatus = timezone.now()
        if 'tracking' in form.changed_data:
            form.instance.user = None
            form.instance.date_inuse = None
            form.instance.status = True  # True = available / in storage
            form.instance.date_return = None
        return super().form_valid(form)

    # For ModelForms, if you need access to fields from the saved object override the get_success_message() method.
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            model=self.object.model,
            brand=self.object.brand,
            qrid=self.object.qrid,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = 'Update'
        context['fieldtype'] = 'Item'
        return context

class ItemUserUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Item
    success_message = "Item <b>%(brand)s %(model)s (%(qrid)s)</b> was updated successfully."
    fields = ['description', 'storage_location', 'image', 'image2']

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    # For ModelForms, if you need access to fields from the saved object override the get_success_message() method.
    def get_success_message(self, cleaned_data):  # TODO check if needed here. Prob not. 8-1-2021
        return self.success_message % dict(
            cleaned_data,
            model=self.object.model,
            brand=self.object.brand,
            qrid=self.object.qrid,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = 'Update'
        context['fieldtype'] = 'Item'
        return context


    # def test_func(self):
    #     post = self.get_object()
    #     if self.request.user == post.author:
    #         return True
    #     return False

@method_decorator(staff_member_required, name='dispatch') #only staff can edit fully
class ItemDeleteView(PermissionRequiredMixin, SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView): # TODO only for managers allow delete
    permission_required = 'users.is_itemmoderator'
    model = Item
    success_message = "Item <b>%(brand)s %(model)s (%(qrid)s)</b> was deleted successfully."
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return True
        # if self.request.user == post.author:
        #     return True
        # return False

@login_required
def test(request):
    return render(request, 'ems/test.html')

@login_required
def scanner(request):
    return render(request, 'ems/scanner.html')

def manual(request):
    file = os.path.join(settings.BASE_DIR, 'static/ems/manual.pdf')
    return FileResponse(open(file, 'rb'), content_type='application/pdf')
