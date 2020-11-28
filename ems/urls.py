from django.urls import path
from . import views  # imports the functions from views.py
from .views import ItemListView, ItemDetailView, ItemCreateView, ItemStaffUpdateView, ItemUserUpdateView, ItemDeleteView, ItemHistoryView

urlpatterns = [
    path('', ItemListView.as_view(), name='ems-home'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    # path('', views.home , name='ems-home'), # '' means home page. views.home refers to the home function in views.urls, third is name
    path('item/new/', ItemCreateView.as_view(), name='item-create'),
    path('item/<int:pk>/staffupdate/', ItemStaffUpdateView.as_view(), name='item-staffupdate'),
    path('item/<int:pk>/update/', ItemUserUpdateView.as_view(), name='item-userupdate'),
    path('item/<int:pk>/delete/', ItemDeleteView.as_view(), name='item-delete'),
    path('item/<int:pk>/history/', ItemHistoryView.as_view(), name='item-history'),
    path('item/<slug:qrid>/', ItemDetailView.as_view(), name='item-detail'),
    path('about/', views.about, name='ems-about'),
    path('test/', views.test, name='ems-test'),
]

    # path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),