from django.db import models
from user.models import User

HIT_STATUS = ((1,'Asignado'),(2,'Fallido'), (3,'Completado'))

class Hit(models.Model):
    asignacion = models.ForeignKey(User, related_name="Asignado", on_delete=models.CASCADE, null=True)
    objetivo = models.CharField(max_length=800, null=True, blank=True)
    descripcion = models.CharField(max_length=800, null=True, blank=True)
    estado = models.IntegerField(choices=HIT_STATUS)
    creador = models.ForeignKey(User, related_name="HitCreadoPor", on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return self.descripcion