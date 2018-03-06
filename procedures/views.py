from django.shortcuts import render_to_response,HttpResponse,redirect
from account.views import login_check,get_login_user_info
from account import models as account_models
from procedures import models as procedures_models
from procedures import forms as procedures_forms
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q
from report.date_index import get_date
from wechat import wechat_api
import datetime,time,json




@login_check
#展示index页面
def index(req,*args,**kwargs):
    userinfo,all_need_deal =get_login_user_info(req)

    #获取本周的开始时间
    this_month_start_day = time.strptime(get_date.this_month_start.strftime('%Y-%m-%d'), '%Y-%m-%d')
    year, month, day = this_month_start_day[:3]
    this_month_start = datetime.datetime(year, month, day)

    # 获取所有的变更类型
    all_change_type = procedures_models.change_type.objects.all()
    # 获取所有的事件类型
    all_event_type = procedures_models.event_type.objects.all()
    # 创建列表用来保存事件类型
    event_info_type = []
    change_info_type = []
    for event_type in all_event_type:
        event = {}
        event_num = event_type.event_info_set.filter(event_start_time__gte=this_month_start).count()
        event['value'] = event_num
        event['name'] = event_type.name
        event_info_type.append(event)

    for change_type in all_change_type:
        change = {}
        change_num = change_type.change_info_set.filter(change_create_time__gte=this_month_start).count()
        change['name'] = change_type.name
        change['value'] = change_num
        change_info_type.append(change)

    # 获取所有的运维人员信息
    all_user = account_models.UserProfile.objects.all()
    # 创建列表用来保存事件信息
    event_info_user = []
    change_info_user = []
    for event_user in all_user:
        event = {}
        event_info = event_user.event_deal_people.filter(event_start_time__gte=this_month_start)
        finish = event_info.filter(event_flag__exact=3,).count()
        unfinish = event_info.filter(Q(event_flag__exact=2) | Q(event_flag__exact=4)).count()
        event['deal_people'] = event_user.name
        event['finish'] = finish
        event['unfinish'] = unfinish
        event_info_user.append(event)
    for change_user in all_user:
        change = {}
        change_info = change_user.change_create_people.filter(change_create_time__gte=this_month_start)
        finish = change_info.filter(change_flag__exact=3, ).count()
        unfinish = change_info.filter(Q(change_flag__exact=2) | Q(change_flag__exact=4)).count()
        change['create_people'] = change_user.name
        change['finish'] = finish
        change['unfinish'] = unfinish
        change_info_user.append(change)
    return render_to_response('procedures/index.html',
                              {
                                  'userinfo':userinfo,
                                  'all_need_deal':all_need_deal,
                                  'change_info_type':json.dumps(change_info_type),
                                  'event_info_type':json.dumps(event_info_type),
                                  'event_info_user':json.dumps(event_info_user),
                                  'change_info_user': json.dumps(change_info_user),
                              }
                              )


@login_check
#展示服务登记页面
def service_register(req,*args,**kwargs):
    userinfo,all_need_deal =get_login_user_info(req)

    this_week_start_day = time.strptime(get_date.this_week_start.strftime('%Y-%m-%d'),'%Y-%m-%d')
    year, month, day = this_week_start_day[:3]
    this_week_start = datetime.datetime(year, month, day)

    #获取所有的变更类型
    all_change_type = procedures_models.change_type.objects.all()
    #获取所有的事件类型
    all_event_type = procedures_models.event_type.objects.all()

    event_info = []
    change_info = []
    for event_type in all_event_type:
        event = {}
        finish_event = event_type.event_info_set.filter(event_flag__exact=3,event_start_time__gte=this_week_start).count()
        unfinish_event = event_type.event_info_set.filter(Q(event_flag__exact=2,event_start_time__gte=this_week_start) | Q(event_flag__exact=4,event_start_time__gte=this_week_start)).count()
        event['name'] = event_type.name
        event['finish'] = finish_event
        event['unfinish'] = unfinish_event
        event_info.append(event)
    for change_type in all_change_type:
        change = {}
        finish_change = change_type.change_info_set.filter(change_flag__exact=3,change_create_time__gte=this_week_start).count()
        unfinish_change = change_type.change_info_set.filter(Q(change_flag__exact=2,change_create_time__gte=this_week_start) | Q(change_flag__exact=4,change_create_time__gte=this_week_start)).count()
        change['name'] = change_type.name
        change['finish'] = finish_change
        change['unfinish'] = unfinish_change
        change_info.append(change)
    return render_to_response('procedures/service_register.html',
                              {
                                  'userinfo':userinfo,
                                  'all_need_deal': all_need_deal,
                                  'change_info':change_info,
                                  'event_info':event_info,
                              }
                              )


