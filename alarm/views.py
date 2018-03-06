from django.shortcuts import render,render_to_response

# Create your views here.




def index(req,*args,**kwargs):
    username = req.session.get('username', None)
    return render_to_response('alarm/index.html',{'username':username})