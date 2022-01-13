from django.urls import path
from . import views  # imports the functions from views.py
from .views import UsersView, FlagsView, CategoriesView, UserCreateView, UserUpdateView, UsersActivityView, \
    CategoryCreateView, CategoryUpdateView, FlagsCreateView, FlagsUpdateView, LabCreateView, \
    LabUpdateView, SetupCreateView, SetupUpdateView, CabinetCreateView, CabinetUpdateView, ManageView, ManageViewNew, \
    Settings, LabView, SetupView, CabinetView, OverviewOpenFlags, OverviewAssignedItems, OverviewItemsWarranty, \
    CheckDetailView, CheckAssignCreateView

urlpatterns = [
    path('', ManageView.as_view(), name='manage-home'),
    path('new', ManageViewNew.as_view(), name='managenew-home'),

    path('overview/openflags/', OverviewOpenFlags.as_view(), name='manage-overview-openflags'),
    path('overview/assigneditems/', OverviewAssignedItems.as_view(), name='manage-overview-assigneditems'),
    path('overview/itemswarranty/', OverviewItemsWarranty.as_view(), name='manage-overview-itemswarranty'),

    path('user/', UsersView.as_view(), name='manage-users'),
    path('user/add/', UserCreateView.as_view(), name='manage-users-add'),
    path('user/<int:pk>/update/', UserUpdateView.as_view(), name='manage-users-update'),

    path('flags/', FlagsView.as_view(), name='manage-flags'),
    path('flags/add/', FlagsCreateView.as_view(), name='manage-flags-add'),
    path('flags/<int:pk>/update/', FlagsUpdateView.as_view(), name='manage-flags-update'),

    path('categories/', CategoriesView.as_view(), name='manage-categories'),
    path('categories/add/', CategoryCreateView.as_view(), name='manage-categories-add'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='manage-categories-update'),

    path('useractivity/', UsersActivityView.as_view(), name='manage-useractivity'),

    path('lab/', LabView.as_view(), name='manage-labs'),
    path('lab/add/', LabCreateView.as_view(), name='manage-labs-add'),
    path('lab/<int:pk>/update/', LabUpdateView.as_view(), name='manage-labs-update'),

    path('setup/', SetupView.as_view(), name='manage-setups'),
    path('setup/add/', SetupCreateView.as_view(), name='manage-setups-add'),
    path('setup/<int:pk>/update/', SetupUpdateView.as_view(), name='manage-setups-update'),

    path('cabinet/', CabinetView.as_view(), name='manage-cabinets'),
    path('cabinet/add/', CabinetCreateView.as_view(), name='manage-cabinets-add'),
    path('cabinet/<int:pk>/update/', CabinetUpdateView.as_view(), name='manage-cabinets-update'),

    path('flags/<int:pk>/resolve/', views.flagresolve, name='manage-flags-resolve'),
    path('item/<int:pk>/assign/remove/', views.assignremove, name='manage-assign-remove'),
    path('item/<int:pk>/warranty/remove/', views.warrantyremove, name='manage-warranty-remove'),

    path('export/', views.export, name='manage-export'),
    path('export_single/<int:pk>/', views.export_single, name='manage-export-single'),
    path('export_outdated/<int:track>/', views.export_outdated, name='manage-export-outdated'),
    path('settings/', Settings.as_view(), name='manage-settings'),

    path('check/', CheckDetailView.as_view(), name='manage-check'),
    path('item/<int:pk>/assign/remove', views.check_assignremove, name='manage-check-item-assign-remove'),
    path('item/<int:pk>/verify', views.check_verify, name='manage-check-item-verify'),
    path('item/<int:pk>/verify', views.check_verify, name='manage-check-item-verify'),
    path('item/<int:pk>/assign/new', CheckAssignCreateView.as_view(), name='manage-check-item-assign'),
]