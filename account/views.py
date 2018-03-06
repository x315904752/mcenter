from django.shortcuts import render,HttpResponseRedirect,render_to_response,redirect
from account.models import AdminInfo,UserProfile
from account.forms import UserForm,ChangePassword
from procedures import models as procedure_models


#获取当前登陆用户的个人信息
def get_login_user_info(req):
    #从session中获取登录用户的名字
    username = req.session.get('username', None)
    #根据名字查询登录用户的具体信息
    userinfo = UserProfile.objects.get(name__exact=username)

    change_need_deal = procedure_models.change_next_people.objects.filter(next_people=userinfo).count()
    event_need_deal = procedure_models.event_next_people.objects.filter(next_people=userinfo).count()
    for change_flow in userinfo.change_flow_set.all():
        change_need_deal += change_flow.change_next_people_set.all().count()
    all_need_deal = change_need_deal + event_need_deal
    return userinfo,all_need_deal


#登录验证
def login_check(main_func):
    def wrapper(request,*args,**kwargs):
        if request.session.get('username'):
            return main_func(request,*args,**kwargs)
        else:
            return redirect('/account/login')
    return  wrapper



def login(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            #获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #获取的表单数据与数据库进行比较
            success = AdminInfo.objects.filter(username__exact = username,password__exact = password)
            if success:
                # username = uf.cleaned_data['username']
                # 把获取表单的用户名传递给session对象
                req.session['username'] = UserProfile.objects.filter(id__exact=success.values('userpro')[0]['userpro']).values('name')[0]['name']
                req.session['user'] = username
                return HttpResponseRedirect('/procedures/index/')
            else:
                #比较失败，还在login
                return render_to_response('account/login.html',{'error':'用户名或密码错误！','uf':uf})
    else:
        uf = UserForm()
    return render_to_response('account/login.html',{'uf':uf})


#退出登录
def logout(req):
    try:
        del req.session['username']  #删除session
    except KeyError:
        pass
    return HttpResponseRedirect('/account/login/')






def index(req,*args,**kwargs):
    username = req.session.get('username', None)
    return render_to_response('account/index.html',{'username':username})


def change_info(req,*args,**kwargs):
    username = req.session.get('username', None)
    # 查询登录用户的相关信息
    userinfo = UserProfile.objects.filter(name__exact=username).values('id', 'name', 'mobile', 'email')
    if len(userinfo) != 1:
        userinfo = userinfo[0]
    else:
        userinfo = userinfo[0]
    user = req.session.get('user', None)
    error = ''
    if req.method == 'POST':
        uf = ChangePassword(req.POST)
        if uf.is_valid():
            old_password = uf.cleaned_data['old_password']
            password = uf.cleaned_data['password']
            if AdminInfo.objects.filter(username__exact = user,password__exact = old_password):
                AdminInfo.objects.filter(username__exact=user, password__exact=old_password).update(password=password)
                return redirect('/account/logout/')
            else:
                error = '您输入的旧密码不正确，请重新输入！'
    else:
        uf = ChangePassword()
    return render_to_response('account/change_info.html', {'userinfo':userinfo,'uf':uf,'error':error})
