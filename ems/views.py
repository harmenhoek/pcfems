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

class ItemHistoryView(DetailView):
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

class ItemDetailView(DetailView):
    model = Item
    slug_url_kwarg = 'qrid'
    slug_field = 'qrid'

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
                fields_changed = []
                for idx, val in enumerate(delta.changes):
                    fields_changed.append(delta.changes[idx].field)
                all_delta.append(fields_changed)
            all_history.append(record)

        context['history'] = history
        context['zipped_allhistory_alldelta'] = zip(all_history, all_delta)

        return context

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

@method_decorator(staff_member_required, name='dispatch') #only staff can edit fully
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

@method_decorator(staff_member_required, name='dispatch') #only staff can edit fully
class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView): # TODO only for managers allow delete
    model = Item
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return True
        # if self.request.user == post.author:
        #     return True
        # return False

def about(request):
    return render(request, 'ems/about.html', {'title': 'About'})

def test(request):
    return render(request, 'ems/test.html')