from django.urls import path, include
from .views import (
    PaginaPrincipalView,
    ArticuloListView,
    ArticuloDetailView,
    ArticuloCreateView,
    ArticuloUpdateView,
    ArticuloDeleteView,
    eliminar_imagen_articulo,
    ckeditor5_subir_imagen,
)

app_name = 'posts'

urlpatterns = [
    # Página principal
    path('', PaginaPrincipalView.as_view(), name='pagina_principal'),

    # Artículos
    path('articulos/', ArticuloListView.as_view(), name='articulo_lista'),
    path('articulos/<int:pk>/', ArticuloDetailView.as_view(), name='articulo_detalle'),
    path('articulos/crear/', ArticuloCreateView.as_view(), name='articulo_crear'),
    path('articulos/<int:pk>/editar/', ArticuloUpdateView.as_view(), name='articulo_editar'),
    path('articulos/<int:pk>/eliminar/', ArticuloDeleteView.as_view(), name='articulo_eliminar'),

    # Eliminar imágenes por AJAX
    path('imagenes/<int:pk>/eliminar/', eliminar_imagen_articulo, name='eliminar_imagen_articulo'),

    # Subida de imágenes CKEditor5
    path('ckeditor/upload/', ckeditor5_subir_imagen, name='ckeditor5_subir_imagen'),

    # Comentarios (delegados al app comentarios)
    path('comentarios/', include('apps.comentarios.urls')),
]