@login_check
#展示需要处理的工单
def need_deal(req,*args,**kwargs):
    userinfo,all_need_deal =get_login_user_info(req)
    user = account_models.UserProfile.objects.get(id__exact=userinfo.id)

    # 获取所有的工作流程
    all_change_flow = procedures_models.change_flow.objects.all().order_by('flow_num')
    # 获取工作流程步骤数
    all_change_flow_num = all_change_flow.count()

    #获取与当前用户相关的流程
    user_flow_list = user.change_flow_set.filter(flow_num__lt = all_change_flow_num)
    #循环每个流程里当前需要处理的工单
    change_list = []
    for user_flow in user_flow_list:
        for flow in user_flow.change_next_people_set.all().order_by('-id')[0:50]:
            change_list.append(flow.change_info)
    for flow in user.change_next_people_set.all():
        change_list.append(flow.change_info)


    event_list = []
    try:
        user_event_flow = user.event_flow_set.get(flow_num__exact=3)
        for event_flow in user_event_flow.event_next_people_set.all().order_by('-id')[0:50]:
            event_list.append(event_flow.event_info)
    except:
        pass
    for event_flow in user.event_next_people_set.all():
        event_list.append(event_flow.event_info)
    return render_to_response('procedures/need_deal.html',
                              {
                                  'userinfo':userinfo,
                                  'all_need_deal': all_need_deal,
                                  'change_list':change_list,
                                  'event_list':event_list,

                              }
                              )


@login_check
#展示我提交的工单
def i_submit(req,*args,**kwargs):
    userinfo,all_need_deal =get_login_user_info(req)
    user = account_models.UserProfile.objects.get(id__exact=userinfo.id)
    #获取与当前用户提交的订单
    get_change = user.change_create_people.order_by('-id')[0:50]
    get_change_num = len(get_change)
    paginator = Paginator(get_change, 10)
    page_num = paginator.num_pages
    page = req.GET.get('page')
    try:
        customer = paginator.page(page)
    except PageNotAnInteger:
        customer = paginator.page(1)
    except EmptyPage:
        customer = paginator.page(paginator.num_pages)
    return render_to_response('procedures/i_submit.html',
                              {
                                  'userinfo':userinfo,
                                  'all_need_deal': all_need_deal,
                                  'get_change':get_change,
                                  'get_change_num': get_change_num,
                                  'page_num': page_num,
                                  'customer': customer,
                              }
                              )


@login_check
#显示我参与的工单
def i_joined(req,*args,**kwargs):
    userinfo,all_need_deal =get_login_user_info(req)
    #获取与当前用户相关的流程
    get_change = procedures_models.change_info.objects.filter(id__gt=7).order_by('-id')[0:50]
    return render_to_response('procedures/i_joined.html',
                              {
                                  'userinfo':userinfo,
                                  'all_need_deal': all_need_deal,
                                  'get_change':get_change,
                              }
                              )

@login_check
#展示我处理过的工单
def i_deal(req,*args,**kwargs):
    userinfo,all_need_deal =get_login_user_info(req)
    #获取与当前用户相关的流程
    get_change = procedures_models.change_info.objects.filter(id__gt=7).order_by('-id')[0:50]
    return render_to_response('procedures/i_deal.html',
                              {
                                  'userinfo':userinfo,
                                  'all_need_deal':all_need_deal,
                                  'get_change':get_change,
                              }
                              )


