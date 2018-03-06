from django.shortcuts import render,render_to_response

# Create your views here.



def index(req,*args,**kwargs):
    username = req.session.get('username', None)
    return render_to_response('monitor/index.html',{'username':username})



def device(req,*args,**kwargs):
    username = req.session.get('username', None)
    return render_to_response('monitor/device.html', {'username':username})



def vm(req,*args,**kwargs):
    username = req.session.get('username', None)
    return render_to_response('monitor/vm.html',{'username':username})


def link(req,*args,**kwargs):
    username = req.session.get('username', None)
    return render_to_response('monitor/link.html',{'username':username})


def web(req,*args,**kwargs):
    username = req.session.get('username', None)
    return render_to_response('monitor/web.html',{'username':username})
