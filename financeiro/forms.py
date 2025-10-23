from django import forms
from .models import Categoria, Transacao

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']


class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['descricao', 'valor', 'data', 'tipo', 'categoria']

        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }

    # Filtra o campo 'categoria' para mostrar apenas as do usuário logado
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) 

        super(TransacaoForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['categoria'].queryset = Categoria.objects.filter(usuario=user)