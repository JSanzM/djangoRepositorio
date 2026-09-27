from django.db import models

from aplicaciones.models import Origen

class TipoJuego(models.Model):
    tipoJuego = models.CharField(max_length=200)
    def __str__(self):
        return f"{self.tipoJuego}"
    class Meta:
        ordering = ['tipoJuego']

# Create your models here.
class Juegos(models.Model):

    YES_NO_CHOICES = {('SI', 'SI'), ('NO', 'NO')}

    nombre = models.CharField(max_length=200)
    tipoJuego = models.ForeignKey(TipoJuego, on_delete=models.CASCADE)
    instalar = models.CharField(max_length=2, choices=YES_NO_CHOICES, default='SI')
    origen = models.ForeignKey(Origen, on_delete=models.CASCADE)
    notas = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.tipoJuego} - {self.origen}"

    class Meta:
        ordering = ['nombre']