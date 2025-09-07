from django.contrib import admin

# Register your models here.
from .models import Category, Zone , Device

admin.site.register([Category,Zone])

admin.site.register(Device)
