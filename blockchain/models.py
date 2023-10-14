from django.db import models

# Create your models here.
class block(models.Model):
    index = models.IntegerField(primary_key=True)
    proof = models.IntegerField()
    prevHash = models.CharField(max_length=50)
    data = models.CharField(max_length=500)
    timestamp = models.DateTimeField()
    users_hash = models.CharField(max_length=50)
    current_hash = models.CharField(max_length=50)
    