@login_check
#处理对应的变更
def deal_change(req,changeid,**kwargs):
    userinfo,all_need_deal =get_login_user_info(req)
    #获取当前登陆用户
    user = account_models.UserProfile.objects.get(id__exact=userinfo.id)
    #获取当前工单
    cur_change = procedures_models.change_info.objects.get(id__exact=changeid)
    #获取当前处理明细，用于页面展示处理流程
    cur_deal_change = procedures_models.change_deal_info.objects.filter(change_info__exact=cur_change)
    #获取所有的工作流程
    all_change_flow = procedures_models.change_flow.objects.all().order_by('flow_num')
    #获取工作流程步骤数
    all_change_flow_num = all_change_flow.count()
    cur_change_next_people = cur_change.change_next_people_set.last()
    # 获取当前操作的流程
    cur_change_flow = cur_change_next_people.change_flow
    # 获取当前步骤是否指定验证人员
    if_flow_verify_people = cur_change_flow.flow_verify_people
    if req.method == 'POST':
        uf = procedures_forms.DealChangeForm(req.POST)
        duf = procedures_forms.DealChangeVerifyPeopleForm(req.POST)
        # 如果表单数据合法
        if duf.is_valid():
            #验证人员保存到变更信息表中
            cur_change.change_verify_people = duf.cleaned_data['change_verify_people']
            cur_change.save()
        if uf.is_valid():
            # 将数据保存在change变量中
            get_uf = uf.save(commit=False)
            #获取【下一处理人表】的信息
            get_uf.change_info = cur_change
            get_uf.change_people = user
            get_uf.change_flow = cur_change_flow
            get_uf.save()
            #如果审批人同意
            if get_uf.change_action == 1:
                #如果下一步是验证
                if cur_change_flow.flow_num + 1 == all_change_flow_num:
                    next_change_flow = all_change_flow[cur_change_flow.flow_num]
                    #将下一步设置为验证人，并更新【下一处理人表】
                    cur_change_next_people.next_people = cur_change.change_verify_people
                    cur_change_next_people.change_flow = next_change_flow
                    cur_change_next_people.save()
                    # 更新当前变更的流程到本流程
                    cur_change.change_flow = cur_change_flow
                    #将当前变更的状态设置为待验证
                    cur_change.change_flag = 4
                    # 保存当前变更的信息
                    cur_change.save()
                    ############################设置微信提醒信息##########################
                    # 设置微信提醒信息
                    title = '您有待验证的变更'
                    descrip = '<div class="normal">关联设备:【%s】<br>变更类型:【%s】<br>变更主题:【%s】<br>申请人员:【%s】</div>' % (
                        cur_change.change_device, cur_change.change_type, cur_change.change_theme,cur_change.change_create_people.name)
                    url = 'http://10.254.30.251/procedures/need_deal/'
                    # 获取微信提醒信息
                    PURL = wechat_api.GetUrl('wx690cf81ebd6fdf40', '6Sv1dIvSPAyZDobvpbde7WMgBj7uy9u5eEdGvXGoyyo')
                    # 获取需要通知的人员
                    touser = cur_change.change_verify_people.wechat
                    wechat_api.SendTextcard(title, descrip, PURL, url, touser)
                    ####################################################################
                #如果当前为在最后一步
                elif cur_change_flow.flow_num + 1 > all_change_flow_num:
                    #删除【下一处理人表】的相关表项
                    cur_change_next_people.delete()
                    #将工单设置为已完成状态
                    cur_change.change_flag = 3
                    #更新当前变更的流程到本流程
                    cur_change.change_flow = cur_change_flow
                    #保存当前变更的信息
                    cur_change.save()
                    ############################设置微信提醒信息##########################
                    # 设置微信提醒信息
                    title = '您提交的变更已完成'
                    descrip = '<div class="normal">关联设备:【%s】<br>变更类型:【%s】<br>变更主题:【%s】<br>申请人员:【%s】</div>' % (
                        cur_change.change_device, cur_change.change_type, cur_change.change_theme,cur_change.change_create_people.name)
                    url = 'http://10.254.30.251/procedures/need_deal/'
                    # 获取微信提醒信息
                    PURL = wechat_api.GetUrl('wx690cf81ebd6fdf40', '6Sv1dIvSPAyZDobvpbde7WMgBj7uy9u5eEdGvXGoyyo')
                    # 获取需要通知的人员
                    touser = cur_change.change_create_people.wechat
                    wechat_api.SendTextcard(title, descrip, PURL, url, touser)
                    ####################################################################
                #当前
                else:
                    #获取下一步变更的工作流
                    next_change_flow = all_change_flow[cur_change_flow.flow_num]
                    #将下一工作流程更新到【下一处理人表】中
                    cur_change_next_people.change_flow = next_change_flow
                    #保存【下一处理人表】
                    cur_change_next_people.save()
                    #更新当前变更的流程到本流程
                    cur_change.change_flow = cur_change_flow
                    #保存当前变更的信息
                    cur_change.save()
                    ############################设置微信提醒信息##########################
                    # 设置微信提醒信息
                    title = '您有待审批的变更'
                    descrip = '<div class="normal">关联设备:【%s】<br>变更类型:【%s】<br>变更主题:【%s】<br>申请人员:【%s】</div>' % (
                        cur_change.change_device, cur_change.change_type, cur_change.change_theme,cur_change.change_create_people.name)
                    url = 'http://10.254.30.251/procedures/need_deal/'
                    # 获取微信提醒信息
                    PURL = wechat_api.GetUrl('wx690cf81ebd6fdf40', '6Sv1dIvSPAyZDobvpbde7WMgBj7uy9u5eEdGvXGoyyo')
                    # 获取需要通知的人员
                    tousers = next_change_flow.flow_role.all()
                    for touser in tousers:
                        wechat_api.SendTextcard(title, descrip, PURL, url, touser.wechat)
                    ####################################################################
            #如果审批人不同意
            else:
                #将工单状态设置为未通过状态
                cur_change.change_flag = 1
                # 将工单流程状态更新为当前状态
                cur_change.change_flow = cur_change_flow
                cur_change.save()
                #删除下一处理人的相关表项
                cur_change_next_people.delete()
                ############################设置微信提醒信息##########################
                # 设置微信提醒信息
                title = '您的变更审批未通过，请重新提交'
                descrip = '<div class="normal">关联设备:【%s】<br>变更类型:【%s】<br>变更主题:【%s】<br>申请人员:【%s】</div>' % (
                        cur_change.change_device, cur_change.change_type, cur_change.change_theme,cur_change.change_create_people.name)
                url = 'http://10.254.30.251/procedures/need_deal/'
                # 获取微信提醒信息
                PURL = wechat_api.GetUrl('wx690cf81ebd6fdf40', '6Sv1dIvSPAyZDobvpbde7WMgBj7uy9u5eEdGvXGoyyo')
                # 获取需要通知的人员
                touser = cur_change.change_create_people.wechat
                wechat_api.SendTextcard(title, descrip, PURL, url, touser)
                ####################################################################
            #返回我的待办页面
            return  redirect('/procedures/need_deal/')
    else:
        uf = procedures_forms.DealChangeForm()
        duf = procedures_forms.DealChangeVerifyPeopleForm()
        return render_to_response('procedures/deal_change.html',
                                  {
                                      'userinfo':userinfo,
                                      'all_need_deal': all_need_deal,
                                      'cur_change':cur_change,
                                      'cur_deal_change':cur_deal_change,
                                      'uf':uf,
                                      'if_flow_verify_people':if_flow_verify_people,
                                      'duf':duf,
                                  }
                                  )





