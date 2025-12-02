from django.urls import path
from .views import (
    RegistroUsuarioView,
    LoginUsuarioView,
    LogoutUsuarioView,
    PerfilUsuarioView,
    PerfilDetalleView,
    EliminarCuentaView,
)

app_name = 'usuarios'

urlpatterns = [
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('login/', LoginUsuarioView.as_view(), name='login'),
    path('logout/', LogoutUsuarioView.as_view(), name='logout'),
    path('perfil/', PerfilUsuarioView.as_view(), name='perfil'),
    path('perfil/editar/', PerfilDetalleView.as_view(), name='perfil_detalle'),
    path('perfil/eliminar/', EliminarCuentaView.as_view(), name='eliminar_cuenta'),
]
