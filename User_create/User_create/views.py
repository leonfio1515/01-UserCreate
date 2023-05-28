from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, CreateView
from django.utils.text import capfirst
from django.urls import reverse
from django.forms.utils import ErrorList


from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

from DB.models import *
from .forms import *
########################################################################

class LoginView(LoginView):
    template_name = 'login.html'  

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Inicio de sesion"

        return context

class UserCreate(CreateView):
    model = Users
    form_class = UserCreateForm
    template_name = 'register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.first_name = capfirst(form.instance.first_name)
        form.instance.last_name = capfirst(form.instance.last_name)
        form.instance.is_active = False
        usuario = form.save(commit=False)
        usuario.save()
        self.enviar_correo_activacion(usuario, self.request)

        if form.errors:
            self.object = None
            errors = form.errors.get_json_data(escape_html=True)
            for field, field_errors in errors.item():
                form.add_error(field, ErrorList(field_errors))
            return self.render_ro_response(self.get_context_data(form=form))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('success_register')

    def enviar_correo_activacion(self, usuario, request):
        current_site = get_current_site(request)
        uid = urlsafe_base64_encode(force_bytes(usuario.id))
        activate_url = reverse('user_activate', kwargs={
                               'uidb64': uid, 'token': default_token_generator.make_token(usuario)})
        activation_link = f"http://{current_site.domain}{activate_url}"
        subject = 'Activación de cuenta'
        message = render_to_string('activate_account.html', {
            'usuario': usuario,
            'activation_link': activation_link,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(usuario.id)),
            'token': default_token_generator.make_token(usuario),
        })
        send_mail(subject, message, settings.EMAIL_HOST_USER, [usuario.email])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de usuario'

        return context

class UserActivate(TemplateView):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            usuario = Users.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Users.DoesNotExist):
            usuario = None

        if usuario is not None and default_token_generator.check_token(usuario, token):
            usuario.is_active = True
            usuario.save()
            return redirect('login')
        else:
            print(uid, usuario)
            return redirect('register')

class IndexView(TemplateView):
    template_name = "index.html"


class SuccessRegister(TemplateView):
    template_name = "success_register.html"
