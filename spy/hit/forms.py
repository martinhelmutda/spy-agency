from django import forms
from django.db.models import fields
from .models import Hit
from user.models import User, Assignments

class HitForm(forms.ModelForm):
    """
    Des
    """

    def __init__(self, user, user_group, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_group = user_group
        self.fields['objetivo'].required = True
        #Boss can add hits to everyone active
        if user_group == 1:
            active_hitmen = User.objects.exclude(id=user.id).filter(is_active=True)
        
        #Manager can add hits to active lackeys and not to himself
        elif user_group == 2:
            lackeys_list = list(Assignments.objects.filter(manager__in = [user]).values_list('lacayo_id', flat=True))
            active_hitmen = User.objects.exclude(id=user.id).filter(id__in = lackeys_list).filter(is_active=True)

        self.fields['asignacion'] = forms.ModelChoiceField(queryset=active_hitmen)
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
        
        self.user_group = user_group
        active_hitmen = User.objects.none()
        #Boss can add hits to everyone active
        if user_group == 1:
            active_hitmen = User.objects.exclude(id=user.id).filter(is_active=True)
        
        #Manager can add hits to active lackeys and not to himself
        elif user_group == 2:
            lackays_list = list(Assignments.objects.filter(manager__in = [user]).values_list('lacayo_id', flat=True))
            active_hitmen = User.objects.exclude(id=user.id).filter(id__in = lackays_list).filter(is_active=True)

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
    
    def clean(self):
        #Protect data modification is HTML is modified
        self.cleaned_data = super().clean()
        print("Limpiando ando", self.instance.descripcion)
        if self.instance.estado != 1:
            self.cleaned_data['estado'] = self.instance.estado
        if self.user_group == 3:
            self.cleaned_data['descripcion'] = self.instance.descripcion
            self.cleaned_data['objetivo'] = self.instance.objetivo
        
        return self.cleaned_data


class HitBuilkForm(forms.ModelForm):
    """
    Author: Martin Helmut 
    Des
    """

    def __init__(self, user, user_group, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("US", user, user_group)
        self.user_group = user_group
        active_hitmen = User.objects.none()

        #Boss can add hits to everyone active
        if user_group == 1:
            active_hitmen = User.objects.exclude(id=user.id).filter(is_active=True)
        
        #Manager can add hits to active lackeys and not to himself
        elif user_group == 2:
            lackays_list = list(Assignments.objects.filter(manager__in = [user]).values_list('lacayo_id', flat=True))
            active_hitmen = User.objects.exclude(id=user.id).filter(id__in = lackays_list).filter(is_active=True)

        self.fields['asignacion_disponible'] = forms.ModelChoiceField(queryset=active_hitmen)
        self.fields['asignacion_disponible'].required = False

        hits_available = Hit.objects.filter(estado=1)
        self.fields['hits'] = forms.ModelMultipleChoiceField(queryset=hits_available)
        self.fields['hits'].required = True
    class Meta:
        model = Hit
        fields = []
    