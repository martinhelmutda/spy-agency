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

from .models import User
from .forms import RegistrationForm
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


class HitmenList(ListView):
    pass

class HitmenDetailUpdate(UpdateView):
    pass

class HitmanCreate(CreateView):
    """
    Authors: Martin Helmut
    Create new hitma.
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
