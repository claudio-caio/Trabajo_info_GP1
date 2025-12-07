from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegistroUsuarioForm, PerfilUsuarioForm
from .models import Usuario

# Registro de usuario
class RegistroUsuarioView(View):
    form_class = RegistroUsuarioForm
    template_name = 'usuarios/registro.html'
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, f"¡Registro exitoso! Bienvenido, {usuario.username}.")
            return redirect('posts:articulo_lista')
        return render(request, self.template_name, {'form': form})

# Login de usuario
class LoginUsuarioView(View):
    template_name = 'usuarios/login.html'
    
    def personalizar_formulario(self, form):
        form.fields['username'].label = "Nombre de usuario"
        form.fields['username'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Ingrese su nombre de usuario'
        })
        form.fields['password'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Ingrese su contraseña'
        })
    
    def get(self, request):
        form = AuthenticationForm()
        self.personalizar_formulario(form)
        next_url = request.GET.get('next', '')
        return render(request, self.template_name, {'form': form, 'next': next_url})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        self.personalizar_formulario(form)
        
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            messages.success(request, f"¡Bienvenido de nuevo, {usuario.username}!")
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect('index')
        messages.error(request, "Nombre de usuario o contraseña incorrectos.")
        return render(request, self.template_name, {'form': form})

# Perfil detalle
class PerfilDetalleView(LoginRequiredMixin, TemplateView):
    template_name = 'usuarios/perfil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context

# Edición de perfil
class PerfilUsuarioView(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = PerfilUsuarioForm
    template_name = 'usuarios/editar_perfil.html'
    success_url = reverse_lazy('usuarios:profile')  # <--- corregido
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, "¡Perfil actualizado con éxito!")
        return super().form_valid(form)

# Eliminar cuenta de usuario
class EliminarCuentaView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usuarios/eliminar_cuenta.html')
    
    def post(self, request):
        usuario = request.user
        logout(request)
        usuario.delete()
        messages.success(request, "Tu cuenta ha sido eliminada exitosamente.")
        return redirect('index')


# Logout con confirmación
class LogoutUsuarioView(LoginRequiredMixin, TemplateView):
    template_name = 'usuarios/logout.html'

    def post(self, request):
        logout(request)
        messages.success(request, "Has cerrado sesión correctamente")
        return redirect('index')
