from django.db import models
from currency.models import FileModel,CategoryModel,TagsModel
# Create your models here.


class ImagesModel(models.Model):
    iid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,verbose_name="名称")
    picture = models.ForeignKey(FileModel,on_delete=models.CASCADE,verbose_name="图片")
    is_recommend = models.BooleanField(default=True, verbose_name="是否显示")
    index = models.IntegerField(default=999, verbose_name="排序")
    tag = models.ManyToManyField(TagsModel, verbose_name="标签")
    album = models.ForeignKey(CategoryModel,on_delete=models.CASCADE, blank=True, null=True, verbose_name="相册")
