from django import forms

from .models import LibroElectronico


class LibroElectronicoForm(forms.ModelForm):
    class Meta:
        model = LibroElectronico
        fields = ['titulo', 'autor', 'serie', 'bajado', 'notas']
        labels = {
            'titulo': 'Título',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'serie': forms.TextInput(attrs={'class': 'form-control'}),
            'bajado': forms.Select(attrs={'class': 'form-control'}),
            'notas': forms.TextInput(attrs={'class': 'form-control'}),
        }
