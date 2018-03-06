from django.shortcuts import render,render_to_response
from sdksy import models as sdksy_models
# Create your views here.


def index(req,*args,**kwargs):
    return render_to_response('sdksy/index.html')


def today(req,*args,**kwargs):
    business = sdksy_models.business.objects.all()

    return render_to_response(
        'sdksy/today.html',
        {
            'business':business,
        }
    )


def tomorrow(req,*args,**kwargs):
    return render_to_response('sdksy/tomorrow.html')