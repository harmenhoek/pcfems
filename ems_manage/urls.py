from django.urls import path
from . import views  # imports the functions from views.py
from .views import UsersView, FlagsView, CategoriesView

urlpatterns = [
    path('', views.manage, name='manage-home'),
    path('user/', UsersView.as_view(), name='manage-users'),
    path('flags/', FlagsView.as_view(), name='manage-flags'),
    path('categories/', CategoriesView.as_view(), name='manage-categories'),
]

    # path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),