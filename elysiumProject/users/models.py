from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Create your models here.
# models.py


class CustomUserManager(BaseUserManager):
    def create_user(self, cedula, nombre, apellidos, correo, password, tipoDeAfiliacion, **extra_fields):
        if not cedula:
            raise ValueError(('El usuario debe tener una cédula'))
        if not correo:
            raise ValueError(('El usuario debe tener un correo electrónico'))

        correo = self.normalize_email(correo)
        user = self.model(cedula=cedula, nombre=nombre, apellidos=apellidos, correo=correo, tipoDeAfiliacion=tipoDeAfiliacion, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cedula, nombre, apellidos, correo, password, tipoDeAfiliacion, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(cedula, nombre, apellidos, correo, password, tipoDeAfiliacion, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    cedula = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    IPS = models.CharField(max_length=50)
    correo = models.EmailField(unique=True)
    tipoDeAfiliacion = models.CharField(max_length=10)  # Puede ser un campo de elección si tienes valores específicos

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'cedula'
    REQUIRED_FIELDS = ['nombre', 'apellidos', 'correo', 'tipoDeAfiliacion']

    def __str__(self):
        return f"{self.cedula} - {self.nombre}"
