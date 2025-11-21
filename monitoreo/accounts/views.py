# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Importamos los formularios
from .forms import (
    LoginForm, 
    RegisterForm, 
    UserUpdateForm, 
    ProfileUpdateForm, 
    PasswordChangeForm
)

# 💡 ¡AÑADIDO! Importar el modelo Profile para el fix
from .models import Profile 

# Importamos 'Organization' desde la app 'devices'
from devices.models import Organization

# ---------------------------
# 🔐 Autenticación y Perfil
# ---------------------------

def login_view(request):
    """Maneja el inicio de sesión."""
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        # Usamos el email como username para autenticar
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            # Usamos messages para mostrar errores
            messages.error(request, 'Email o contraseña incorrectos.')
    
    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    """Maneja el registro de nuevos usuarios y organizaciones."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        company_name = form.cleaned_data.get('company_name')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        try:
            # Creamos el usuario
            user = User.objects.create_user(
                username=email,  # Usamos email como username
                email=email,
                password=password,
                first_name=company_name
            )
            
            # 🔹 Crear organización asociada (como lo tenías)
            # (Nota: Esto creará un perfil gracias a la signal en models.py)
            Organization.objects.create(name=company_name)

            messages.success(request, f'¡Registro exitoso! La empresa {company_name} ha sido registrada.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error al registrar la empresa: {e}')

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def logout_view(request):
    """Maneja el cierre de sesión."""
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect("login")


@login_required
def profile_view(request):
    """
    Vista para editar el perfil (datos de usuario y avatar)
    y para cambiar la contraseña.
    """
    
    # ==================================================
    # == FIX (Reparación del Error 500)
    # == Obtenemos el perfil, o lo creamos si no existe
    # == para usuarios antiguos que no lo tengan.
    # ==================================================
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    # Definimos los formularios antes del POST
    password_form = PasswordChangeForm(request.user)
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=profile) # Usamos la variable 'profile'

    if request.method == 'POST':
        # Diferenciamos qué formulario se envió
        if 'update_profile' in request.POST:
            # Formularios de actualización de perfil
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile) # Usamos 'profile'
            
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Tu perfil ha sido actualizado.')
                return redirect('profile')
            else:
                messages.error(request, 'Error al actualizar el perfil. Revisa los campos.')

        elif 'change_password' in request.POST:
            # Formulario de cambio de contraseña
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Importante
                messages.success(request, 'Tu contraseña ha sido cambiada.')
                return redirect('profile')
            else:
                # 💡 FIX: Mostrar error de contraseña
                # Si el form NO es válido, añadimos el mensaje
                # y dejamos que la vista continúe hasta el 'return render'
                messages.error(request, 'Error al cambiar la contraseña. Revisa los campos.')
    
    # Si es GET, o si un POST falló, renderiza la página con los formularios
    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form
    })

def password_reset_view(request):
    """Vista placeholder para reseteo de contraseña (requiere email)."""
    message_sent = False
    if request.method == "POST":
        email = request.POST.get('email')
        # Aquí iría la lógica de envío de email
        message_sent = True
    return render(request, 'accounts/password_reset.html', {'message_sent': message_sent})