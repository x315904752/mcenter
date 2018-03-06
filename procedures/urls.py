"""ItsmCenter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from procedures import views as procedures_views


urlpatterns = [
    url(r'index/',procedures_views.index),
    url(r'service_register/',procedures_views.service_register),
    url(r'add_event/',procedures_views.add_event),
    url(r'add_change/',procedures_views.add_change),
    url(r'need_deal/',procedures_views.need_deal),
    url(r'i_submit/',procedures_views.i_submit),
    url(r'i_joined/',procedures_views.i_joined),
    url(r'i_deal/', procedures_views.i_deal),
    url(r'deal_change/(\d+)/', procedures_views.deal_change),
    url(r'deal_event/(\d+)/',procedures_views.deal_event),
    url(r'show_change_info/(\d+)/', procedures_views.show_change_info),
    url(r'show_event_info/(\d+)/',procedures_views.show_event_info),
    url(r'show_change/',procedures_views.show_change),
    url(r'show_event/',procedures_views.show_event),
    url(r'have_deal/',procedures_views.have_deal),
    url(r'have_failed/',procedures_views.have_failed),
    url(r'have_finished_change/',procedures_views.have_finished_change),
]
