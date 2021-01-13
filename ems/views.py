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
from .forms import ItemForm, AssignForm
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.forms import modelformset_factory

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.conf import settings

class ItemListView(LoginRequiredMixin, ListView):
   model = Item
   template_name = 'ems/home.html'  # <app>/<model>_<viewtype>.html
   ordering = ['-added_on']  # minus sign to get oldest first.

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

        # update last_scanned in model if refered from scanner
        from urllib import parse
        if parse.urlparse(self.request.META.get('HTTP_REFERER')).path == reverse('ems-scanner'):
            item = get_object_or_404(Item, pk=self.kwargs['pk'])
            item.last_scanned = timezone.now()
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

@login_required
def assignremove(request, pk):
    item = get_object_or_404(Item, pk=pk)
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
    item.save()
    return HttpResponseRedirect(reverse('item-detail', args=(pk,)))  # get pk from the url

class FlagCreateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Item
    success_message = "Item flagged as <b>%(flag)s</b> successfully."
    fields = ['flag']

@method_decorator(staff_member_required, name='dispatch') #only staff can edit fully
class ItemStaffUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    success_message = "Item <b>%(brand)s %(model)s (%(qrid)s)</b> was updated successfully."

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    # For ModelForms, if you need access to fields from the saved object override the get_success_message() method.
    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            model=self.object.model,
            brand=self.object.brand,
            qrid=self.object.qrid,
        )

class ItemUserUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Item
    success_message = "Item <b>%(brand)s %(model)s (%(qrid)s)</b> was updated successfully."
    fields = ['description', 'image', 'image2']

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

def about(request):
    return render(request, 'ems/about.html', {'title': 'About'})

@login_required
def test(request):
    return render(request, 'ems/test.html')

@login_required
def scanner(request):
    return render(request, 'ems/scanner.html')

# Regular function
def createqr(text):
    import qrcode
    from PIL import Image, ImageFont, ImageDraw, ImageOps
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=15,
        border=1,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    img = ImageOps.expand(img, border=(0, 0, 0, 60), fill='white')
    txt = Image.new("RGBA", img.size, (255, 255, 255, 0))

    # from django.conf.urls.static import static
    from django.templatetags.static import static
    fontfile = static('ems/Arial.ttf')

    # from django.contrib.staticfiles.storage import staticfiles_storage
    # fontfile = staticfiles_storage.url('ems/Arial.ttf')1
    font = ImageFont.truetype(fontfile, 60)
    d = ImageDraw.Draw(txt)
    d.text((img.size[0] / 2, img.size[1] - 10), text, anchor="ms", font=font, fill=(0, 0, 0, 256))
    out = Image.alpha_composite(img, txt)
    return out

@login_required
def qrgenerator(request, pk):
    item = get_object_or_404(Item, pk=pk)

    out = createqr(item.qrid)

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

    p = canvas.Canvas(buffer)

    for pk in range(pk1, pk2+1):
        try:
            item = get_object_or_404(Item, pk=pk)
            out = createqr(item.qrid)
            scale = 1
            (wdt, hgt) = (out.width // scale, out.height // scale)
            p.drawImage(ImageReader(out.resize((wdt, hgt))), 10, 10, mask='auto')
            scale = 2
            (wdt, hgt) = (out.width // scale, out.height // scale)
            p.drawImage(ImageReader(out.resize((wdt, hgt))), 10, hgt * 2 + 10, mask='auto')
            scale = 4
            (wdt, hgt) = (out.width // scale, out.height // scale)
            p.drawImage(ImageReader(out.resize((wdt, hgt))), 10, hgt * 6 + 10, mask='auto')
            scale = 6
            (wdt, hgt) = (out.width // scale, out.height // scale)
            p.drawImage(ImageReader(out.resize((wdt, hgt))), 10, hgt * 11 + 5, mask='auto')
            p.showPage()

        except:
            pass
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')