from django.contrib import admin
from .models import Comentario

# Register your models here.
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('autor', 'articulo', 'contenido', 'fecha')
    list_filter = ('fecha', 'articulo')
    search_fields = ('autor__username', 'contenido')

admin.site.register(Comentario, ComentarioAdmin)