from django.core.paginator import Paginator
from django.db.models import Case, DecimalField, ExpressionWrapper, F, Q, Sum, Value, When
from django.db.models.functions import Coalesce, TruncMonth
from django.utils import timezone

from .models import Categoria, Conta, MetaFinanceira, OrcamentoMensal, Transacao


def contas_do_usuario(usuario, apenas_ativas=False):
    queryset = Conta.objects.filter(usuario=usuario)
    if apenas_ativas:
        queryset = queryset.filter(ativa=True)
    return queryset


def categorias_do_usuario(usuario):
    return Categoria.objects.filter(usuario=usuario)


def orcamentos_do_usuario(usuario):
    return OrcamentoMensal.objects.filter(usuario=usuario).select_related("categoria")


def metas_do_usuario(usuario, apenas_ativas=False):
    queryset = MetaFinanceira.objects.filter(usuario=usuario)
    if apenas_ativas:
        queryset = queryset.filter(status="ativa")
    return queryset


def transacoes_do_usuario(usuario):
    return Transacao.objects.filter(usuario=usuario).select_related("categoria", "conta")


def filtrar_transacoes(usuario, filtros):
    queryset = transacoes_do_usuario(usuario)

    conta_id = filtros.get("conta")
    tipo = filtros.get("tipo")
    busca = (filtros.get("q") or "").strip()
    recorrente = filtros.get("recorrente")

    if conta_id:
        queryset = queryset.filter(conta_id=conta_id)
    if tipo in {"receita", "despesa"}:
        queryset = queryset.filter(tipo=tipo)
    if recorrente in {"true", "false"}:
        queryset = queryset.filter(recorrente=(recorrente == "true"))
    if busca:
        queryset = queryset.filter(Q(descricao__icontains=busca) | Q(observacao__icontains=busca))

    return queryset, {
        "conta": conta_id or "",
        "tipo": tipo or "",
        "q": busca,
        "recorrente": recorrente or "",
    }


def paginar_queryset(queryset, page_number, per_page=10):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(page_number)


def _sum_or_zero(queryset, **filters):
    return queryset.filter(**filters).aggregate(total=Sum("valor"))["total"] or 0


def _historico_mensal(usuario, limite=6):
    queryset = (
        transacoes_do_usuario(usuario)
        .annotate(mes=TruncMonth("data"))
        .values("mes")
        .annotate(
            receitas=Coalesce(Sum("valor", filter=Q(tipo="receita")), Value(0), output_field=DecimalField(max_digits=12, decimal_places=2)),
            despesas=Coalesce(Sum("valor", filter=Q(tipo="despesa")), Value(0), output_field=DecimalField(max_digits=12, decimal_places=2)),
        )
        .order_by("-mes")[:limite]
    )
    historico = []
    for item in queryset:
        item["saldo"] = item["receitas"] - item["despesas"]
        historico.append(item)
    return historico


def _resumo_orcamentos(usuario, ano, mes):
    orcamentos = orcamentos_do_usuario(usuario).filter(ano=ano, mes=mes)
    resumo = []
    for orcamento in orcamentos:
        gasto = _sum_or_zero(
            transacoes_do_usuario(usuario),
            tipo="despesa",
            categoria=orcamento.categoria,
            data__year=ano,
            data__month=mes,
        )
        restante = orcamento.limite - gasto
        percentual = 0
        if orcamento.limite:
            percentual = min((gasto / orcamento.limite) * 100, 999)
        resumo.append(
            {
                "orcamento": orcamento,
                "gasto": gasto,
                "restante": restante,
                "percentual": percentual,
                "excedido": gasto > orcamento.limite,
            }
        )
    return resumo


def _resumo_metas(usuario):
    metas = metas_do_usuario(usuario)
    resumo = []
    for meta in metas:
        percentual = 0
        if meta.valor_alvo:
            percentual = min((meta.valor_atual / meta.valor_alvo) * 100, 100)
        resumo.append(
            {
                "meta": meta,
                "percentual": percentual,
                "faltante": max(meta.valor_alvo - meta.valor_atual, 0),
            }
        )
    return resumo


def resumo_dashboard(usuario):
    hoje = timezone.localdate()
    transacoes = transacoes_do_usuario(usuario)
    contas = contas_do_usuario(usuario)
    categorias = categorias_do_usuario(usuario)

    total_receitas = _sum_or_zero(transacoes, tipo="receita")
    total_despesas = _sum_or_zero(transacoes, tipo="despesa")
    saldo = total_receitas - total_despesas
    saldo_inicial_total = contas.aggregate(total=Sum("saldo_inicial"))["total"] or 0
    patrimonio_total = saldo_inicial_total + saldo

    receitas_mes = _sum_or_zero(transacoes, tipo="receita", data__year=hoje.year, data__month=hoje.month)
    despesas_mes = _sum_or_zero(transacoes, tipo="despesa", data__year=hoje.year, data__month=hoje.month)
    saldo_mes = receitas_mes - despesas_mes

    contas_resumo = contas.annotate(
        movimentacao=Coalesce(
            Sum(
                Case(
                    When(transacao__tipo="receita", then=F("transacao__valor")),
                    When(
                        transacao__tipo="despesa",
                        then=ExpressionWrapper(F("transacao__valor") * Value(-1), output_field=DecimalField(max_digits=12, decimal_places=2)),
                    ),
                    default=Value(0),
                    output_field=DecimalField(max_digits=12, decimal_places=2),
                )
            ),
            Value(0),
            output_field=DecimalField(max_digits=12, decimal_places=2),
        )
    )

    return {
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "saldo": saldo,
        "saldo_inicial_total": saldo_inicial_total,
        "patrimonio_total": patrimonio_total,
        "contas_total": contas.count(),
        "categorias_total": categorias.count(),
        "transacoes_total": transacoes.count(),
        "contas_ativas": contas.filter(ativa=True).count(),
        "precisa_onboarding": not contas.exists() or not transacoes.exists(),
        "transacoes_recentes": transacoes.order_by("-data", "-id")[:5],
        "contas_resumo": contas_resumo,
        "receitas_mes": receitas_mes,
        "despesas_mes": despesas_mes,
        "saldo_mes": saldo_mes,
        "historico_mensal": _historico_mensal(usuario),
        "orcamentos_resumo": _resumo_orcamentos(usuario, hoje.year, hoje.month),
        "metas_resumo": _resumo_metas(usuario),
        "mes_atual": hoje.month,
        "ano_atual": hoje.year,
    }
