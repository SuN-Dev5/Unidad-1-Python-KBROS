from django.contrib import admin

# Register your models here.
from .models import Category, Zone , Device, Organization

admin.site.register([Category,Zone, Organization])

admin.site.register(Device)
