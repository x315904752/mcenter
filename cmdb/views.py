from django.shortcuts import redirect,render_to_response
from account.views import login_check
from cmdb.forms import DeviceForm
from cmdb import models as cmdb_models



# Create your views here.
@login_check
def index(req,*args,**kwargs):

    username = req.session.get('username', None)
    return render_to_response('cmdb/show_device.html', {'username': username})



@login_check
def show_device(req,*args,**kwargs):
    username = req.session.get('username', None)
    # 查询登录用户的相关信息
    asset = cmdb_models.Asset.objects.all()
    print (asset)
    return render_to_response('cmdb/show_device.html', {'username': username,'asset':asset})


@login_check
def add_device(req,*args,**kwargs):
    username = req.session.get('username',None)
    if req.method == 'POST':
        #获取表单post的数据
        uf = DeviceForm(req.POST)

        #验证表单数据是否合法
        if uf.is_valid():

            #获取表单中的数据
            name = uf.cleaned_data['name']
            category_id = uf.cleaned_data['category_id']
            ip = uf.cleaned_data['ip']
            code = uf.cleaned_data['code']
            worth = uf.cleaned_data['worth']
            business_unit = uf.cleaned_data['business_unit']
            remark = uf.cleaned_data['remark']
            userpro = uf.cleaned_data['userpro']
            room = uf.cleaned_data['room']
            guaranteed = uf.cleaned_data['guaranteed']
            production_date = uf.cleaned_data['production_date']
            up_date = uf.cleaned_data['up_date']

            #将数据插入到变更表中
            cmdb_models.Asset.objects.create(
                name = name,
                category_id = cmdb_models.Category.objects.get(id__exact=category_id),
                ip = ip,
                code = code,
                worth = worth,
                business_unit = cmdb_models.Business_unit.objects.get(id__exact=business_unit),
                remark = remark,
                userpro =cmdb_models.UserProfile.objects.get(id__exact=userpro),
                room=cmdb_models.Room.objects.get(id__exact=room),
                guaranteed=guaranteed,
                production_date=production_date,
                up_date = up_date,
                #delete_flag=False,
                )
            return redirect('/cmdb/show_device/')
    else :
        uf = DeviceForm()
        return render_to_response('cmdb/add_device.html',{'username':username,'uf':uf})
