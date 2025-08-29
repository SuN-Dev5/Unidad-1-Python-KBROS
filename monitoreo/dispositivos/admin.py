from django.contrib import admin

# Register your models here.
from .models import Categoria, Zona , Dispositivo

admin.site.register([Categoria,Zona])

admin.site.register(Dispositivo)
