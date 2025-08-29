from django.db import models

class Dispositivo(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete= models.CASCADE)
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)
    prim_consumo = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return self.nombre

 #feature/modelos_alerta_medicion_Seba
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

# feature/modelos_categoria_zona_Gabo
# Tus modelos: Categoria y Zona
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Zona(models.Model):
    nombre = models.CharField(max_length=50, unique=True)


    def __str__(self):
        return self.nombre
 main
