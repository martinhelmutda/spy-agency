from django import forms
from django.db.models import fields
from .models import Hit

class HitForm(forms.ModelForm):
    """
    Author: Martin Helmut 
    Des
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Hit
        exclude = ['creador', 'estado']

        widgets = {
            'asignacion': forms.Select(),
            'objetivo': forms.TextInput(attrs={'class': 'input'}),
            'creador': forms.Select(),
            'estado': forms.Select(),
            'descripcion': forms.Textarea(attrs={'class': 'input'}),
        }

        labels = {
            'asignacion': 'Asignado a',
            'objetivo': 'Nombre del objetivo',
            'descripcion': 'Descripción',
        }