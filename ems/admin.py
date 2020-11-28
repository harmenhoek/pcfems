from django.contrib import admin
from .models import Lab, Cabinet, Setup, Item, Flag, Category
from simple_history.admin import SimpleHistoryAdmin

# admin.site.register(Lab)
# admin.site.register(Cabinet)
# admin.site.register(Setup)
# admin.site.register(Item)
# admin.site.register(Flag)
# admin.site.register(Category)

admin.site.register(Lab, SimpleHistoryAdmin)
admin.site.register(Cabinet, SimpleHistoryAdmin)
admin.site.register(Setup, SimpleHistoryAdmin)
admin.site.register(Item, SimpleHistoryAdmin)
admin.site.register(Flag, SimpleHistoryAdmin)
admin.site.register(Category, SimpleHistoryAdmin)