from django import forms

from .models import Categoria, Conta, MetaFinanceira, OrcamentoMensal, Transacao


class ContaForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = ["nome", "tipo", "saldo_inicial", "ativa"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_nome(self):
        nome = self.cleaned_data["nome"].strip()
        queryset = Conta.objects.filter(nome__iexact=nome)
        if self.user:
            queryset = queryset.filter(usuario=self.user)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise forms.ValidationError("Voce ja possui uma conta com esse nome.")
        return nome


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nome"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_nome(self):
        nome = self.cleaned_data["nome"].strip()
        queryset = Categoria.objects.filter(nome__iexact=nome)
        if self.user:
            queryset = queryset.filter(usuario=self.user)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise forms.ValidationError("Voce ja possui uma categoria com esse nome.")
        return nome


class OrcamentoMensalForm(forms.ModelForm):
    class Meta:
        model = OrcamentoMensal
        fields = ["categoria", "ano", "mes", "limite", "observacao"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields["categoria"].queryset = Categoria.objects.filter(usuario=self.user)

    def clean(self):
        cleaned_data = super().clean()
        categoria = cleaned_data.get("categoria")
        ano = cleaned_data.get("ano")
        mes = cleaned_data.get("mes")

        if mes and (mes < 1 or mes > 12):
            self.add_error("mes", "Informe um mes entre 1 e 12.")

        if categoria and ano and mes:
            queryset = OrcamentoMensal.objects.filter(
                usuario=self.user,
                categoria=categoria,
                ano=ano,
                mes=mes,
            )
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise forms.ValidationError("Ja existe um orcamento para essa categoria nesse periodo.")
        return cleaned_data


class MetaFinanceiraForm(forms.ModelForm):
    class Meta:
        model = MetaFinanceira
        fields = ["nome", "valor_alvo", "valor_atual", "prazo", "status"]
        widgets = {
            "prazo": forms.DateInput(attrs={"type": "date"}),
        }


class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ["conta", "descricao", "valor", "data", "tipo", "categoria", "observacao", "recorrente"]
        widgets = {
            "data": forms.DateInput(attrs={"type": "date"}),
            "observacao": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["conta"].required = True
        self.fields["conta"].empty_label = "Selecione uma conta"
        if user:
            self.fields["conta"].queryset = Conta.objects.filter(usuario=user, ativa=True)
            self.fields["categoria"].queryset = Categoria.objects.filter(usuario=user)
