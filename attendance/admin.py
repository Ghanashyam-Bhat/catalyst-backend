from django.contrib import admin
from .models import fam,studentcourse,declaration,attendaceRequest,subjectAttendaceRequest

admin.site.register(fam)
admin.site.register(studentcourse)
admin.site.register(declaration)
admin.site.register(attendaceRequest)
admin.site.register(subjectAttendaceRequest)

# Register your models here.
