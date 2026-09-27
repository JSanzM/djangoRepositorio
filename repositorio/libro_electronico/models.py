from django.db import models

# Create your models here.
class LibroElectronico(models.Model):

    YES_NO_CHOICES = {('SI','SI'),('NO','NO')}

    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    serie = models.CharField(max_length=200)
    bajado = models.CharField(max_length=2, choices=YES_NO_CHOICES, default='NO')
    notas = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.titulo} - {self.autor} - {self.serie}"
    class Meta:
        ordering = ('autor','serie','titulo',)