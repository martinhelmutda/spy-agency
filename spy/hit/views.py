from django.contrib.auth.models import Group
from django.shortcuts import render
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.list import ListView
from .models import Hit
from user.models import Assignments 
from .forms import HitForm, HitUpdateForm
from django.urls import reverse

# Create your views here.

class HitsList(ListView):
    model = Hit

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        grupo = Group.objects.get(user=current_user).id
        context['grupo']= grupo
        hits = []
        
        #boss
        if grupo == 1:
            hits =  Hit.objects.all()

        #manager
        elif grupo == 2:
            #Lacayos del usuario actual
            lackeys = list(Assignments.objects.filter(manager__in = [current_user]).values_list('lacayo_id', flat=True))
            #Eliminarse a sí mismo de la segunda lista
            lackeys.pop(current_user.id)
            hits =  Hit.objects.filter(asignacion_id__in=lackeys)

        context['my_hits'] = Hit.objects.filter(asignacion=current_user)
        context['hits'] = hits

        return context


class HitDetailUpdate(UpdateView):
    model = Hit
    form_class = HitUpdateForm
    template_name_suffix = '_update_form'

    def get_context_data(self, **kwargs):
        context = super(HitDetailUpdate, self).get_context_data(**kwargs)
        return context

    def get_form_kwargs(self):
        kwargs = super(HitDetailUpdate, self).get_form_kwargs()
        user = self.request.user
        user_group = Group.objects.get(user=user).id
        if hasattr(self, 'object'):
            kwargs.update({'user': user, 'user_group':user_group})
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(HitDetailUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse('hit:hits_list')

class HitCreate(CreateView):
    """
    Authors: Martin Helmut
    Create new hit.
    """
    model = Hit
    form_class = HitForm

    def get_context_data(self, **kwargs):
        context = super(HitCreate, self).get_context_data(**kwargs)
        return context
    
    def get_form_kwargs(self):
        kwargs = super(HitCreate, self).get_form_kwargs()
        user = self.request.user
        user_group = Group.objects.get(user=user).id
        if hasattr(self, 'object'):
            kwargs.update({'user': user, 'user_group':user_group})
        return kwargs

    def form_valid(self, form):
        #Asignación automática a hitmen
        form.instance.creador = self.request.user
        return super(HitCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('hit:hit_list')

class HitBulkEdit(FormView):
    pass
