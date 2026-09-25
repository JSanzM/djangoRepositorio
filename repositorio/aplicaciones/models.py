from django.db import models

# Create your models here.


class Origen(models.Model):
    origen = models.CharField(max_length=100)
    def __str__(self):
        return self.origen

class Aplicaciones(models.Model):

    YES_NO_CHOICES = {('SI', 'SI'), ('NO', 'NO')}

    aplicacion = models.CharField(max_length=200)
    origen = models.ForeignKey(Origen, on_delete=models.CASCADE)
    instalar = models.CharField(max_length=2, choices=YES_NO_CHOICES, default='SI')
    favoritos = models.CharField(max_length=2, choices=YES_NO_CHOICES, default='NO')
    notas = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.aplicacion} - {self.origen} - {self.instalar} - {self.favoritos}"

    class Meta:
        ordering = ['aplicacion']