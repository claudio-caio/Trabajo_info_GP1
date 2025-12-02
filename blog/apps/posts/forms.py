from django import forms
from .models import Articulo
from django.core.exceptions import ValidationError
from django.forms import Textarea as CKEditorUploadingWidget

_widget_candidates = (
    'ckeditor_uploader.widgets.CKEditorUploadingWidget',
    'ckeditor.widgets.CKEditorWidget',
    'django_ckeditor_5.widgets.CKEditor5Widget',
    'django_ckeditor_5.widgets.CKEditorWidget',
)

for _path in _widget_candidates:
    try:
        module_path, cls_name = _path.rsplit('.', 1)
        module = __import__(module_path, fromlist=[cls_name])
        CKEditorUploadingWidget = getattr(module, cls_name)
        break
    except Exception:
        continue
from utils.sanitizers import clean_html

# Widget custom para permitir múltiples archivos
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['titulo', 'contenido', 'categoria']
        try:
            widget_name = CKEditorUploadingWidget.__name__
        except Exception:
            widget_name = ''
        
        if 'CKEditor5' in widget_name or 'CKEditor5Widget' in widget_name:
            widgets = {
                'contenido': CKEditorUploadingWidget(config_name='default'),
            }
        else:
            widgets = {
                'contenido': CKEditorUploadingWidget(),
            }
    
    def clean_contenido(self):
        raw = self.cleaned_data.get('contenido', '')
        cleaned = clean_html(raw)
        return cleaned