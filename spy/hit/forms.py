from django import forms
from django.db.models import fields
from .models import Hit
from user.models import User, Assignments

class HitForm(forms.ModelForm):
    """
    Author: Martin Helmut 
    Des
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['objetivo'].required = True

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
            'objetivo': 'Nombre del objetivo (target)',
            'descripcion': 'Descripción',
        }

class HitUpdateForm(forms.ModelForm):
    """
    Author: Martin Helmut 
    Des
    """

    def __init__(self, user, user_group, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['objetivo'].required = True
        #Boss puede asignar a todos, excepto a sí mismo y a usuarios inactivos
        if user_group == 1:
            active_hitmen = User.objects.exclude(id=user.id).filter(is_active=True)
        
        #Manager puede asignar a sus lacayos, excepto a sí mismo y a usuarios inactivos
        elif user_group == 2:
            lackays_list = list(Assignments.objects.filter(manager__in = user).values_list('lacayo_id', flat=True))
            active_hitmen = User.objects.exclude(id=user.id).filte(id__in = lackays_list).filter(is_active=True)

        self.fields['asignacion_disponible'] = forms.ModelChoiceField(queryset=active_hitmen)
        self.fields['asignacion_disponible'].required = False
    class Meta:
        model = Hit
        exclude = ['creador', 'asignacion']

        
        widgets = {
            'asignacion': forms.Select(),
            'objetivo': forms.TextInput(attrs={'class': 'input'}),
            'creador': forms.Select(),
            'estado': forms.Select(),
            'descripcion': forms.Textarea(attrs={'class': 'input'}),
        }

        labels = {
            'asignacion': 'Cambiar asignación',
            'objetivo': 'Nombre del objetivo (target)',
            'descripcion': 'Descripción',
            'estado':'Estado del hit',
            'creador': 'Creado por'
        }