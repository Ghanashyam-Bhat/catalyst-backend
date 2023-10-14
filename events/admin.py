from django.contrib import admin
from .models import event,participant,organizer,report

# Register your models here.
admin.site.register(event)
admin.site.register(participant)
admin.site.register(organizer)
admin.site.register(report)
