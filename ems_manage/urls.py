from django.urls import path
from . import views  # imports the functions from views.py
from .views import UsersView, FlagsView, CategoriesView, UserCreateView, UserUpdateView, UsersActivityView

urlpatterns = [
    path('', views.manage, name='manage-home'),
    path('user/', UsersView.as_view(), name='manage-users'),
    path('user/add/', UserCreateView.as_view(), name='manage-users-add'),
    path('user/<int:pk>/update/', UserUpdateView.as_view(), name='manage-users-update'),
    path('flags/', FlagsView.as_view(), name='manage-flags'),
    path('categories/', CategoriesView.as_view(), name='manage-categories'),
    path('useractivity/', UsersActivityView.as_view(), name='manage-useractivity'),
]

    # path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),