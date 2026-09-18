from django.db import models

# Create your models here.
class Grupo(models.Model):
    grupo = models.CharField(max_length=100)
    def __str__(self):
        return self.grupo

class Tipo(models.Model):
    tipo = models.CharField(max_length=100)
    def __str__(self):
        return self.tipo


class Cds(models.Model):

    YES_NO_CHOICES = {('SI', 'SI'), ('NO', 'NO')}

    titulo = models.CharField(max_length=200)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    anyo = models.IntegerField()
    notas = models.CharField(max_length=100, blank=True, null=True)
    copiado = models.CharField(max_length=2, choices=YES_NO_CHOICES, default='NO')
    falta = models.CharField(max_length=2, choices=YES_NO_CHOICES, default='SI')
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.titulo} -  {self.grupo.grupo}"

    class Meta:
        ordering = ('grupo', 'titulo',)
