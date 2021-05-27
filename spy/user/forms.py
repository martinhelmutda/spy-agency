from django import forms
from django.db.models import fields
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError
from .models import User

class RegistrationForm(UserCreationForm):
    """
    Author: Martin Helmut 
    Des
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email"]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'input'}),
            'password1': forms.TextInput(attrs={'class': 'input'}),
            'password2': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.TextInput(attrs={'class': 'input'}),
        }
class UserUpdateForm(forms.ModelForm):
    """
    Author: Martin Helmut 
    Des
    """

    def __init__(self, user, user_group, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lacayos'].queryset = User.objects.exclude(id=user.id).filter(is_active=True)
        self.fields['lacayos'].required = False

    class Meta:
        model = User
        fields = ["username", "email", "descripcion", "is_active", "lacayos"]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.TextInput(attrs={'class': 'input'}),
            'descripcion': forms.Textarea(attrs={'class': 'input'}),
        }

        labels = {
            'username':'Nombre clave',
            'email':'Correo electrónico',
            'descripcion':'Descripción',
            'is_active':'Usuario activo',
            'lacayos':'Lacayos',
        }
