from django.shortcuts import render,render_to_response
from account.views import login_check,get_login_user_info

# Create your views here.
@login_check
#展示服务登记页面
def index(req,*args,**kwargs):
    userinfo = get_login_user_info(req)
    return render_to_response('notice/index.html',)