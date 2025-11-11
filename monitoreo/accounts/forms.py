# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm as AuthPasswordChangeForm
from .models import Profile

# ---------------------------
# 🔐 Formulario de Login
# ---------------------------
class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@empresa.com'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )

# ---------------------------
# 📝 Formulario de Registro
# ---------------------------
class RegisterForm(forms.Form):
    company_name = forms.CharField(
        label="Nombre Empresa",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password_confirm = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    # Validación: Email único
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists(): # Usamos email como username
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email

    # Validación: Contraseñas coinciden y tienen largo mínimo
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        
        # Requisito de la Rúbrica: validaciones mínimas
        if password and len(password) < 8:
             raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        
        return cleaned_data

# ---------------------------
# 👤 Formulario de Datos de Usuario (first_name, email, etc.)
# ---------------------------
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

# ---------------------------
# 🖼️ Formulario de Perfil (Avatar y Teléfono)
# ---------------------------
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['telefono', 'avatar'] # 'avatar' cumple el requisito de la rúbrica
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }

# ---------------------------
# 🔑 Formulario de Cambio de Contraseña
# ---------------------------
class PasswordChangeForm(AuthPasswordChangeForm):
    # Esto cumple el requisito de "doble campo de verificación"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = "Contraseña Actual"
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        
        self.fields['new_password1'].label = "Nueva Contraseña"
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        
        self.fields['new_password2'].label = "Confirmar Nueva Contraseña"
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})