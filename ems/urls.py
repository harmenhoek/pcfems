from django.urls import path
from . import views  # imports the functions from views.py
from .views import ItemListView, ItemDetailView, ItemCreateView, ItemStaffUpdateView, ItemUserUpdateView, ItemDeleteView

urlpatterns = [
   path('', ItemListView.as_view(), name='ems-home'),
   path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),  # pk is primary key.
   # path('', views.home , name='ems-home'), # '' means home page. views.home refers to the home function in views.urls, third is name
    path('post/new/', ItemCreateView.as_view(), name='item-create'),
    path('post/<int:pk>/staffupdate/', ItemStaffUpdateView.as_view(), name='item-staffupdate'),  # pk is primary key.
    path('post/<int:pk>/update/', ItemUserUpdateView.as_view(), name='item-userupdate'),  # pk is primary key.
    path('post/<int:pk>/delete/', ItemDeleteView.as_view(), name='item-delete'),  # pk is primary key.
    path('about/', views.about, name='ems-about'),
]

# path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),