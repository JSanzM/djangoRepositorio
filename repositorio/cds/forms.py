from django import forms

from .models import Cds


class CdsForm(forms.ModelForm):
    class Meta:
        model = Cds
        fields = ['titulo', 'grupo', 'anyo', 'copiado', 'falta', 'tipo', 'notas']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'grupo': forms.Select(attrs={'class': 'form-control'}),
            'anyo': forms.NumberInput(attrs={'class': 'form-control'}),
            'copiado': forms.Select(attrs={'class': 'form-control'}),
            'falta': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'notas': forms.TextInput(attrs={'class': 'form-control'}),
        }
