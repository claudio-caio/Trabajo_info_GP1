from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Articulo, Categoria, ImagenArticulo
from .forms import ArticuloForm
from django.db.models import Sum
from apps.comentarios.models import Comentario
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from apps.comentarios.forms import ComentarioForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from django.utils import timezone
from django.utils.text import get_valid_filename
from django.conf import settings
import os

# Create your views here.
class ArticuloListView(ListView):
    model = Articulo
    template_name = 'posts/articulo_lista.html'
    context_object_name = 'articulos'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        queryset = queryset.select_related("categoria", "autor").prefetch_related("imagenes")
        queryset = queryset.order_by('-fecha_publicacion')
        
        categoria_id = self.request.GET.get('categoria')
        ordenar_por = self.request.GET.get('ordenar_por')
        
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
        
        if ordenar_por == 'mas_recientes':
            # Ordenar por fecha de publicación más reciente primero
            queryset = queryset.order_by('-fecha_publicacion')
        elif ordenar_por == 'mas_visitados':
            queryset = queryset.order_by('-visitas')
        elif ordenar_por == 'fecha_ascendente':
            queryset = queryset.order_by('fecha_publicacion')
        elif ordenar_por == 'fecha_descendente':
            queryset = queryset.order_by('-fecha_publicacion')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context

class ArticuloDetailView(DetailView):
    model = Articulo
    template_name = 'posts/articulo_detalle.html'
    context_object_name = 'articulo'
    
    def get_object(self):
        articulo = super().get_object()
        articulo.visitas += 1
        articulo.save(update_fields=['visitas'])
        return articulo
    
    def get_queryset(self):
        # Optimización de queries
        return super().get_queryset().select_related(
            "categoria", "autor"
        ).prefetch_related("imagenes")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario_actual'] = self.request.user
        context['comentarios'] = Comentario.objects.filter(
            articulo=self.object
        ).select_related("autor")
        context['form'] = ComentarioForm()
        return context
    
    def post(self, request, *args, **kwargs):
        articulo = self.get_object()
        contenido = request.POST.get('contenido')
        if contenido and request.user.is_authenticated:
            Comentario.objects.create(
                contenido=contenido, 
                articulo=articulo, 
                autor=request.user
            )
        return self.get(request, *args, **kwargs)
    
class ArticuloCreateView(LoginRequiredMixin, CreateView):
    model = Articulo
    form_class = ArticuloForm
    template_name = 'posts/articulo_crear.html'
    success_url = reverse_lazy('posts:articulo_lista')
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        
        # Validar archivos recibidos (tipo y tamaño)
        archivos = self.request.FILES.getlist('imagenes')
        errores = []
        tipos_permitidos = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        tamaño_maximo = 5 * 1024 * 1024 # 5 MB
        for archivo in archivos:
            if archivo.content_type not in tipos_permitidos:
                errores.append(f"El archivo {archivo.name} no es un tipo de imagen permitido.")
            if archivo.size > tamaño_maximo:
                errores.append(f"El archivo {archivo.name} excede el tamaño máximo permitido de 5 MB.")
        
        if errores:
            # Anexar errores genéricos al formulario y re-renderizar
            form.add_error('titulo', 'Error(es) en las imágenes: ' + ': '.join(errores))
            return self.form_invalid(form)
        
        # Si todo está bien, guardar el objeto y luego las imágenes
        response = super().form_valid(form)
        for archivo in archivos:
            ImagenArticulo.objects.create(articulo=self.object, imagen=archivo)
        return response
    
    def form_invalid(self, form):
        # Si el formulario es inválido, renderizar la plantilla con errores
        return super().form_invalid(form)

class ArticuloUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Articulo
    form_class = ArticuloForm
    template_name = 'posts/articulo_editar.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        for archivo in self.request.FILES.getlist('imagenes'):
            ImagenArticulo.objects.create(articulo=self.object, imagen=archivo)
        return response
    
    def test_func(self):
        return self.get_object().puede_editar(self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('posts:articulo_detalle', kwargs={'pk': self.object.pk})

@login_required
def eliminar_imagen_articulo(request, pk):
    """
    Elimina una imagen de un artículo mediante AJAX.
    """
    try:
        imagen = ImagenArticulo.objects.get(pk=pk)
        if imagen.articulo.puede_editar(request.user):
            imagen.delete()
            return JsonResponse({'exito': True})
        else:
            return JsonResponse({'exito': False, 'error': 'No tienes permiso para eliminar esta imagen.'})
    except ImagenArticulo.DoesNotExist:
        return JsonResponse({'exito': False, 'error': 'La imagen no existe.'})

class ArticuloDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Articulo
    template_name = 'posts/articulo_eliminar.html'
    success_url = reverse_lazy('posts:articulo_lista')
    
    def test_func(self):
        return self.get_object().puede_editar(self.request.user)

class PaginaPrincipalView(TemplateView):
    template_name = 'posts/pagina_principal.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_vistas = Articulo.objects.aggregate(total_vistas=Sum('visitas'))['total_vistas'] or 0
        context['total_vistas'] = total_vistas
        return context

@login_required
@require_POST
def ckeditor5_subir_imagen(request):
    """Endpoint simple para recibir subidas desde CKEditor5 SimpleUploadAdapter.

    Espera un campo 'upload' en multipart/form-data y devuelve JSON {"url": "..."}.
    Requiere usuario autenticado para evitar subidas anónimas.
    """
    upload = request.FILES.get('upload')
    if not upload:
        return JsonResponse({'error': 'No se ha proporcionado ningún archivo.'}, status=400)
    
    # construir ruta dentro de MEDIA_ROOT: uploads/YYYY/MM/DD/filename
    today = timezone.now()
    folder = os.path.join('uploads', str(today.year), f"{today.month:02}", f"{today.day:02}")
    filename = get_valid_filename(upload.name)
    save_path = os.path.join(folder, filename)
    
    # Asegurar no sobrescribir: default_storage.save hará unique name si existe
    saved_path = default_storage.save(save_path, upload)
    url = settings.MEDIA_URL.rstrip('/') + '/' + saved_path.replace('\\', '/')
    return JsonResponse({'url': url}, status=201)