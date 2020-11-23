from django.contrib import admin
from .models import Lab, Cabinet, Setup, Item, Flag, Category

admin.site.register(Lab)
admin.site.register(Cabinet)
admin.site.register(Setup)
admin.site.register(Item)
admin.site.register(Flag)
admin.site.register(Category)
