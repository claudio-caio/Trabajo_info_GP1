from django import forms
from .models import Articulo
from django.core.exceptions import ValidationError

from django import forms
from .models import Articulo

# Widget custom para permitir múltiples archivos
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True
    attrs = {'class': 'hidden'}  # ocultamos el input por defecto y lo manejamos con un botón

class ArticuloForm(forms.ModelForm):

    class Meta:
        model = Articulo
        fields = ['titulo', 'contenido', 'categoria']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': (
                    'w-full p-3 mb-4 rounded-xl border-2 border-orange-300 '
                    'focus:border-orange-500 focus:ring-2 focus:ring-orange-200 '
                    'text-gray-800 placeholder-gray-400 transition-all duration-200'
                ),
                'placeholder': 'Escribe el título del artículo...',
            }),
            'contenido': forms.Textarea(attrs={
                'class': (
                    'w-full p-4 rounded-xl border-2 border-orange-300 '
                    'focus:border-orange-500 focus:ring-2 focus:ring-orange-200 '
                    'text-gray-800 placeholder-gray-400 resize-none '
                    'transition-all duration-200'
                ),
                'rows': 10,
                'placeholder': 'Escribe el contenido del artículo aquí...',
            }),
            'categoria': forms.Select(attrs={
                'class': (
                    'w-full p-3 rounded-xl border-2 border-orange-300 '
                    'focus:border-orange-500 focus:ring-2 focus:ring-orange-200 '
                    'bg-white text-gray-800 transition-all duration-200'
                ),
            }),
        }
