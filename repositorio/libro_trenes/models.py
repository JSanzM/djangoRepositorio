from django.db import models

# Create your models here.
class LibroTrenes(models.Model):

    YES_NO_CHOICES = {('SI', 'SI'), ('NO', 'NO')}

    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    editorial = models.CharField(max_length=200)
    anyo = models.IntegerField()
    leido = models.CharField(max_length=2, choices=YES_NO_CHOICES, default='NO')

    def __str__(self):
        return f"{self.titulo} - {self.autor} - {self.editorial}"

    class Meta:
        ordering = ('titulo',)