from django.contrib import admin
from account.models import UserProfile,AdminInfo,Permission



# Register your models here.
admin.site.register(UserProfile)
admin.site.register(AdminInfo)
admin.site.register(Permission)
