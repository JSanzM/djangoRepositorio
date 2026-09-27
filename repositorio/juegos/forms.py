from django import forms

from juegos.models import Juegos


class JuegosForm(forms.ModelForm):
    class Meta:
        model = Juegos
        fields = ['nombre', 'tipoJuego', 'instalar', 'origen', 'notas']
        widgets =  {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipoJuego': forms.Select(attrs={'class': 'form-control'}),
            'instalar': forms.Select(attrs={'class': 'form-control'}),
            'origen': forms.Select(attrs={'class': 'form-control'}),
            'notas': forms.TextInput(attrs={'class': 'form-control'}),}