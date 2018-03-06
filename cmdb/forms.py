from django import forms
from cmdb import models

#设备表单
class DeviceForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'style17','placeholder': '请输入设备名称','width': '800px;'}))
    category_id = forms.IntegerField(widget=forms.Select(attrs = {'style':'height:30px;width:182px'}))
    ip = forms.GenericIPAddressField(widget=forms.TextInput(attrs={'class':'style5','placeholder': '请输入设备IP'}))
    code = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'style5','placeholder': '请输入设备序列号'}))
    worth = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'style5','placeholder': '请输入采购金额'}))
    business_unit = forms.IntegerField(required=False,widget=forms.Select(attrs = {'style':'height:30px;width:182px','class':'style5'}))
    remark = forms.CharField(required=False,widget=forms.Textarea(attrs={'class':'textarea2'}))
    userpro = forms.IntegerField(required=False,widget=forms.Select(attrs = {'style':'height:30px;width:182px','class':'style5'}))
    #tag = forms.IntegerField(widget=forms.Select(attrs = {'style':'height:24px;width:152px'}))
    room = forms.IntegerField(required=False,widget=forms.Select(attrs = {'style':'height:30px;width:182px','class':'style5'}))
    guaranteed = forms.IntegerField(required=False,widget=forms.TextInput(attrs = {'style':'height:30px;width:104px','class':'style5','placeholder': '维保期限（年）'}))
    production_date = forms.CharField(required=False,widget=forms.DateInput(attrs={'type':'date','class':'style5','style':'height:30px;width:182px'}))
    up_date = forms.CharField(required=False,widget=forms.DateInput(attrs={'type':'date','class':'style5','style':'height:30px;width:182px'}))
    def __init__(self,*args,**kwargs):
        super(DeviceForm,self).__init__(*args,**kwargs)
        self.fields['category_id'].widget.choices = models.Category.objects.all().values_list('id','name')
        self.fields['business_unit'].widget.choices = models.Business_unit.objects.all().values_list('id', 'name')
        self.fields['userpro'].widget.choices = models.UserProfile.objects.all().values_list('id', 'name')
        self.fields['room'].widget.choices = models.Room.objects.all().values_list('id', 'name')