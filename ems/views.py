from django.shortcuts import render
from .models import Lab, Cabinet, Setup, Item, Flag, Category, ItemLog
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# for using fnct-decorator as class decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
# for function-based views, decorator: staff_member_required @staff_member_required
from .forms import ItemForm, AssignForm, AddStorageLocationForm
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.forms import modelformset_factory

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.conf import settings
from django.db.models import Count

import os

from django.contrib.staticfiles.views import serve

class ItemListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'ems/home.html'  # <app>/<model>_<viewtype>.html
    ordering = ['-added_on']  # minus sign to get oldest first.

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

        if item.storage_location is None and item.status is True:
            messages.warning(self.request, f'Something is wrong with this item. It is not in use and no storage location is set. Please set a storage location, or contact a staff member.')

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
        all_history = [] #[-1] not supported in Django
        for record in history:
            if record.prev_record: #i.e. first record (add) is not included
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
class ItemCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
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
    return HttpResponseRedirect(reverse('item-detail', args=(pk,)))  # get pk from the url


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
class ItemStaffUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    success_message = "Item <b>%(brand)s %(model)s (%(qrid)s)</b> was updated successfully."

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        if {'brand', 'model', 'serial', 'tracking', 'parts'}.intersection(set(form.changed_data)):
            form.instance.version = self.object.version + 1
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
class ItemDeleteView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView): # TODO only for managers allow delete
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
    return serve(request, file)

# Regular function
def createqr(qrid):
    import qrcode
    from PIL import Image, ImageFont, ImageDraw, ImageOps
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=15,
        border=1,
    )
    qr.add_data(qrid)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    img = ImageOps.expand(img, border=(0, 0, 0, 60), fill='white')
    txt = Image.new("RGBA", img.size, (255, 255, 255, 0))

    fontfile = os.path.join(settings.BASE_DIR, 'static/ems/Arial.ttf')
    font = ImageFont.truetype(fontfile, 30)

    d = ImageDraw.Draw(txt)
    d.text((img.size[0] / 2, img.size[1] - 10), qrid, anchor="ms", font=font, fill=(0, 0, 0, 256))
    out = Image.alpha_composite(img, txt)
    return out

