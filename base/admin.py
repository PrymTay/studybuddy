from django.contrib import admin

from base.models import Rooms, Topic, message

# Register your models here.
admin.site.register(Rooms)
admin.site.register(message)
admin.site.register(Topic)