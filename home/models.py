from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class faculty(models.Model):
    id = models.CharField(max_length=13,primary_key=True)
    name = models.CharField(max_length=25)
    access = models.IntegerField(default=0)
    class Meta:
        verbose_name_plural = 'Faculties'

class department(models.Model):
    id =  models.CharField(primary_key=True,max_length=15)
    name = models.CharField(max_length=15)
    chairperson = models.ForeignKey(faculty,on_delete=models.DO_NOTHING)
    
class student(models.Model):
    srn  = models.CharField(max_length=13,primary_key=True)
    name = models.CharField(max_length=25) 
    sem = models.IntegerField()
    cgpa = models.FloatField()
    department = models.ForeignKey(department,on_delete=models.CASCADE)
    crypto = models.FloatField(validators=[MinValueValidator(0)],default=0)

    
class club(models.Model):
    id = models.CharField(max_length=13,primary_key=True)
    name = models.CharField(max_length=25)
    head = models.ForeignKey(student,on_delete=models.CASCADE)
    faculty = models.ForeignKey(faculty,on_delete=models.CASCADE)

class subject(models.Model):
    id = models.CharField(primary_key=True,max_length=15)
    name = models.CharField(max_length=15)
    department = models.ForeignKey(department,on_delete=models.CASCADE)
