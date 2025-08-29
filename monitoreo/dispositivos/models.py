from django.db import models

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