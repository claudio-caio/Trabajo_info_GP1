from django.urls import path
from .views import (
    ComentarioCreateView,
    ComentarioUpdateView,
    ComentarioDeleteView,
)

app_name = 'comentarios'

urlpatterns = [
    # Crear comentario asociado a un artículo
    path('crear/<int:articulo_pk>/', ComentarioCreateView.as_view(), name='crear_comentario'),

    # Editar comentario
    path('editar/<int:pk>/', ComentarioUpdateView.as_view(), name='editar_comentario'),

    # Eliminar comentario
    path('eliminar/<int:pk>/', ComentarioDeleteView.as_view(), name='eliminar_comentario'),
]
