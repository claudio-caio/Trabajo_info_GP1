from django.urls import path
from .views import (
    RegistroUsuarioView,
    LoginUsuarioView,
    PerfilDetalleView,
    PerfilUsuarioView,
    EliminarCuentaView,
    LogoutUsuarioView,
)

app_name = 'usuarios'

urlpatterns = [
    # Registro
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),

    # Login
    path('login/', LoginUsuarioView.as_view(), name='login'),

    # Logout
    path('logout/', LogoutUsuarioView.as_view(), name='logout'),

    # Perfil (detalle y edición)
    path('perfil/', PerfilDetalleView.as_view(), name='profile'),  # <--- nombre corregido
    path('perfil/editar/', PerfilUsuarioView.as_view(), name='editar_perfil'),

    # Eliminación de cuenta
    path('eliminar/', EliminarCuentaView.as_view(), name='eliminar_cuenta'),
]
