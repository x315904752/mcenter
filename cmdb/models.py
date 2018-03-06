from django.db import models
from account.models import UserProfile
#-------------------------------------------------------------------------------------
# Create your models here.
# class Position(models.Model):
#     name = models.CharField('项目名称', max_length=32, null=True, default=None)
#     address = models.CharField('地址', max_length=100, null=True, default=None)
#     create_user = models.ForeignKey(UserProfile, default=None)
#     create_time = models.DateTimeField('创建时间',auto_now_add=True)
#     update_time = models.DateTimeField(blank=True, auto_now=True)
#     remark = models.CharField('备注', max_length=200, null=True, default=None)
#
# class Room(models.Model):
#     name = models.CharField('房间名称', max_length=32, null=True, default=None)
#     position_id = models.OneToOneField('Position', default=None)
#     floor = models.IntegerField('楼层', null=True, default=None)
#     room_area = models.FloatField('机房面积',default=None)
#     create_user = models.ForeignKey(UserProfile, default=None)
#     create_time = models.DateTimeField(blank=True, auto_now_add=True)
#     update_time = models.DateTimeField(blank=True, auto_now=True)
#     delete_flag = models.BooleanField('删除标识',default=None)
#     remark = models.CharField('备注', max_length=200, null=True, default=None)
#
# class Contract(models.Model):
#     sn = models.CharField('合同号码',max_length=64,unique=True)
#     name = models.CharField('合同名称', max_length=32, null=True, default=None)
#     cost = models.FloatField('合同金额')
#     start_time = models.DateTimeField(blank=True)
#     end_time = models.DateTimeField(blank=True)
#     remark = models.CharField('备注', max_length=200, null=True, default=None)
#     create_time = models.DateTimeField(blank=True,auto_now_add=True)
#     update_time = models.DateTimeField(blank=True,auto_now=True)
#
# class Tag(models.Model):
#     name = models.CharField('标签名称',max_length=32,unique=True)
#     creater = models.ForeignKey(UserProfile,blank=True,null=True)
#
# class Cabinet(models.Model):
#     name = models.CharField('机柜名称', max_length=32, null=True, default=None)
#     room_id = models.ForeignKey('Room', default=None)
#     code = models.IntegerField('资产编号', null=True, default=None)
#     contract_id = models.ForeignKey('Contract',default=None)
#     udigit = models.IntegerField('总U数', null=True, default=None)
#     length = models.IntegerField('机柜长', null=True, default=None)
#     width = models.IntegerField('机柜宽', null=True, default=None)
#     hight = models.IntegerField('机柜高', null=True, default=None)
#     worth = models.FloatField('采购金额', null=True, default=None)
#     remark = models.CharField('备注',max_length=200,null=True, default=None)
#     create_time = models.DateTimeField(blank=True, auto_now_add=True)
#     update_time = models.DateTimeField(blank=True, auto_now=True)
#     delete_flag = models.BooleanField('删除标识',default=None)
#
# class Category(models.Model):
#     name = models.CharField('分类名称', max_length=32, null=True, default=None)
#     remark = models.CharField('备注', max_length=200, null=True, default=None)
#
# class Business_unit_1(models.Model):
#     name = models.CharField('一级分类', max_length=32, null=True, default=None)
#
# class Business_unit_2(models.Model):
#     name = models.CharField('二级分类', max_length=32, null=True, default=None)
#     bussiness_unit_1 = models.ForeignKey('Business_unit_1',verbose_name='所属一级',null=True,blank=True)
#
# class Business_unit_3(models.Model):
#     name = models.CharField('三级分类', max_length=32, null=True, default=None)
#     bussiness_unit_2 = models.ForeignKey('Business_unit_2', verbose_name='所属二级', null=True, blank=True)
#
#
# class Asset(models.Model):
#     name = models.CharField('设备名称', max_length=32, null=True, default=None)
#     cabinet_id = models.ForeignKey('Cabinet', default=None)#关联机柜
#     contract_id = models.ForeignKey('Contract', default=None)#关联合同
#     category_id = models.ForeignKey('Category', default=None)#关联资产类型
#     code = models.IntegerField('资产编号', null=True, default=None)
#     worth = models.FloatField('采购金额', null=True, default=None)
#     cabinet_position = models.CommaSeparatedIntegerField(max_length=32)#机柜位置
#     business_unit = models.ForeignKey('Business_unit_3',verbose_name='所属三级',null=True,blank=True)
#     remark = models.TextField('备注')
#     create_time = models.DateTimeField(blank=True, auto_now_add=True)
#     update_time = models.DateTimeField(blank=True, auto_now=True)
#     userpro = models.ForeignKey(UserProfile,verbose_name='设备负责人',null=True,blank=True)
#     tag = models.ManyToManyField('Tag',null=True,blank=True)
#     delete_flag = models.BooleanField('删除标识', default=None)
#
# class Manufactory(models.Model):
#     name = models.CharField('厂商名称',max_length=32)
#     phone = models.CharField('400电话',max_length=32)
#
#
# class Server(models.Model):
#     asset = models.OneToOneField('Asset')
#     sn = models.CharField('序列号',max_length=64)
#     manufactory = models.ForeignKey('Manufactory',verbose_name='关联厂商')
#     model = models.CharField('型号',max_length=32,null=True,blank=True)
#     create_time = models.DateTimeField(blank=True,auto_now_add=True)
#     update_time = models.DateTimeField(blank=True,auto_now=True)
#     username = models.CharField('用户名',max_length=32)
#     password = models.CharField('密码', max_length=32)
#
# class Os(models.Model):
#     server = models.ForeignKey('Server',verbose_name='关联服务器')
#     name = models.CharField('系统名称',max_length=64)
#     version = models.CharField('系统版本',max_length=64)
#
# class Network(models.Model):
#     asset = models.OneToOneField('Asset')
#     sn = models.CharField('序列号',max_length=64)
#     manufactory = models.ForeignKey('Manufactory', verbose_name='关联厂商')
#     model = models.CharField('型号',max_length=32,null=True,blank=True)
#     username = models.CharField('用户名', max_length=32)
#     password = models.CharField('密码', max_length=32)
#     create_time = models.DateTimeField(blank=True, auto_now_add=True)
#     update_time = models.DateTimeField(blank=True, auto_now=True)
#
# class hba(models.Model):
#     server = models.ForeignKey('Server',verbose_name='关联服务器')
#     name = models.CharField('hba卡名称', max_length=32, null=True, default=None)
#     manufactory = models.ForeignKey('Manufactory', verbose_name='关联厂商')
#     model = models.CharField('型号', max_length=32, null=True, blank=True)
#     slot = models.CharField('槽位', max_length=32, null=True, blank=True)
#
#
# class hba_fc(models.Model):
#     hba = models.ForeignKey('hba',verbose_name='关联HBA卡')
#     bandwidth = models.IntegerField('带宽/M')
#     wwn = models.CharField('wwn号',max_length=64)
#
#
#
# class cpu(models.Model):
#     server = models.ForeignKey('Server',null=True,blank=True)
#     network = models.ForeignKey('Network',null=True,blank=True)
#     model = models.CharField('CPU型号',max_length=32)
#     hz = models.FloatField('主频')
#     num = models.IntegerField('CPU个数')
#-------------------------------------------------------------------------------------

