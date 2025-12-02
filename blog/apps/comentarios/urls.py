from django.urls import path
from .views import ComentarioCreateView, ComentarioUpdateView, ComentarioDeleteView

app_name = 'comentarios'

urlpatterns = [
    path('comentarios/agregar/<int:articulo_pk>/', ComentarioCreateView.as_view(), name='comentario_create'),
    path('comentarios/editar/<int:pk>/', ComentarioUpdateView.as_view(), name='comentario_update'),
    path('comentarios/eliminar/<int:pk>/', ComentarioDeleteView.as_view(), name='comentario_delete'),
]
