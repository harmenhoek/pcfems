from django.urls import path
from . import views  # imports the functions from views.py

urlpatterns = [
   path('', views.home , name='ems-home'), # '' means home page. views.home refers to the home function in views.urls, third is name
]
