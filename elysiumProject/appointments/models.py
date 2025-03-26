from django.db import models
from users.models import CustomUser
# Create your models here.

class Doctor(models.Model):
    nombre = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=50)
    IPS = models.CharField(max_length=50)
    correo = models.EmailField(unique=True)
    cedula = models.CharField(max_length=20, unique=True)
    especialidad = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} - {self.especialidad}"

class Appointment(models.Model):
    doctorId = models.ForeignKey(Doctor, on_delete=models.CASCADE) 
    userId = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    tipoCita = models.CharField(max_length=75)
    fechaInicio = models.DateTimeField()
    fechaFin = models.DateTimeField()

    
