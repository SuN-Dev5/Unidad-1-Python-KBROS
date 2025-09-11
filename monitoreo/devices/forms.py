from django import forms
from .models import Device, Measurement
from django.contrib.auth.models import User

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'category', 'zone' , 'maximum_consumption' , 'organization' ,'status']
        
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['device', 'consumption', 'organization']
        widgets = {
            'device': forms.Select(attrs={'class': 'form-control'}),
            'consumption': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'organization': forms.Select(attrs={'class': 'form-control'}),
        }