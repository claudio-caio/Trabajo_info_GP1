from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # Sobrescribimos el email para hacerlo único
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.webp', null=True, blank=True)

    pass
    # Opcional: si quieres que el email sea el campo principal para login
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']  # si usas email como login

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.username