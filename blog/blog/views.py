from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "index.html"



""" def home(request):
    return HttpResponse("¡Bienvenido a mi blog de mascotas!") """