@login_check
#添加事件信息
def add_event(req,*args,**kwargs):
    userinfo,all_need_deal =get_login_user_info(req)
    #查找当前用户
    user = account_models.UserProfile.objects.get(id__exact=userinfo.id)

    #处理POST来的数据
    if req.method == 'POST':
        #获取表单post的数据
        uf = procedures_forms.EventForm(req.POST)
        #如果表单数据合法
        if uf.is_valid():
            #将数据保存在event变量中
            event = uf.save(commit=False)
            #绑定当前的用户信息
            event.event_create_people = user
            #获取当前变更流程的第一步
            event_flow = procedures_models.event_flow.objects.all().order_by('flow_num')
            event.event_flow = event_flow[0]
            #设置当前变更的状态为处理中（2）
            event.event_flag = 2
            #将数据提交至数据库中
            event.save()


            ############################设置事件处理摘要###########################
            procedures_models.event_deal_info.objects.create(
                event_info = event,
                event_flow = event_flow[0],
                event_people = user,
                event_action = 2,
                event_note = '',
            )
            ####################################################################

            ############################设置下一处理人信息#########################
            procedures_models.event_next_people.objects.create(
                event_info = event,
                event_flow = event_flow[1],
                next_people = uf.cleaned_data['event_deal_people']
            )
            ####################################################################

            ############################设置微信提醒信息##########################
            title = '您有待处理的事件'
            descrip = '<div class="normal">关联设备:【%s】<br>事件类型:【%s】<br>事件主题:【%s】</div>' % (
            uf.cleaned_data['device'], uf.cleaned_data['event_type'], uf.cleaned_data['event_theme'],)
            url = 'http://10.254.30.251/procedures/need_deal/'
            # 获取微信提醒信息
            PURL = wechat_api.GetUrl('wx690cf81ebd6fdf40', '6Sv1dIvSPAyZDobvpbde7WMgBj7uy9u5eEdGvXGoyyo')
            # 获取需要通知的人员
            touser = uf.cleaned_data['event_deal_people'].wechat
            # 发送提醒信息
            wechat_api.SendTextcard(title, descrip, PURL, url, touser)
            ####################################################################
            return redirect('/procedures/index/')
    #如果是GET，则返回添加变更的页面
    else :
        uf = procedures_forms.EventForm()
        return render_to_response(
            'procedures/add_event.html',
            {
                'userinfo':userinfo,
                'all_need_deal':all_need_deal,
                'uf':uf
            }
        )


