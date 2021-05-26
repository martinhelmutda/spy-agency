from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    descripcion = models.CharField(max_length=1800, null=True, blank=True)
    estado = models.BooleanField(default=True)
    lacayos = models.ManyToManyField("self",through='Assignments', symmetrical=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Assignments(models.Model):
    manager = models.ForeignKey(User, verbose_name='manager_de', related_name="manager_de", on_delete=models.CASCADE) 
    lacayo = models.ForeignKey(User, verbose_name='lacayo_de',related_name="lacayo_de",  on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
