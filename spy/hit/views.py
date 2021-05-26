from django.contrib.auth.models import Group
from django.shortcuts import render
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.list import ListView
from .models import Hit
from user.models import Assignments 
from .forms import HitForm
from django.urls import reverse

# Create your views here.

class HitsList(ListView):
    model = Hit

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        grupo = Group.objects.get(user=current_user).id
        context['grupo']= grupo

        #boss
        if grupo == 1:
            hits =  Hit.objects.all()

        #manager
        elif grupo == 2:
            #Lacayos del usuario actual
            lackeys = list(Assignments.objects.filter(manager__in = [current_user]).values_list('id', flat=True))
            #Eliminarse a sí mismo de la segunda lista
            lackeys.pop(current_user.id)
            hits =  Hit.objects.filter(asignacion_id__in=lackeys)

        context['my_hits'] = Hit.objects.filter(asignacion=current_user)
        context['hits'] = hits

        return context


class HitDetailUpdate(UpdateView):
    pass

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

    def form_valid(self, form):
        #Asignación automática
        form.instance.estado = 1
        form.instance.creador = self.request.user
        return super(HitCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('hit:hit_list')

class HitBulkEdit(FormView):
    pass
