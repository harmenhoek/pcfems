from django.urls import path
from . import views  # imports the functions from views.py
from .views import ItemListView, ItemDetailView, ItemCreateView, ItemStaffUpdateView, ItemUserUpdateView, \
    ItemDeleteView, ItemHistoryView, AssignCreateView, LogCreateView, LogUpdateView, LogDeleteView

urlpatterns = [
    path('', ItemListView.as_view(), name='ems-home'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    # path('', views.home , name='ems-home'), # '' means home page. views.home refers to the home function in views.urls, third is name
    path('item/new/', ItemCreateView.as_view(), name='item-create'),
    path('item/<int:pk>/staffupdate/', ItemStaffUpdateView.as_view(), name='item-staffupdate'),
    path('item/<int:pk>/update/', ItemUserUpdateView.as_view(), name='item-userupdate'),
    path('item/<int:pk>/delete/', ItemDeleteView.as_view(), name='item-delete'),
    path('item/<int:pk>/history/', ItemHistoryView.as_view(), name='item-history'),
    path('item/<int:pk>/assign/new', AssignCreateView.as_view(), name='item-assign'),
    path('item/<int:pk>/assign/remove', views.assignremove, name='item-assign-remove'),
    # path('item/<int:pk>/log/new/', LogCreateView.as_view() , name='item-log-create'),
    # path('item/<int:pk>/log/<int:pk_2>/update/', LogUpdateView.as_view() , name='item-log-update'), #                             <a class="btn btn-secondary btn-sm mt-1 mb-1" href="{% url  'item-log-update' object.id log.id %}">Update</a>
    # path('item/<int:pk>/log/<int:pk_2>/delete/', LogDeleteView.as_view() , name='item-log-delete'),
    path('item/<int:pk>/log/new/', LogCreateView.as_view(), name='item-log-create'),
    path('log/<int:pk>/update/', LogUpdateView.as_view(), name='item-log-update'),
    path('log/<int:pk>/delete/', LogDeleteView.as_view(), name='item-log-delete'),
    path('item/<slug:qrid>/', ItemDetailView.as_view(), name='item-detail'),
    path('about/', views.about, name='ems-about'),
    path('test/', views.test, name='ems-test'),
    path('scanner/', views.scanner, name='ems-scanner'),
    path('qrgenerator/<int:pk>/', views.qrgenerator, name='ems-qrgenerator'),
    path('qrbatchgenerator/<int:pk1>/<int:pk2>/', views.qrbatchgenerator, name='ems-qrbatchgenerator'),
]

    # path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),