from django.db import models

# Create your models here.
class Dispositivo(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey("Categoria", on_delete= models.CASCADE)
    zona = models.ForeignKey("Zona", on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)
    prim_consumo = models.DecimalField(max_digits=10, decimal_places=3)



    def __str__(self):
        return self.nombre