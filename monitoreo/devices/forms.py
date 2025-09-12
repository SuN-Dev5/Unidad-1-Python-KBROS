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
        widgets ={'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})}

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['device', 'consumption', 'organization']
        widgets = {
            'device': forms.Select(attrs={'class': 'form-control'}),
            'consumption': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'organization': forms.Select(attrs={'class': 'form-control'}),
        }
def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'organization'):
            self.fields['device'].queryset = Device.objects.filter(organization=user.organization)
            self.fields['organization'].initial = user.organization
