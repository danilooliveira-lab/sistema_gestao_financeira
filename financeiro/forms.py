from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Categoria, Conta, MetaFinanceira, OrcamentoMensal, Transacao


class RegistroUsuarioForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        label="Nome",
        widget=forms.TextInput(attrs={"placeholder": "Seu nome"}),
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        label="Sobrenome",
        widget=forms.TextInput(attrs={"placeholder": "Seu sobrenome"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "voce@exemplo.com"}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")
        labels = {
            "username": "Nome de usuario",
        }
        help_texts = {
            "username": "Esse sera o identificador de acesso dentro do sistema.",
        }
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Escolha um nome de usuario"}),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ja existe uma conta com esse email.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"].strip()
        user.last_name = self.cleaned_data["last_name"].strip()
        user.email = self.cleaned_data["email"].strip().lower()
        if commit:
            user.save()
        return user


class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username"]
        labels = {
            "first_name": "Nome",
            "last_name": "Sobrenome",
            "email": "Email",
            "username": "Nome de usuario",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Seu nome"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Seu sobrenome"}),
            "email": forms.EmailInput(attrs={"placeholder": "voce@exemplo.com"}),
            "username": forms.TextInput(attrs={"placeholder": "Seu nome de usuario"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get("instance")
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        queryset = User.objects.filter(email__iexact=email)
        if self.user:
            queryset = queryset.exclude(pk=self.user.pk)
        if queryset.exists():
            raise forms.ValidationError("Ja existe uma conta com esse email.")
        return email

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        queryset = User.objects.filter(username__iexact=username)
        if self.user:
            queryset = queryset.exclude(pk=self.user.pk)
        if queryset.exists():
            raise forms.ValidationError("Ja existe uma conta com esse nome de usuario.")
        return username


class LoginUsuarioForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={"placeholder": "Seu nome de usuario", "autofocus": True}),
    )
    password = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Sua senha"}),
    )


class ContaForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = ["nome", "tipo", "saldo_inicial", "ativa"]
        labels = {
            "nome": "Nome da conta",
            "tipo": "Tipo",
            "saldo_inicial": "Saldo inicial",
            "ativa": "Conta ativa",
        }
        help_texts = {
            "nome": "Exemplos: Nubank, Carteira, Caixa da empresa, Reserva.",
            "saldo_inicial": "Use o saldo de partida para o sistema começar mais perto da sua realidade.",
            "ativa": "Desative apenas contas que voce nao quer mais usar em novos lancamentos.",
        }
        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Ex.: Nubank ou Carteira"}),
            "saldo_inicial": forms.NumberInput(attrs={"placeholder": "0,00", "step": "0.01"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["tipo"].choices = [
            ("corrente", "Conta do dia a dia"),
            ("poupanca", "Reserva / poupanca"),
            ("carteira", "Dinheiro em especie"),
            ("investimento", "Conta de investimento"),
        ]
        self.fields["tipo"].help_text = "Escolha o tipo que mais se aproxima do uso real dessa conta."

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
        labels = {"nome": "Nome da categoria"}
        help_texts = {
            "nome": "Use categorias reutilizaveis, como Moradia e contas, Alimentacao ou Transporte.",
        }
        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Ex.: Moradia e contas"}),
        }

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
        labels = {
            "categoria": "Categoria",
            "ano": "Ano",
            "mes": "Mes",
            "limite": "Limite mensal",
            "observacao": "Observacao",
        }
        widgets = {
            "ano": forms.NumberInput(attrs={"placeholder": "2026"}),
            "mes": forms.NumberInput(attrs={"placeholder": "3"}),
            "limite": forms.NumberInput(attrs={"placeholder": "0,00", "step": "0.01"}),
            "observacao": forms.TextInput(attrs={"placeholder": "Opcional"}),
        }

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
        labels = {
            "nome": "Nome da meta",
            "valor_alvo": "Valor alvo",
            "valor_atual": "Valor atual",
            "prazo": "Prazo",
            "status": "Status",
        }
        widgets = {
            "prazo": forms.DateInput(attrs={"type": "date"}),
            "nome": forms.TextInput(attrs={"placeholder": "Ex.: Reserva de emergencia"}),
            "valor_alvo": forms.NumberInput(attrs={"placeholder": "10000,00", "step": "0.01"}),
            "valor_atual": forms.NumberInput(attrs={"placeholder": "0,00", "step": "0.01"}),
        }


class TransacaoForm(forms.ModelForm):
    nova_categoria = forms.CharField(
        required=False,
        label="Criar categoria agora",
        help_text="Se a categoria ainda nao existir, digite aqui e o sistema cria para voce no mesmo envio.",
        widget=forms.TextInput(attrs={"placeholder": "Ex.: Moradia e contas"}),
    )

    class Meta:
        model = Transacao
        fields = ["conta", "descricao", "valor", "data", "tipo", "categoria", "observacao", "recorrente"]
        labels = {
            "conta": "Conta",
            "descricao": "Descricao",
            "valor": "Valor",
            "data": "Data",
            "tipo": "Tipo",
            "categoria": "Categoria",
            "observacao": "Observacao",
            "recorrente": "Lancamento recorrente",
        }
        widgets = {
            "data": forms.DateInput(attrs={"type": "date"}),
            "descricao": forms.TextInput(attrs={"placeholder": "Ex.: Conta de luz março"}),
            "valor": forms.NumberInput(attrs={"placeholder": "0,00", "step": "0.01"}),
            "observacao": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Detalhes opcionais. Ex.: vencimento, fornecedor, referencia da fatura.",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        initial_data = kwargs.pop("initial_data", None) or {}
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["conta"].required = True
        self.fields["categoria"].required = False
        self.fields["conta"].empty_label = "Selecione a conta usada"
        self.fields["categoria"].empty_label = "Selecionar categoria existente"
        self.fields["tipo"].help_text = "Escolha despesa para saidas e receita para entradas."
        self.fields["descricao"].help_text = "Use o nome real do gasto ou recebimento para facilitar a busca."
        self.fields["valor"].help_text = "Informe apenas o valor. O tipo define se entra como receita ou despesa."
        self.fields["conta"].help_text = "O sistema lembra a ultima conta usada para acelerar os proximos lancamentos."
        self.fields["categoria"].help_text = "Se preferir, use o campo abaixo para criar uma categoria sem sair da tela."
        if user:
            self.fields["conta"].queryset = Conta.objects.filter(usuario=user, ativa=True)
            self.fields["categoria"].queryset = Categoria.objects.filter(usuario=user)
        self.fields["recorrente"].widget.attrs.update({"class": "switch-input"})
        for field_name, value in initial_data.items():
            if field_name in self.fields and not self.is_bound and value not in (None, ""):
                self.fields[field_name].initial = value

    def clean_nova_categoria(self):
        return self.cleaned_data.get("nova_categoria", "").strip()

    def clean(self):
        cleaned_data = super().clean()
        categoria = cleaned_data.get("categoria")
        nova_categoria = cleaned_data.get("nova_categoria")

        if categoria and nova_categoria:
            self.add_error("nova_categoria", "Escolha uma categoria existente ou crie uma nova, nao os dois ao mesmo tempo.")
        return cleaned_data
