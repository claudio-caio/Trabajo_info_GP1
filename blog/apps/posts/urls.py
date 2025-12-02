from django.urls import path, include
from .views import ArticuloListView, ArticuloDetailView, ArticuloCreateView, ArticuloUpdateView, ArticuloDeleteView, PaginaPrincipalView
from . import views

app_name = 'posts'

urlpatterns = [
    path('', PaginaPrincipalView.as_view(), name='pagina_principal'),
    path('articulos/', ArticuloListView.as_view(), name='articulo_list'),
    path('articulos/<int:pk>/', ArticuloDetailView.as_view(), name='articulo_detail'),
    path('crear/', ArticuloCreateView.as_view(), name='articulo_create'),
    path('editar/<int:pk>/', ArticuloUpdateView.as_view(), name='articulo_update'),
    path('eliminar/<int:pk>/', ArticuloDeleteView.as_view(), name='articulo_delete'),
    path('imagen/<int:pk>/eliminar/', views.eliminar_imagen_articulo, name='eliminar_imagen_articulo'),
    path('comentarios/', include('blog.apps.comments.urls'), name='comments')
]