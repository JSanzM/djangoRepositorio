from django import forms

from .models import Aplicaciones


class AplicacionesForm(forms.ModelForm):
    class Meta:
        model = Aplicaciones
        fields = ('aplicacion', 'origen', 'instalar', 'favoritos', 'notas')
        widgets = {
            'aplicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'origen': forms.Select(attrs={'class': 'form-control'}),
            'instalar': forms.Select(attrs={'class': 'form-control'}),
            'favoritos': forms.Select(attrs={'class': 'form-control'}),
            'notas': forms.TextInput(attrs={'class': 'form-control'}),
        }