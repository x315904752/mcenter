from django.db import models
from account import models as account_models
# Create your models here.



#工作流表
class change_flow(models.Model):
    flow_num = models.IntegerField('步骤编号')
    flow_name = models.CharField('流程名称',max_length=32)
    flow_repeat_no = models.IntegerField('审批次数',blank=True)
    flow_role = models.ManyToManyField(account_models.UserProfile,blank=True)
    flow_verify_people = models.BooleanField('指定审核人员',blank=True)
    def __str__(self):
        return self.flow_name

class change_type(models.Model):
    name = models.CharField('变更类型', max_length=32, null=True)
    def __str__(self):
        return self.name


#变更信息表
class change_info(models.Model):
    change_type = models.ForeignKey('change_type',on_delete=models.DO_NOTHING)
    change_device = models.CharField('关联设备',blank=True,null=True,max_length=100)#关联资产
    change_partner = models.ManyToManyField(account_models.UserProfile,related_name='change_partner')#参与者ID
    change_verify_people = models.ForeignKey(account_models.UserProfile,null=True,on_delete=models.DO_NOTHING,related_name='change_verify_people')#确认者ID
    change_theme = models.CharField('变更主题',null=True,max_length=100)
    change_target = models.TextField('变更目的',blank=True,null=True)
    change_plan = models.TextField('变更方案',blank=True,null=True)
    change_back = models.TextField('回退方案', blank=True, null=True)
    change_note = models.TextField('变更记录', blank=True, null=True)
    change_create_time = models.DateTimeField('创建时间',auto_now_add=True)
    change_create_people = models.ForeignKey(account_models.UserProfile,on_delete=models.DO_NOTHING,null=True,related_name='change_create_people')
    change_flow = models.ForeignKey('change_flow',on_delete=models.DO_NOTHING,null=True)
    change_flag = models.IntegerField('变更状态')#0:已删除，1:未通过，2:审批中，3：已完成，4：待验证
    def __str__(self):
        return self.change_theme


class change_deal_info(models.Model):
    change_deal_time = models.DateTimeField('处理时间',auto_now_add=True)
    change_info = models.ForeignKey('change_info',verbose_name='关联变更',on_delete=models.DO_NOTHING)
    change_flow = models.ForeignKey('change_flow',verbose_name='关联步骤',on_delete=models.DO_NOTHING)
    change_people = models.ForeignKey(account_models.UserProfile,verbose_name='关联处理人',on_delete=models.DO_NOTHING)
    change_action = models.IntegerField('处理结果',null=True)#0：不通过，1：通过，2：已创建
    change_note = models.TextField('处理意见',null=True,blank=True)



class change_next_people(models.Model):
    change_info = models.ForeignKey('change_info',verbose_name='关联变更',on_delete=models.DO_NOTHING)
    change_flow = models.ForeignKey('change_flow', verbose_name='关联动作', on_delete=models.DO_NOTHING)
    next_people = models.ForeignKey(account_models.UserProfile,verbose_name='关联处理人',on_delete=models.DO_NOTHING,default=None,null=True)



#工作流表
class event_flow(models.Model):
    flow_num = models.IntegerField('步骤编号')
    flow_name = models.CharField('流程名称',max_length=32)
    flow_role = models.ManyToManyField(account_models.UserProfile,blank=True)
    def __str__(self):
        return self.flow_name

class event_type(models.Model):
    name = models.CharField('事件类型', max_length=32, null=True)
    def __str__(self):
        return self.name



class event_info(models.Model):
    event_type = models.ForeignKey('event_type',verbose_name='事件分类',default=None,on_delete=models.DO_NOTHING)
    device = models.CharField('关联资产',blank=True,null=True,max_length=100, default=None)#关联资产
    event_theme = models.CharField('事件主题',null=True,max_length=100, default=None)
    event_description = models.TextField('事件描述',blank=True,null=True, default=None)
    event_start_time = models.DateTimeField('产生时间',auto_now_add=True)
    event_deal_people = models.ForeignKey(account_models.UserProfile,verbose_name='指派人员',default=None,on_delete=models.DO_NOTHING, related_name='event_deal_people')
    event_create_people = models.ForeignKey(account_models.UserProfile,verbose_name='创建人',blank=True,null=True,default=None,on_delete=models.DO_NOTHING, related_name='event_create_people')
    event_flow = models.ForeignKey('event_flow',verbose_name='关联流程',default=None,on_delete=models.DO_NOTHING)
    event_flag = models.IntegerField('事件状态',default=None)#0:已删除，1:未通过，2:处理中，3：已完成，4：待验证



class event_next_people(models.Model):
    event_info = models.ForeignKey('event_info',verbose_name='关联事件',on_delete=models.DO_NOTHING)
    event_flow = models.ForeignKey('event_flow', verbose_name='关联动作', on_delete=models.DO_NOTHING)
    next_people = models.ForeignKey(account_models.UserProfile,verbose_name='关联处理人',on_delete=models.DO_NOTHING,default=None,null=True)


class event_deal_info(models.Model):
    event_deal_time = models.DateTimeField('处理时间',auto_now_add=True)
    event_info = models.ForeignKey('event_info',verbose_name='关联事件',on_delete=models.DO_NOTHING)
    event_flow = models.ForeignKey('event_flow',verbose_name='关联步骤',on_delete=models.DO_NOTHING)
    event_people = models.ForeignKey(account_models.UserProfile,verbose_name='关联处理人',on_delete=models.DO_NOTHING)
    event_action = models.IntegerField('处理结果',null=True)#0：不通过，1：通过，2：已创建
    event_note = models.TextField('处理意见',null=True,blank=True)