def createqrv2(data, request):

    # settings

    label_height = 500
    label_width = 1250

    edge_padding = 30

    def x_percent(x):
        return x * ((label_width - label_height - edge_padding) / 100) + label_height

    def y_percent(y):
        return y * ((label_height - 2 * edge_padding) / 100) + edge_padding

    # x_percent = (label_width - label_height) / 100 + label_height
    # y_percent = label_height / 100



    import qrcode
    from PIL import Image, ImageFont, ImageDraw, ImageOps
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=20,  # 11 when url, 15 when just id
        border=1,
    )

    urlitem = reverse('item-detail', kwargs={'qrid': data['qrid']})
    urlhost = request.build_absolute_uri('/')
    urlfull = os.path.join(urlhost, *urlitem.split(os.sep))

    # just ID
    # qr.add_data(f"{data['qrid']}?v={data['version']}")
    # URL
    qr.add_data(f"{urlfull}?v={data['version']}")

    qr.make(fit=True)
    if data['tracking']:
        fillclr = "black"
        value = 'TRACK ITEM'
    else:
        fillclr = "black"
        value = 'NO TRACKING'
    img = qr.make_image(fill_color=fillclr, back_color="white").convert("RGBA")
    # img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

    img = img.resize((label_height, label_height))
    imgsize = img.size
    img = ImageOps.expand(img, border=(0, 0, label_width - label_height, 0), fill='white')
    txt = Image.new("RGBA", img.size, (255, 255, 255, 0))

    fontfile = os.path.join(settings.BASE_DIR, 'static/ems/Arial.ttf')

    d = ImageDraw.Draw(txt)

    def add_text(d, text, location, type, anchor='lm'):
        if type == 'title':
            fill = (0, 0, 0, 128)
            fontsize = 30
        elif type == 'field':
            fill = (0, 0, 0, 256)
            fontsize = 55
        elif type == 'mainfield':
            fill = (0, 0, 0, 256)
            fontsize = 90
        elif type == 'tracking':
            fill = (256, 0, 0, 256)
            fontsize = 55
        elif type == 'notracking':
            fill = (0, 0, 0, 128)
            fontsize = 55
        elif type == 'version':
            fill = (0, 0, 0, 128)
            fontsize = 15
        elif type == 'owner':
            fill = (0, 0, 0, 256)
            fontsize = 15

        return d.multiline_text(location, text, anchor=anchor, font=ImageFont.truetype(fontfile, fontsize), fill=fill)


    add_text(d, 'Item ID', (x_percent(0), y_percent(0)), 'title')
    add_text(d, data['qrid'], (x_percent(35), y_percent(17.5)), 'mainfield', anchor='mm')
    d.rectangle([(x_percent(0), y_percent(5)), (x_percent(70), y_percent(30))],
                fill=None, outline='black', width=3)

    if data['parts'] > 1:
        add_text(d, 'Part', (x_percent(80), y_percent(0)), 'title')
        add_text(d, f"{data['part']}/{data['parts']}", (x_percent(80), y_percent(17.5)), 'mainfield')

    add_text(d, 'Brand and model', (x_percent(0), y_percent(37.5)), 'title')
    add_text(d, f"{data['brand']} {data['model']}", (x_percent(0), y_percent(48.5)), 'field')

    add_text(d, 'Serial number', (x_percent(0), y_percent(60)), 'title')
    add_text(d, f"{data['serial']}", (x_percent(0), y_percent(71)), 'field')

    d.line([(x_percent(0), y_percent(80)), (x_percent(100), y_percent(80))], fill='black', width=3)
    if data['tracking']:
        add_text(d, 'TRACK ITEM', (x_percent(50), y_percent(95)), 'tracking', anchor='ms')
    else:
        add_text(d, 'NO TRACKING', (x_percent(50), y_percent(95)), 'notracking', anchor='ms')

    add_text(d, f"{data['printed']} ({data['version']})", (x_percent(100), y_percent(102.5)), 'version', anchor='rs')
    add_text(d, f"Property of Physics of Complex Fluids, University of Twente.", (x_percent(0), y_percent(102.5)), 'owner', anchor='ls')

    out = Image.alpha_composite(img, txt)
    return out

@login_required
def qrgenerator(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.GET.get('part'):
        part = request.GET.get('part')
    else:
        part = 1

    from datetime import date
    data = {
        'qrid': item.qrid,
        'parts': item.parts,
        'part': part,
        'tracking': item.tracking,
        'serial': item.serial,
        'brand': item.brand,
        'model': item.model,
        'title': item.title,
        'version': item.version,
        'storage': item.storage_location,
        'printed': date.today(),
    }
    out = createqrv2(data, request)

    response = HttpResponse(content_type='image/png')
    out.save(response, "PNG")

    return response

@login_required
def qrbatchgenerator(request, pk1, pk2):

    import io
    from django.http import FileResponse
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    buffer = io.BytesIO()
    from datetime import date

    from reportlab.lib.units import mm
    scale_factor = .36
    label_height = 500
    label_width = 1250
    pagesize = (label_width * scale_factor * mm, label_height * scale_factor * mm)
    p = canvas.Canvas(buffer, pagesize=pagesize)

    for pk in range(pk1, pk2+1):
        try:
            item = get_object_or_404(Item, pk=pk)

            for part in range(item.parts):
                data = {
                    'qrid': item.qrid,
                    'parts': item.parts,
                    'part': part+1,
                    'tracking': item.tracking,
                    'serial': item.serial,
                    'brand': item.brand,
                    'model': item.model,
                    'title': item.title,
                    'version': item.version,
                    'storage': item.storage_location,
                    'printed': date.today(),
                }
                out = createqrv2(data, request)

                scale = 1
                (wdt, hgt) = (out.width // scale, out.height // scale)
                p.drawImage(ImageReader(out.resize((wdt, hgt))), 10, 10, mask='auto')
                p.showPage()

        except:
            pass
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='qrcodes.pdf')