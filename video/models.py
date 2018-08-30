from django.db import models

# Create your models here.

class VideoModel(models.Model):
    vid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    titleList = models.TextField()
    numberList = models.TextField()
    urlList = models.TextField()