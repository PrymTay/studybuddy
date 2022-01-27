from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from base.models import Message, Rooms, Topic, User, UserProfile
#
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from base import admin

# class UserProfileInline(admin.StackedInline):
#     model = UserProfile
#     can_delete = False
#     verbose_name_plural = 'userprofile'


# class UserAdmin(BaseUserAdmin):
#     inlines = ([UserProfileInline])

 

# Register your models here.
admin.site.register(Rooms)
admin.site.register(Message)
admin.site.register(Topic)
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)