from django import forms
from procedures import models as procedures_models



#事件表单
class EventForm(forms.ModelForm):
    class Meta:
        model = procedures_models.event_info
        exclude = ['event_start_time','event_create_people','event_flow','event_flag']
        widgets = {
            'event_type':forms.Select(attrs={'class':'style5'}),
            'device':forms.TextInput(attrs={'class':'style5'}),
            'event_theme':forms.Textarea(attrs={'cols': '90', 'rows': '4'}),
            'change_target' : forms.Textarea(attrs={'cols': '90', 'rows': '4'}),
            'event_description' : forms.Textarea(attrs={'cols': '90', 'rows': '7'}),
            'event_deal_people':forms.Select(attrs={'class':'style5'}),
        }


#变更表单
class ChangeForm(forms.ModelForm):
    class Meta:
        model = procedures_models.change_info
        exclude = ['change_verify_people','change_create_people','change_flow','change_flag']
        widgets = {
            'change_type':forms.Select(attrs={'class':'style5'}),
            'change_partner':forms.SelectMultiple(attrs={'style':'width:232px'}),
            'device':forms.TextInput(attrs={'class':'style5'}),
            'change_theme':forms.Textarea(attrs={'cols': '90', 'rows': '4'}),
            'change_target' : forms.Textarea(attrs={'cols': '90', 'rows': '4'}),
            'change_plan' : forms.Textarea(attrs={'cols': '90', 'rows': '7'}),
            'change_back' : forms.Textarea(attrs={'cols': '90', 'rows': '7'}),
            'change_note' : forms.Textarea(attrs={'cols': '90', 'rows': '7'}),
        }


class DealChangeForm(forms.ModelForm):
    class Meta:
        change_action_list = (
            (1, '同意'),
            (0, '不同意'),
        )
        model = procedures_models.change_deal_info
        fields = ['change_action','change_note']
        widgets = {
            'change_action': forms.Select(choices=change_action_list),
            'change_note': forms.Textarea(attrs={'cols': '90', 'rows': '4'}),
        }


class DealEventForm(forms.ModelForm):
    class Meta:
        change_action_list = (
            (1, '已完成'),
            (0, '未完成'),
        )
        model = procedures_models.event_deal_info
        fields = ['event_action','event_note']
        widgets = {
            'event_action': forms.Select(choices=change_action_list),
            'event_note': forms.Textarea(attrs={'cols': '90', 'rows': '4'}),
        }


class DealChangeVerifyPeopleForm(forms.ModelForm):
    class Meta:
        model = procedures_models.change_info
        fields = ['change_verify_people']
        # widgets = {
        #     'change_verify_people': forms.Select(),
        # }