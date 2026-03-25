from django.contrib.auth.models import User
from django.db import models


class Conta(models.Model):
    TIPO_CHOICES = (
        ("corrente", "Conta corrente"),
        ("poupanca", "Poupanca"),
        ("carteira", "Carteira"),
        ("investimento", "Investimento"),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default="corrente")
    saldo_inicial = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ativa = models.BooleanField(default=True)
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["nome", "usuario"],
                name="unique_conta_por_usuario",
            )
        ]
        ordering = ["nome"]


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["nome", "usuario"],
                name="unique_categoria_por_usuario",
            )
        ]
        ordering = ["nome"]


class OrcamentoMensal(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    ano = models.PositiveIntegerField()
    mes = models.PositiveSmallIntegerField()
    limite = models.DecimalField(max_digits=10, decimal_places=2)
    observacao = models.CharField(max_length=255, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.categoria.nome} - {self.mes:02d}/{self.ano}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "categoria", "ano", "mes"],
                name="unique_orcamento_categoria_periodo",
            )
        ]
        ordering = ["-ano", "-mes", "categoria__nome"]


class MetaFinanceira(models.Model):
    STATUS_CHOICES = (
        ("ativa", "Ativa"),
        ("concluida", "Concluida"),
        ("pausada", "Pausada"),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=120)
    valor_alvo = models.DecimalField(max_digits=12, decimal_places=2)
    valor_atual = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    prazo = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="ativa")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ["status", "prazo", "nome"]


class Transacao(models.Model):
    TIPO_CHOICES = (
        ("receita", "Receita"),
        ("despesa", "Despesa"),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    conta = models.ForeignKey(Conta, on_delete=models.SET_NULL, null=True, blank=True)
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    tipo = models.CharField(max_length=7, choices=TIPO_CHOICES)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    observacao = models.TextField(blank=True)
    recorrente = models.BooleanField(default=False)
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.descricao} (R$ {self.valor})"

    class Meta:
        ordering = ["-data", "-id"]