@login_check
#处理对应的变更
def deal_event(req,eventid,**kwargs):
    userinfo,all_need_deal =get_login_user_info(req)
    #获取当前登陆用户
    user = account_models.UserProfile.objects.get(id__exact=userinfo.id)
    #获取当前事件
    cur_event = procedures_models.event_info.objects.get(id__exact=eventid)
    #获取当前处理明细，用于页面展示处理流程
    cur_deal_event = procedures_models.event_deal_info.objects.filter(event_info__exact=cur_event)
    cur_event_next_people = cur_event.event_next_people_set.last()
    # 获取当前操作的流程
    cur_event_flow = cur_event_next_people.event_flow

    if req.method == 'POST':
        uf = procedures_forms.DealEventForm(req.POST)
        if uf.is_valid():
            # 将数据保存在get_uf变量中
            get_uf = uf.save(commit=False)
            # 获取【下一处理人表】的信息
            get_uf.event_info = cur_event
            get_uf.event_people = user
            get_uf.event_flow = cur_event_flow
            get_uf.save()
            # 如果审批人同意
            if get_uf.event_action == 1:
                # 如果下一步是验证
                if cur_event_flow.flow_num + 1 == 3:
                    # 查找到最后一步的流程
                    next_event_flow = procedures_models.event_flow.objects.get(flow_num__exact=3)
                    cur_event_next_people.event_flow = next_event_flow
                    cur_event_next_people.save()

                    ############################设置微信提醒信息##########################
                    # 设置微信提醒信息

                    title = '您有待验证的事件'
                    print(title)
                    descrip = '<div class="normal">关联设备:【%s】<br>事件类型:【%s】<br>事件主题:【%s】</div>' % (cur_event.device, cur_event.event_type, cur_event.event_theme,)
                    url = 'http://10.254.30.251/procedures/need_deal/'
                    # 获取微信提醒信息
                    PURL = wechat_api.GetUrl('wx690cf81ebd6fdf40', '6Sv1dIvSPAyZDobvpbde7WMgBj7uy9u5eEdGvXGoyyo')
                    # 获取需要通知的人员
                    tousers = next_event_flow.flow_role.all()
                    for touser in tousers:
                        touser = touser.wechat
                        # 发送提醒信息
                        wechat_api.SendTextcard(title, descrip, PURL, url, touser)
                    ####################################################################

                    # 更新当前变更的流程到本流程
                    cur_event.event_flow = cur_event_flow
                    # 将当前变更的状态设置为待验证
                    cur_event.change_flag = 4
                    # 保存当前变更的信息
                    cur_event.save()

                #如果当前为在最后一步
                elif cur_event_flow.flow_num + 1 > 3:
                    #删除【下一处理人表】的相关表项
                    cur_event_next_people.delete()
                    #将工单设置为已完成状态
                    cur_event.event_flag = 3
                    #更新当前变更的流程到本流程
                    cur_event.event_flow = cur_event_flow
                    #保存当前变更的信息
                    cur_event.save()
                    ############################设置微信提醒信息##########################
                    # 设置微信提醒信息
                    title = '您提交的事件已经处理完毕'
                    print(title)
                    descrip = '<div class="normal">关联设备:【%s】<br>事件类型:【%s】<br>事件主题:【%s】</div>' % (cur_event.device, cur_event.event_type, cur_event.event_theme,)
                    url = 'http://10.254.30.251/procedures/need_deal/'
                    # 获取微信提醒信息
                    PURL = wechat_api.GetUrl('wx690cf81ebd6fdf40', '6Sv1dIvSPAyZDobvpbde7WMgBj7uy9u5eEdGvXGoyyo')
                    # 获取需要通知的人员
                    touser = cur_event.event_create_people.wechat
                    # 发送提醒信息
                    wechat_api.SendTextcard(title, descrip, PURL, url, touser)
                    ####################################################################
            #如果审批人不同意
            else:
                # 如果下一步是验证
                if cur_event_flow.flow_num + 1 == 3:
                    next_event_flow = procedures_models.event_flow.objects.get(flow_num__exact=2)
                    cur_event_next_people.event_flow = next_event_flow
                    cur_event_next_people.save()
                    ############################设置微信提醒信息##########################
                    # 设置微信提醒信息
                    title = '您提交的事件已处理，但未解决'
                    print(title)
                    descrip = '<div class="normal">关联设备:【%s】<br>事件类型:【%s】<br>事件主题:【%s】</div>' % (
                    cur_event.device, cur_event.event_type, cur_event.event_theme,)
                    url = 'http://10.254.30.251/procedures/need_deal/'
                    # 获取微信提醒信息
                    PURL = wechat_api.GetUrl('wx690cf81ebd6fdf40', '6Sv1dIvSPAyZDobvpbde7WMgBj7uy9u5eEdGvXGoyyo')
                    # 获取需要通知的人员
                    touser = cur_event.event_create_people.wechat
                    # 发送提醒信息
                    wechat_api.SendTextcard(title, descrip, PURL, url, touser)
                    ####################################################################
                # 如果当前为在最后一步
                elif cur_event_flow.flow_num + 1 > 3:
                    next_event_flow = procedures_models.event_flow.objects.get(flow_num__exact=2)
                    cur_event_next_people.event_flow = next_event_flow
                    cur_event_next_people.save()
                    ############################设置微信提醒信息##########################
                    # 设置微信提醒信息
                    title = '您处理的事件审核未通过,请重新处理'
                    print(title)
                    descrip = '<div class="normal">关联设备:【%s】<br>事件类型:【%s】<br>事件主题:【%s】</div>' % (
                        cur_event.device, cur_event.event_type, cur_event.event_theme,)
                    url = 'http://10.254.30.251/procedures/need_deal/'
                    # 获取微信提醒信息
                    PURL = wechat_api.GetUrl('wx690cf81ebd6fdf40', '6Sv1dIvSPAyZDobvpbde7WMgBj7uy9u5eEdGvXGoyyo')
                    # 获取需要通知的人员
                    touser = cur_event.event_deal_people.wechat
                    # 发送提醒信息
                    wechat_api.SendTextcard(title, descrip, PURL, url, touser)
                    ####################################################################
        #返回我的待办页面
        return  redirect('/procedures/need_deal/')
    else:
        uf = procedures_forms.DealEventForm()
        return render_to_response('procedures/deal_event.html',
                                  {
                                      'userinfo':userinfo,
                                      'all_need_deal': all_need_deal,
                                      'cur_event':cur_event,
                                      'cur_deal_event':cur_deal_event,
                                      'uf':uf,
                                  }
                                  )


