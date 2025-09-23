from django import forms
from .models import Device, Measurement, Alert
from django.contrib.auth.models import User


# ---------------------------
# 📌 Device Form
# ---------------------------
class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'category', 'zone', 'maximum_consumption', 'organization', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'zone': forms.Select(attrs={'class': 'form-control'}),
            'maximum_consumption': forms.NumberInput(attrs={'class': 'form-control'}),
            'organization': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


# ---------------------------
# 👤 User Update Form
# ---------------------------
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }


# ---------------------------
# 📏 Measurement Form
# ---------------------------
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


# ---------------------------
# 🚨 Alert Form
# ---------------------------
class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ['device', 'message', 'severity', 'organization']
        widgets = {
            'device': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'maxlength': 200}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'organization': forms.Select(attrs={'class': 'form-control'}),
        }
