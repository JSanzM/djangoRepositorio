from django import forms

from .models import LibroInformatica


class LibroForm(forms.ModelForm):
    class Meta:
        model = LibroInformatica
        fields = ['titulo', 'autor', 'editorial', 'anyo', 'tipo', 'subtipo', 'leido']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'editorial': forms.TextInput(attrs={'class': 'form-control'}),
            'anyo': forms.NumberInput(attrs={'class': 'form-control'}),
            'leido': forms.Select(attrs={'class': 'form-control'}),
        }