@login_check
#添加变更信息
def add_change(req,*args,**kwargs):
    userinfo,all_need_deal =get_login_user_info(req)
    #查找当前用户
    user = account_models.UserProfile.objects.get(id__exact=userinfo.id)

    #处理POST来的数据
    if req.method == 'POST':
        #获取表单post的数据
        uf = procedures_forms.ChangeForm(req.POST)
        #如果表单数据合法
        if uf.is_valid():
            #将数据保存在change变量中
            change = uf.save(commit=False)
            #绑定当前的用户信息
            change.change_create_people = user
            #获取当前变更流程的第一步
            change_flow = procedures_models.change_flow.objects.all().order_by('flow_num')
            change.change_flow = change_flow[0]
            #设置当前变更的状态为处理中（2）
            change.change_flag = 2
            #将数据提交至数据库中
            change.save()

            procedures_models.change_deal_info.objects.create(
                change_info=change,
                change_flow=change_flow[0],
                change_people=user,
                change_action=2,
                change_note='',
            )

            procedures_models.change_next_people.objects.create(
                change_info = change,
                change_flow = change_flow[1],
            )
            ############################设置微信提醒信息##########################
            # 设置微信提醒信息
            title = '您有待审批的变更'
            descrip = '<div class="normal">关联设备:【%s】<br>事件类型:【%s】<br>事件主题:【%s】<br>申请人员:【%s】</div>' % (
                change.change_device, change.change_type, change.change_theme,change.change_create_people.name)
            url = 'http://10.254.30.251/procedures/need_deal/'
            # 获取微信提醒信息
            PURL = wechat_api.GetUrl('wx690cf81ebd6fdf40', '6Sv1dIvSPAyZDobvpbde7WMgBj7uy9u5eEdGvXGoyyo')
            # 获取需要通知的人员
            tousers = change_flow[1].flow_role.all()
            for touser in tousers:
                print(touser)
                # 发送提醒信息
                wechat_api.SendTextcard(title, descrip, PURL, url, touser.wechat)
            ####################################################################
            return redirect('/procedures/index/')


    #如果是GET，则返回添加变更的页面
    else :
        uf = procedures_forms.ChangeForm()
        return render_to_response('procedures/add_change.html',
                                  {
                                      'userinfo':userinfo,
                                      'all_need_deal':all_need_deal,
                                      'uf':uf
                                  }
                                  )



