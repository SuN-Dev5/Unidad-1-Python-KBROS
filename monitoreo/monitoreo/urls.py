# monitoreo/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include  # <-- Asegúrate de importar 'include'

#
# ¡No más importaciones de vistas aquí!
#

urlpatterns = [
    path('admin/', admin.site.urls),

    # 1. Conecta todas las URLs de autenticación y perfil
    path('', include('accounts.urls')),
    
    # 2. Conecta todas las URLs de la app (dashboard, CRUDs, etc.)
    path('', include('devices.urls')),
]

# Dejamos esto al final para que funcionen los avatares
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)