from django.db import models

# Create your models here.
class Medicion(models.Model):
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    consumo = models.DecimalField(max_digits=10, decimal_places=3)
    tomada_en = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.dispositivo} - {self.consumo}"

class Alerta(models.Model):
    dispositivo = models.ForeignKey(Dispositivo,on_delete=models.CASCADE)
    mensaje = models.CharField(max_length=150)
    creada_en = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.dispositivo} - {self.mensaje}"
