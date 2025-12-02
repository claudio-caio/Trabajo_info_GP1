from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Categoria(models.Model):
    """Categorías para organizar los artículos del blog"""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class Articulo(models.Model):
    """Modelo para los artículos del blog"""
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articulos')
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    visitas = models.PositiveIntegerField(default=0)
    destacado = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-fecha_publicacion']
    
    def  __str__(self):
        return self.titulo
    
    def puede_editar(self, user):
        """Verifica si un usuario puede editar el artículo"""
        return (
            user.is_authenticated and (
                user == self.autor or 
                user.is_staff or 
                user.is_superuser
            )
        )
    
class ImagenArticulo(models.Model):
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='articulos/imagenes/')
    
    class Meta:
        verbose_name = "Imagen de Artículo"
        verbose_name_plural = "Imágenes de Artículo"
        
    def  __str__(self):
        return f"Imagen para {self.articulo.titulo}"