from django.urls import path
from . import views
from .views import OrderListView, OrderCreateView

urlpatterns = [
    path('', OrderListView.as_view(), name='orders-home'),
    path('new/', OrderCreateView.as_view(), name='order-create'),
]