from django.contrib.auth.models import Group
from django.shortcuts import render
from django.views.generic import FormView, RedirectView, UpdateView, CreateView
from django.views.generic.list import ListView
from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from urllib.parse import urlparse
from django.urls import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import User, Assignments
from .forms import RegistrationForm, UserUpdateForm
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.

class LoginView(FormView):
    """
    Author: Martin Helmut 
    """

    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'user/login.html'

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        """
        Returns the view with csrf protection and cache disabled.
        """
        return super(LoginView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        If user is already logged in redirect him with function
        """
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super(LoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        """
        The user has provided valid credentials (this was checked in AuthenticationForm.is_valid()). So now we
        """
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """
        Defines the success url to redirect to
        """
        if self.success_url:
            redirect_to = self.success_url
        else:
            redirect_to = self.request.REQUEST.get(
                self.redirect_field_name, 'hits/')

        netloc = urlparse(redirect_to)[1]

        if not redirect_to:
            redirect_to = settings.LOGIN_REDIRECT_URL
        # Security check -- don't allow redirection to a different host.
        elif netloc and netloc != self.request.get_host():
            redirect_to = settings.LOGIN_REDIRECT_URL
        return redirect_to

    def set_test_cookie(self):
        """
        Sets a cookie to ensure login can be saved.
        """
        self.request.session.set_test_cookie()

    def check_and_delete_test_cookie(self):
        """
        Check if the test cookie works and deletes it.
        """
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True
        return False

    def post(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.post(), but adds test cookie stuff
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            self.check_and_delete_test_cookie()
            return self.form_valid(form)
        else:
            self.set_test_cookie()
            return self.form_invalid(form)


class LogoutView(RedirectView):
    """
    Authors: Martin Helmut 
    """
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class HitmenList(PermissionRequiredMixin, ListView):
    permission_required = ('user.view_user')
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        grupo = Group.objects.get(user=current_user).id
        context['grupo']= grupo

        #boss can see all the users in system
        if grupo == 1:
            hitmen =  User.objects.all()

        #manager can see his lackeys
        else:
            #Lackeys of the current user
            lackeys = list(Assignments.objects.filter(manager_id__in = [current_user.id]).values_list('lacayo_id', flat=True))
            hitmen =  User.objects.exclude(id=current_user.id).filter(id__in=lackeys)

        context['hitmen'] = hitmen
        return context

class HitmenDetailUpdate(PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    permission_required = ('user.change_user')
    model = User
    form_class = UserUpdateForm
    template_name_suffix = '_update_form'
    success_message = "%(username)s se actualizó exitosamente"

    def get_context_data(self, **kwargs):
        context = super(HitmenDetailUpdate, self).get_context_data(**kwargs)
        current_user = self.request.user
        grupo = Group.objects.get(user=current_user).id
        context['grupo'] = grupo
        return context

    def get_form_kwargs(self):
        """
        Send kwargs needded to make the queryset to know available hitmen
        """
        kwargs = super(HitmenDetailUpdate, self).get_form_kwargs()
        user = self.request.user
        user_group = Group.objects.get(user=user).id
        if hasattr(self, 'object'):
            kwargs.update({'user': user, 'user_group':user_group})
        return kwargs

    def form_valid(self, form):
        #Make the new assignment with the restrictions given
        return super(HitmenDetailUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse('user:hitmen_list')


class HitmanCreate(CreateView):
    """
    Authors: Martin Helmut
    Create new hitmam.
    """
    model = User
    form_class = RegistrationForm

    def get_context_data(self, **kwargs):
        context = super(HitmanCreate, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        #Se crea como Hitman automaticamente
        return super(HitmanCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('user:login')
