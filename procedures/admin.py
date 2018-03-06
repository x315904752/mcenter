from django.contrib import admin
from procedures.models import change_flow,change_type,change_deal_info,event_flow,event_type



# Register your models here.
admin.site.register(change_flow)
admin.site.register(change_type)
admin.site.register(change_deal_info)
admin.site.register(event_flow)
admin.site.register(event_type)