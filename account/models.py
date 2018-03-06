from django.db import models

# Create your models here.


#用户表
class UserProfile(models.Model):
    name = models.CharField('姓名',max_length=32,null=True,default=None)
    email = models.EmailField('邮箱',blank=True)
    phone = models.CharField('座机',blank=True,max_length=32,null=True,default=None)
    mobile = models.CharField('手机',blank=True,max_length=32,null=True,default=None)
    remark = models.TextField('备注',blank=True)
    wechat = models.CharField('微信号',blank=True,max_length=64,default=None)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class AdminInfo(models.Model):
    userpro = models.OneToOneField('UserProfile', default=None,on_delete=models.DO_NOTHING)
    username = models.CharField('用户名',max_length=32,null=True,default=None)
    password = models.CharField('密码',max_length=32,null=True,default=None)
    permission = models.ForeignKey('Permission',default=None,on_delete=models.DO_NOTHING)

class Permission(models.Model):
    name = models.CharField('权限名称',max_length=32,null=True,default=None)
