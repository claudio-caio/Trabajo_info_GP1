from django.contrib import admin
from .models import Categoria, Articulo, ImagenArticulo


# Register your models here.
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre', )

# Inline para cargar varias imágenes dentro de un Articulo
class ImagenArticuloInline(admin.TabularInline):
    model = ImagenArticulo
    extra = 1

class ArticuloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'fecha_publicacion', 'visitas', 'destacado')
    list_filter = ('categoria', 'destacado')
    search_fields = ('titulo', 'contenido')
    inlines = [ImagenArticuloInline]


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Articulo, ArticuloAdmin)
admin.site.register(ImagenArticulo)