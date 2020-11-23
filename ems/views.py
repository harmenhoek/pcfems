from django.shortcuts import render
from .models import Lab, Cabinet, Setup, Item, Flag, Category
from django.http import HttpResponse

def home(request):
   content = {
       'posts': Item.objects.all()
   }
   return render(request, 'ems/home.html', content)


def about(request):
   return render(request, 'ems/about.html', {'title': 'About'})