@login_check
#展示变更信息表
def show_change(req,*args,**kwargs):
    userinfo,all_need_deal =get_login_user_info(req)
    get_change = procedures_models.change_info.objects.order_by('-id')[0:50].all()
    get_change_num = len(get_change)
    paginator = Paginator(get_change, 10)
    page_num = paginator.num_pages
    page = req.GET.get('page')
    try:
        customer = paginator.page(page)
    except PageNotAnInteger:
        customer = paginator.page(1)
    except EmptyPage:
        customer = paginator.page(paginator.num_pages)
    return render_to_response('procedures/show_change.html',
                              {
                                  'userinfo':userinfo,
                                  'all_need_deal': all_need_deal,
                                  'get_change':get_change,
                                  'get_change_num': get_change_num,
                                  'page_num': page_num,
                                  'customer': customer,
                               }
                              )

@login_check
#展示变更信息表
def show_event(req,*args,**kwargs):
    userinfo,all_need_deal =get_login_user_info(req)
    get_event = procedures_models.event_info.objects.all().order_by('-id')[0:50]
    get_event_num = len(get_event)
    paginator = Paginator(get_event, 10)
    page_num = paginator.num_pages
    page = req.GET.get('page')
    try:
        customer = paginator.page(page)
    except PageNotAnInteger:
        customer = paginator.page(1)
    except EmptyPage:
        customer = paginator.page(paginator.num_pages)
    return render_to_response('procedures/show_event.html',
                              {
                                  'userinfo':userinfo,
                                  'all_need_deal': all_need_deal,
                                  'get_event':get_event,
                                  'get_event_num': get_event_num,
                                  'page_num': page_num,
                                  'customer': customer,

                              }
                              )


