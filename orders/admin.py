from django.contrib import admin
from .models import Ofi, OrderCategory, Order, OrderLog

from simple_history.admin import SimpleHistoryAdmin

admin.site.register(Ofi, SimpleHistoryAdmin)
admin.site.register(OrderCategory, SimpleHistoryAdmin)
admin.site.register(Order, SimpleHistoryAdmin)
admin.site.register(OrderLog, SimpleHistoryAdmin)