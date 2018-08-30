from django.db import models
from usercenter.models import UserModel

# Create your models here.


class TagsModel(models.Model):
    tid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, verbose_name="标签名称")
    remark = models.CharField(max_length=150, verbose_name="备注说明")
    date = models.DateTimeField(auto_now_add=True, verbose_name="时间")
    type = models.CharField(max_length=30, verbose_name="类型")
    unique = models.CharField(max_length=150, unique=True, verbose_name="唯一性判断")


class CategoryModel(models.Model):
    cid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, verbose_name="名称")
    index = models.IntegerField(default=999, verbose_name="排序")
    date = models.DateTimeField(auto_now_add=True, verbose_name="时间")
    remark = models.CharField(max_length=150, verbose_name="备注说明")
    type = models.CharField(max_length=30, verbose_name="类型")
    count = models.IntegerField(default=0, verbose_name="数量")
    unique = models.CharField(max_length=150, unique=True, verbose_name="唯一性判断")

class FileModel(models.Model):
    fid = models.AutoField(primary_key=True)
    md5 = models.CharField(max_length=100, verbose_name="md5")
    name = models.CharField(max_length=100,verbose_name="名称")
    file_add = models.CharField(max_length=300,verbose_name="附件地址")
    type = models.CharField(max_length=100,verbose_name="附件类型")
    size = models.IntegerField(default=0, verbose_name="大小")
    date = models.DateTimeField(auto_now_add=True, verbose_name="时间")
    category = models.CharField(max_length=100, verbose_name="分类")

class ArticleModel(models.Model):
    aid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name="文章标题")
    desc = models.TextField(verbose_name="文章描述")
    content = models.TextField(verbose_name="文章内容")
    click_count = models.IntegerField(default=0, verbose_name="点击次数")
    date_publish = models.DateTimeField(auto_created=True,auto_now_add=True,verbose_name="发布时间")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name="用户")
    category = models.ForeignKey(CategoryModel,on_delete=models.CASCADE, blank=True, null=True, verbose_name="分类")
    tag = models.ManyToManyField(TagsModel, verbose_name="标签")
    is_recommend = models.BooleanField(default=True, verbose_name="是否草稿")
    type = models.CharField(max_length=30, verbose_name="查看类型")
    watched = models.BooleanField(default=True, verbose_name="是否查看")

class CommentsModel(models.Model):
    cid = models.AutoField(primary_key=True)
    content = models.TextField(verbose_name="评论内容")
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    username = models.CharField(max_length=50, verbose_name="用户")
    usertype = models.IntegerField(default=0, verbose_name="用户类型")
    qq = models.CharField(max_length=13, blank=True, null=True, verbose_name="QQ号")
    mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name="电话号")
    pid = models.ForeignKey('self',on_delete=models.CASCADE, blank=True, null=True, verbose_name="父级评论")
    is_recommend = models.BooleanField(default=True, verbose_name="是否显示")
    watched = models.BooleanField(default=True, verbose_name="是否查看")
    email = models.CharField(max_length=50, verbose_name="邮箱")
    article_title = models.CharField(max_length=50, verbose_name="文章")
    article = models.ForeignKey(ArticleModel,on_delete=models.CASCADE,)