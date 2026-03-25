from django.contrib import admin

from .models import Categoria, Conta, MetaFinanceira, OrcamentoMensal, Transacao


@admin.register(Conta)
class ContaAdmin(admin.ModelAdmin):
    list_display = ("nome", "tipo", "saldo_inicial", "ativa", "usuario")
    list_filter = ("tipo", "ativa")
    search_fields = ("nome", "usuario__username")


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "usuario", "criada_em")
    search_fields = ("nome", "usuario__username")


@admin.register(OrcamentoMensal)
class OrcamentoMensalAdmin(admin.ModelAdmin):
    list_display = ("categoria", "mes", "ano", "limite", "usuario")
    list_filter = ("ano", "mes")
    search_fields = ("categoria__nome", "usuario__username")


@admin.register(MetaFinanceira)
class MetaFinanceiraAdmin(admin.ModelAdmin):
    list_display = ("nome", "valor_alvo", "valor_atual", "prazo", "status", "usuario")
    list_filter = ("status",)
    search_fields = ("nome", "usuario__username")


@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ("descricao", "tipo", "valor", "data", "conta", "categoria", "usuario", "recorrente")
    list_filter = ("tipo", "recorrente", "conta")
    search_fields = ("descricao", "observacao", "usuario__username")
