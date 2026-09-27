from django.db import models

# Create your models here.
class Tipo(models.Model):
    tipo = models.CharField(max_length=60)
    descripcion = models.CharField(max_length=60)

    def __str__(self):
        return self.tipo

    class Meta:
        ordering = ('tipo',)

class Subtipo(models.Model):
    subtipo = models.CharField(max_length=60)
    descripcion = models.CharField(max_length=60)

    def __str__(self):
        return self.subtipo

    class Meta:
        ordering = ('subtipo',)

class LibroInformatica(models.Model):

    YES_NO_CHOICES = {('SI','SI'),('NO','NO')}

    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    editorial = models.CharField(max_length=200)
    anyo = models.IntegerField()
    tipo = models.ForeignKey (Tipo, on_delete=models.RESTRICT)
    subtipo = models.ForeignKey (Subtipo, on_delete=models.RESTRICT)
    leido = models.CharField(max_length=2, choices=YES_NO_CHOICES, default='NO')

    def __str__(self):
        return f"{self.titulo} - {self.autor} - {self.editorial}"
    class Meta:
        ordering = ('titulo',)