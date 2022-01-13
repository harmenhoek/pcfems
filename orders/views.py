from django.shortcuts import render
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, FormView
from django.utils.decorators import method_decorator
from orders.models import Order, OrderLog, OrderCategory, Ofi
from django.utils import timezone


@method_decorator(staff_member_required, name='dispatch')
class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders.html'
    ordering = ['-added_on']

class OrderCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Order
    template_name = 'order_form.html'
    success_message = "Order added successfully."
    fields = ['name', 'user', 'price', 'ofi', 'url', 'notes', 'approver', 'category']
    success_url = reverse_lazy('orders-home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = 'Add'
        return context

    def form_valid(self, form):
        form.instance.status = 1
        form.instance.added_on = timezone.now()
        form.instance.added_by = self.request.user
        return super().form_valid(form)