from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Comentario
from .forms import ComentarioForm
from apps.posts.models import Articulo
from .mixins import ComentarioPermisoMixin

# Create your views here.
class ComentarioCreateView(LoginRequiredMixin, CreateView):
    model = Comentario
    form_class = ComentarioForm
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        form.instance.articulo = get_object_or_404(Articulo, pk=self.kwargs['articulo_pk'])
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy(
            'posts:articulo_detalle',
            kwargs={'pk': self.kwargs['articulo_pk']}
        )
    
    def get(self, request, *args, **kwargs):
        return redirect('posts:articulo_detalle', pk=self.kwargs['articulo_pk'])

class ComentarioUpdateView(ComentarioPermisoMixin, UpdateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'comentarios/editar_comentario.html'

class ComentarioDeleteView(ComentarioPermisoMixin, DeleteView):
    model = Comentario
    template_name = 'comentarios/eliminar_comentario.html'