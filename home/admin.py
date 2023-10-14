from django.contrib import admin
from .models import student,faculty,club,department,subject
# Register your models here.
admin.site.register(student)
admin.site.register(faculty)
admin.site.register(club)
admin.site.register(department)
admin.site.register(subject)