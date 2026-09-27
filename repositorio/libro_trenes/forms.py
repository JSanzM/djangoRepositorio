from django import forms

from .models import LibroTrenes


class LibroTrenesForm(forms.ModelForm):
    class Meta:
        model = LibroTrenes
        fields = ['titulo', 'autor', 'editorial', 'anyo', 'leido']
        labels = {
            'anyo': 'Año',
            'titulo': 'Título',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'editorial': forms.TextInput(attrs={'class': 'form-control'}),
            'anyo': forms.NumberInput(attrs={'class': 'form-control'}),
            'leido': forms.Select(attrs={'class': 'form-control'}),
        }