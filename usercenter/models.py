from django.db import models

# Create your models here.

class UserModel(models.Model):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30,unique=True, verbose_name="用户名")
    sex = models.CharField(max_length=10, null=True,verbose_name="性别")
    email = models.CharField(max_length=30, verbose_name="邮箱")
    photo = models.CharField(default="/static/currency/userphoto/default/user.png",max_length=100,null=True,verbose_name="头像")
    wechat = models.CharField(max_length=30,null=True, verbose_name="微信")
    qq = models.CharField(max_length=30, null=True, verbose_name="QQ")
    phone = models.CharField(max_length=30, null=True, verbose_name="电话")
    date = models.DateTimeField(auto_now_add=True, verbose_name="时间")
    password = models.CharField(max_length=30, verbose_name="密码")
    type = models.CharField(max_length=30, verbose_name="类型")
    state = models.BooleanField(default=True, verbose_name="状态")
