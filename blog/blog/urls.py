"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from blog.views import IndexView
from apps.posts.views import ckeditor5_subir_imagen

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', IndexView.as_view(), name='index'),

    # Usuarios
    path('usuarios/', include(('apps.usuarios.urls', 'usuarios'), namespace='usuarios')),
    
    # Nosotros
    path('nosotros/', TemplateView.as_view(template_name='nosotros.html'), name='nosotros'),
    
    # Contacto
    path('contacto/', TemplateView.as_view(template_name='contacto.html'), name='contacto'),

    # POSTS -> NECESARIO PARA QUE FUNCIONE "posts:articulo_lista"
    path('posts/', include(('apps.posts.urls', 'posts'), namespace='posts')),

    path("comentarios/", include("apps.comentarios.urls", namespace="comentarios")),
    
    # CKEditor 5 upload - URL global requerida por CKEditor 5
    path('ckeditor/upload/', ckeditor5_subir_imagen, name='ck_editor_5_upload_file'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
