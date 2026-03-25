from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST

from .forms import CategoriaForm, ContaForm, MetaFinanceiraForm, OrcamentoMensalForm, TransacaoForm
from .models import Categoria, Conta, MetaFinanceira, OrcamentoMensal, Transacao
from .selectors import (
    categorias_do_usuario,
    contas_do_usuario,
    filtrar_transacoes,
    metas_do_usuario,
    orcamentos_do_usuario,
    paginar_queryset,
    resumo_dashboard,
)
from .services import (
    criar_categoria_para_usuario,
    criar_conta_para_usuario,
    criar_meta_para_usuario,
    criar_orcamento_para_usuario,
    criar_transacao_para_usuario,
    remover_recurso_do_usuario,
    usuario_possui_conta_ativa,
)


class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        messages.success(self.request, "Conta criada com sucesso.")
        return redirect(self.get_success_url())


@login_required
def dashboard(request):
    return render(request, "financeiro/dashboard.html", resumo_dashboard(request.user))


@login_required
def gerenciar_contas(request):
    if request.method == "POST":
        form = ContaForm(request.POST, user=request.user)
        if form.is_valid():
            criar_conta_para_usuario(form, request.user)
            messages.success(request, "Conta criada com sucesso.")
            return redirect("gerenciar_contas")
        messages.error(request, "Nao foi possivel salvar a conta. Verifique os dados informados.")
    else:
        form = ContaForm(user=request.user)

    contas = contas_do_usuario(request.user)
    return render(request, "financeiro/contas.html", {"form": form, "contas": contas})


@login_required
@require_POST
def deletar_conta(request, id):
    get_object_or_404(Conta, id=id, usuario=request.user)
    remover_recurso_do_usuario(Conta, id, request.user)
    messages.success(request, "Conta removida com sucesso.")
    return redirect("gerenciar_contas")


@login_required
def gerenciar_categorias(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST, user=request.user)
        if form.is_valid():
            criar_categoria_para_usuario(form, request.user)
            messages.success(request, "Categoria criada com sucesso.")
            return redirect("gerenciar_categorias")
        messages.error(request, "Nao foi possivel salvar a categoria. Verifique os dados informados.")
    else:
        form = CategoriaForm(user=request.user)

    categorias = categorias_do_usuario(request.user)
    context = {"form": form, "categorias": categorias}
    return render(request, "financeiro/categorias.html", context)


@login_required
@require_POST
def deletar_categoria(request, id):
    get_object_or_404(Categoria, id=id, usuario=request.user)
    remover_recurso_do_usuario(Categoria, id, request.user)
    messages.success(request, "Categoria removida com sucesso.")
    return redirect("gerenciar_categorias")


@login_required
def gerenciar_orcamentos(request):
    if request.method == "POST":
        form = OrcamentoMensalForm(request.POST, user=request.user)
        if form.is_valid():
            criar_orcamento_para_usuario(form, request.user)
            messages.success(request, "Orcamento criado com sucesso.")
            return redirect("gerenciar_orcamentos")
        messages.error(request, "Nao foi possivel salvar o orcamento. Verifique os dados informados.")
    else:
        form = OrcamentoMensalForm(user=request.user)

    return render(
        request,
        "financeiro/orcamentos.html",
        {
            "form": form,
            "orcamentos": orcamentos_do_usuario(request.user),
        },
    )


@login_required
@require_POST
def deletar_orcamento(request, id):
    get_object_or_404(OrcamentoMensal, id=id, usuario=request.user)
    remover_recurso_do_usuario(OrcamentoMensal, id, request.user)
    messages.success(request, "Orcamento removido com sucesso.")
    return redirect("gerenciar_orcamentos")


@login_required
def gerenciar_metas(request):
    if request.method == "POST":
        form = MetaFinanceiraForm(request.POST)
        if form.is_valid():
            criar_meta_para_usuario(form, request.user)
            messages.success(request, "Meta criada com sucesso.")
            return redirect("gerenciar_metas")
        messages.error(request, "Nao foi possivel salvar a meta. Verifique os dados informados.")
    else:
        form = MetaFinanceiraForm()

    return render(
        request,
        "financeiro/metas.html",
        {
            "form": form,
            "metas": metas_do_usuario(request.user),
        },
    )


@login_required
@require_POST
def deletar_meta(request, id):
    get_object_or_404(MetaFinanceira, id=id, usuario=request.user)
    remover_recurso_do_usuario(MetaFinanceira, id, request.user)
    messages.success(request, "Meta removida com sucesso.")
    return redirect("gerenciar_metas")


@login_required
def listar_transacoes(request):
    queryset, filtros = filtrar_transacoes(request.user, request.GET)
    page_obj = paginar_queryset(queryset, request.GET.get("page"), per_page=8)

    context = {
        "transacoes": page_obj.object_list,
        "page_obj": page_obj,
        "contas": contas_do_usuario(request.user, apenas_ativas=True),
        "filtro_conta": filtros["conta"],
        "filtro_tipo": filtros["tipo"],
        "filtro_recorrente": filtros["recorrente"],
        "busca": filtros["q"],
    }
    return render(request, "financeiro/lista_transacoes.html", context)


@login_required
def adicionar_transacao(request):
    if not usuario_possui_conta_ativa(request.user):
        messages.error(request, "Cadastre ao menos uma conta ativa antes de lancar transacoes.")
        return redirect("gerenciar_contas")

    if request.method == "POST":
        form = TransacaoForm(request.POST, user=request.user)
        if form.is_valid():
            criar_transacao_para_usuario(form, request.user)
            messages.success(request, "Transacao adicionada com sucesso.")
            return redirect("lista_transacoes")
        messages.error(request, "Nao foi possivel salvar a transacao. Verifique os dados informados.")
    else:
        form = TransacaoForm(user=request.user)

    return render(
        request,
        "financeiro/form_transacao.html",
        {
            "form": form,
            "form_title": "Adicionar Nova Transacao",
            "submit_label": "Salvar Transacao",
        },
    )


@login_required
def editar_transacao(request, id):
    transacao = get_object_or_404(Transacao, id=id, usuario=request.user)

    if request.method == "POST":
        form = TransacaoForm(request.POST, user=request.user, instance=transacao)
        if form.is_valid():
            form.save()
            messages.success(request, "Transacao atualizada com sucesso.")
            return redirect("lista_transacoes")
        messages.error(request, "Nao foi possivel atualizar a transacao. Verifique os dados informados.")
    else:
        form = TransacaoForm(user=request.user, instance=transacao)

    context = {
        "form": form,
        "form_title": "Editar Transacao",
        "submit_label": "Salvar Alteracoes",
    }
    return render(request, "financeiro/form_transacao.html", context)


@login_required
@require_POST
def deletar_transacao(request, id):
    get_object_or_404(Transacao, id=id, usuario=request.user)
    remover_recurso_do_usuario(Transacao, id, request.user)
    messages.success(request, "Transacao removida com sucesso.")
    return redirect("lista_transacoes")
