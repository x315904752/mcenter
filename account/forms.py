from django import forms
from account import models as account_models

#登录页面用户表单（用户名、密码）
class UserForm(forms.ModelForm):
    class Meta:
        model = account_models.AdminInfo
        fields = ['username','password']
        widgets = {
            'username':forms.TextInput(attrs = {'placeholder':'请输入用户名'}),
            'password': forms.PasswordInput(attrs={'placeholder': '请输入密码'}),
        }

class ChangePassword(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'请输入旧密码'}))
    class Meta:
        model = account_models.AdminInfo
        fields = ['password']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': '请输入新密码'}),
        }