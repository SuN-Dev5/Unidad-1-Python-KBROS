from django.db import models

# -----------------------------
# Modelo Base con atributos comunes
# -----------------------------
class BaseModel(models.Model):
    STATUS = [
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
    ]

    status = models.CharField(max_length=10, choices=STATUS, default="ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True)   # se asigna al crear
    updated_at = models.DateTimeField(auto_now=True)       # se actualiza cada vez que se guarda
    deleted_at = models.DateTimeField(null=True, blank=True)  # opcional para borrado lógico

    class Meta:
        abstract = True   # no crea tabla, solo se hereda

# -----------------------------
# Tablas principales
# -----------------------------
class Category(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Zone(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Device(BaseModel):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    maximum_consumption = models.IntegerField()  # watts

    def __str__(self):
        return self.name

class Measurement(BaseModel):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    consumption = models.FloatField()  # kWh

    def __str__(self):
        return f"{self.device} - {self.consumption} kWh"

class Alert(BaseModel):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    mesage = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert {self.device} - {self.mesage}"