from django import forms
from .models import Comentario

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'class': (
                    'w-full p-4 rounded-xl border-2 border-orange-300 '
                    'focus:border-orange-500 focus:ring-2 focus:ring-orange-200 '
                    'text-gray-800 placeholder-gray-400 resize-none '
                    'transition-all duration-200'
                ),
                'rows': 6,
                'placeholder': 'Escribe tu comentario aquí...',
            }),
        }
