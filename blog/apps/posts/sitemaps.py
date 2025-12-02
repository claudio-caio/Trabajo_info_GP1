from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Articulo

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'
    
    def items(self):
        return ['posts:pagina_principal', 'posts:articulo_list', 'posts:articulo_create']
    
    def location(self, item):
        return reverse(item)

class ArticuloSitemap(Sitemap):
    priority = 0.9
    changefreq = 'weekly'
    
    def items(self):
        return Articulo.objects.all().order_by('-fecha_publicacion')
    
    def lastmod(self, obj):
        return obj.fecha_publicacion
    
    def location(self, obj):
        return reverse('posts:articulo_detail', args=[obj.pk])