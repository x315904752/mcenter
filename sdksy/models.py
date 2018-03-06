from django.db import models

# Create your models here.



class business(models.Model):
    business_start_day = models.DateField('开始日期')
    business_end_day = models.DateField('结束日期')
    business_start_time = models.TimeField('开始时间')
    business_end_time = models.TimeField('结束时间')
    business_name = models.CharField('业务名称',max_length=32)
    business_remark = models.TextField('业务备注')
