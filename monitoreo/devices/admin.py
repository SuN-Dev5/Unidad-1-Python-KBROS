from django.contrib import admin

# Register your models here.
from .models import Category, Zone , Device, Organization, Alert, Measurement

admin.site.register([Category,Zone, Organization, Alert, Measurement])

admin.site.register(Device)
