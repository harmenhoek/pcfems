from django.contrib import admin
from .models import Lab, Cabinet, Setup, Item, Flag, Category, ItemImage, ItemLog
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(Lab, SimpleHistoryAdmin)
admin.site.register(Cabinet, SimpleHistoryAdmin)
admin.site.register(Setup, SimpleHistoryAdmin)
admin.site.register(Flag, SimpleHistoryAdmin)
admin.site.register(Category, SimpleHistoryAdmin)
admin.site.register(ItemLog, SimpleHistoryAdmin)

class PostImageAdmin(admin.StackedInline):
    model = ItemImage


class ItemAdmin(admin.ModelAdmin):
    inlines = [PostImageAdmin]

    class Meta:
        model = Item

# define a new class that inherits the Admins from Item and SampleHistory.
# https://stackoverflow.com/questions/61746318/allowing-django-admin-site-register-to-take-more-than-3-arguments
class ItemAdminSimpleHistoryAdmin(ItemAdmin, SimpleHistoryAdmin):
    pass
admin.site.register(Item, ItemAdminSimpleHistoryAdmin)


class ItemImageAdmin(admin.ModelAdmin):
    pass
class ItemImageAdminSimpleHistoryAdmin(ItemImageAdmin, SimpleHistoryAdmin):
    pass
admin.site.register(ItemImage, ItemImageAdminSimpleHistoryAdmin)




# class ItemImageInline(admin.TabularInline):
#     model = ItemImages
#     extra = 3
#
# class ItemAdmin(admin.ModelAdmin):
#     inlines = [ ItemImageInline, ]
#
# admin.register(Item, ItemAdmin, SimpleHistoryAdmin)