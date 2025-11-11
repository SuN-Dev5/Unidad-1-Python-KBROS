from django.contrib import admin
from .models import Profile

# Esto registra tu modelo Profile en el panel de admin
admin.site.register(Profile)