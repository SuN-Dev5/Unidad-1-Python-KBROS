from django import forms
from .models import Device
from django.contrib.auth.models import User

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'category', 'zone' , 'maximum_consumption' , 'organization' ,'status']
        
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']