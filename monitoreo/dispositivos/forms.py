from django import forms
from .models import Dispositivo

class DispositivoForm(forms.ModelForm):
    class Meta:
        model = Dispositivo
        fields = ['nombre', 'categoria', 'zona' , 'estado', 'prim_consumo']