@login_check
#展示处理中的工单
def have_deal(req,*args,**kwargs):
    userinfo,all_need_deal =get_login_user_info(req)
    #获取与当前用户相关的流程
    get_change = procedures_models.change_info.objects.filter(change_flag__exact=2).order_by('-id')[0:50]
    get_event = procedures_models.event_info.objects.filter(event_flag__exact=2).order_by('-id')[0:50].values(
        'device',
        'event_theme',
        'event_type__name',
        'event_create_people__name',
        'event_flow__flow_name',
        'event_start_time',
    )
    print(list(get_event))
    get_change_num = len(get_change)
    paginator = Paginator(get_change, 10)
    page_num = paginator.num_pages
    page = req.GET.get('page')
    try:
        customer = paginator.page(page)
    except PageNotAnInteger:
        customer = paginator.page(1)
    except EmptyPage:
        customer = paginator.page(paginator.num_pages)
    return render_to_response('procedures/have_deal.html',
                              {
                                  'userinfo':userinfo,
                                  'all_need_deal': all_need_deal,
                                  'get_change_num': get_change_num,
                                  'page_num': page_num,
                                  'customer': customer,
                              }
                              )



@login_check
#展示显示审批未通过的工单
def have_failed(req,*args,**kwargs):
    userinfo,all_need_deal =get_login_user_info(req)
    #获取与当前用户相关的流程
    get_change = procedures_models.change_info.objects.filter(change_flag__exact=1).order_by('-id')[0:50]
    get_change_num = len(get_change)
    paginator = Paginator(get_change, 10)
    page_num = paginator.num_pages
    page = req.GET.get('page')
    try:
        customer = paginator.page(page)
    except PageNotAnInteger:
        customer = paginator.page(1)
    except EmptyPage:
        customer = paginator.page(paginator.num_pages)
    return render_to_response('procedures/have_failed.html',
                              {'userinfo':userinfo,
                               'all_need_deal': all_need_deal,
                               'get_change_num': get_change_num,
                               'page_num': page_num,
                               'customer': customer,
                               }
                              )





@login_check
#展示成功完结的工单
def have_finished_change(req,*args,**kwargs):
    userinfo,all_need_deal =get_login_user_info(req)
    #获取与当前用户相关的流程
    get_change = procedures_models.change_info.objects.filter(change_flag__exact=3).order_by('-id')[0:50]
    get_change_num = len(get_change)
    paginator = Paginator(get_change, 10)
    page_num = paginator.num_pages
    page = req.GET.get('page')
    try:
        customer = paginator.page(page)
    except PageNotAnInteger:
        customer = paginator.page(1)
    except EmptyPage:
        customer = paginator.page(paginator.num_pages)
    return render_to_response('procedures/have_finished_change.html',
                              {
                                  'userinfo':userinfo,
                                  'all_need_deal': all_need_deal,
                                  'get_change':get_change,
                                  'get_change_num': get_change_num,
                                  'page_num': page_num,
                                  'customer': customer,
                              }
                              )


@login_check
#展示显示变更的详细信息
def show_change_info(req,changeid,**kwargs):
    userinfo,all_need_deal =get_login_user_info(req)
    #获取当前事件的摘要信息
    # 获取当前工单
    cur_change = procedures_models.change_info.objects.get(id__exact=changeid)
    # 获取当前处理明细，用于页面展示处理流程
    cur_deal_change = procedures_models.change_deal_info.objects.filter(change_info__exact=cur_change)
    return render_to_response('procedures/show_change_info.html',
                              {'userinfo':userinfo,
                               'all_need_deal': all_need_deal,
                               'cur_change':cur_change,
                               'cur_deal_change':cur_deal_change,
                               }
                              )



@login_check
#展示显示事件的详细信息
def show_event_info(req,eventid,**kwargs):
    userinfo,all_need_deal =get_login_user_info(req)
    #获取当前事件的摘要信息
    # 获取当前工单
    cur_event = procedures_models.event_info.objects.get(id__exact=eventid)
    # 获取当前处理明细，用于页面展示处理流程
    cur_deal_event = procedures_models.event_deal_info.objects.filter(event_info__exact=cur_event)
    return render_to_response('procedures/show_event_info.html',
                              {
                                  'userinfo':userinfo,
                                  'cur_event':cur_event,
                                  'cur_deal_event':cur_deal_event,
                               }
                              )