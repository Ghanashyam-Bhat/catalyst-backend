from django.contrib import admin
from .models import project,studentProject,subjectTeacher

# Register your models here.
admin.site.register(project)
admin.site.register(studentProject)
admin.site.register(subjectTeacher)
