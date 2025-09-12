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

class Organization(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(BaseModel):
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Zone(BaseModel):
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Device(BaseModel):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    maximum_consumption = models.IntegerField()  # watts
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Measurement(BaseModel):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    consumption = models.FloatField()  # kWh
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.device} - {self.consumption} kWh"

class Alert(BaseModel):
    SEVERITY_CHOICES = [
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
    ]

    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_CHOICES,
        default='medium'
    )
    date = models.DateTimeField(auto_now_add=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
   

    def __str__(self):
        return f"Alert {self.device} - {self.message}"
    
