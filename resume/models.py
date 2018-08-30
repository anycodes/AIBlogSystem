from django.db import models

# Create your models here.

class ResumeModel(models.Model):
    rid = models.AutoField(primary_key=True)
    keyData = models.CharField(max_length=100)
    valueData = models.TextField()