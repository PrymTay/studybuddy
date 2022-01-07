from django.contrib import admin

from base.models import Message, Rooms, Topic

# Register your models here.
admin.site.register(Rooms)
admin.site.register(Message)
admin.site.register(Topic)