class Business_unit(models.Model):
    name = models.CharField('所属业务', max_length=32, null=True, default=None)

class Category(models.Model):
    name = models.CharField('分类名称', max_length=32, null=True, default=None)

class Tag(models.Model):
    name = models.CharField('标签名称',max_length=32,unique=True)
    creater = models.ForeignKey(UserProfile,blank=True,null=True,on_delete=models.SET_NULL)

class Room(models.Model):
    name = models.CharField('机房名称', max_length=32, null=True, default=None)


class Asset(models.Model):
    name = models.CharField('设备名称', max_length=32, null=True, default=None)
    category_id = models.ForeignKey('Category',blank=True, null=True,on_delete=models.SET_NULL)#关联资产类型
    code = models.CharField('序列号',max_length=64,blank=True, null=True, default=None)
    ip = models.GenericIPAddressField('IP地址')
    worth = models.FloatField('采购金额',blank=True, null=True, default=None)
    business_unit = models.ForeignKey('Business_unit',verbose_name='所属业务',null=True,blank=True,on_delete=models.SET_NULL)
    remark = models.TextField('备注',blank=True, null=True)
    create_time = models.DateTimeField(blank=True, auto_now_add=True)
    update_time = models.DateTimeField(blank=True, auto_now=True)
    userpro = models.ForeignKey(UserProfile,verbose_name='设备负责人',null=True,blank=True,on_delete=models.DO_NOTHING)
    #tag = models.ManyToManyField('Tag',null=True,blank=True)
    #delete_flag = models.BooleanField('删除标识', default=None)
    room = models.ForeignKey('Room',verbose_name='所属机房',default=None,blank=True, null=True,on_delete=models.DO_NOTHING)
    guaranteed = models.IntegerField('保修期限',default=None,blank=True, null=True)
    production_date = models.DateField('生产日期',default=None,blank=True, null=True)
    up_date = models.DateField('上架日期',default=None,blank=True, null=True)
    def __str__(self):
        return self.name