from django.db import models
from home.models import student,faculty,subject,department
from events.models import event

# Create your models here.
class subjectTeacher(models.Model):
    faculty = models.ForeignKey(faculty,on_delete=models.CASCADE)
    subject = models.ForeignKey(subject,on_delete=models.CASCADE)
    class Meta:
        unique_together = (('faculty','subject'),)

class project(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=25)
    details = models.CharField(max_length=500)
    withCollege = models.BooleanField()
    link =  models.URLField(max_length=200, blank=True, default='')
    category = models.CharField(max_length=15,null=True)
    department = models.ForeignKey(department,null=True,on_delete=models.CASCADE)
    guide = models.ForeignKey(faculty,null=True,on_delete=models.DO_NOTHING)
    hackathon = models.ForeignKey(event,null=True,on_delete=models.CASCADE)
    completion = models.IntegerField(default=0)
    approval = models.IntegerField(default=0)

class studentProject(models.Model):
    project = models.ForeignKey(project,null=False,on_delete=models.DO_NOTHING)
    student = models.ForeignKey(student,null=False,on_delete=models.DO_NOTHING)
    
    class Meta:
        unique_together = (('project','student'),)