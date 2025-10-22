# financeiro/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Sum # <-- IMPORT FINAL PARA O DASHBOARD

from .models import Categoria, Transacao 
from .forms import CategoriaForm, TransacaoForm 

# Módulo 1: Registro
class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('dashboard') 

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response

# --- NOVA VIEW (MÓDULO 2) ---
@login_required
def dashboard(request):
    transacoes = Transacao.objects.filter(usuario=request.user)

    total_receitas = transacoes.filter(tipo='receita').aggregate(total=Sum('valor'))['total'] or 0
    total_despesas = transacoes.filter(tipo='despesa').aggregate(total=Sum('valor'))['total'] or 0

    saldo = total_receitas - total_despesas

    recentes = transacoes.order_by('-data')[:5] 

    context = {
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo': saldo,
        'transacoes_recentes': recentes,
    }

    return render(request, 'financeiro/dashboard.html', context)


# Módulo 4: Gerenciar Categorias
@login_required
def gerenciar_categorias(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.usuario = request.user
            try:
                categoria.save()
            except:
                pass 
            return redirect('gerenciar_categorias')
    else:
        form = CategoriaForm()
    categorias = Categoria.objects.filter(usuario=request.user)
    context = { 'form': form, 'categorias': categorias }
    return render(request, 'financeiro/categorias.html', context)

# Módulo 4: Deletar Categoria
@login_required
def deletar_categoria(request, id):
    try:
        categoria = Categoria.objects.get(id=id, usuario=request.user)
        categoria.delete()
    except Categoria.DoesNotExist:
        pass
    return redirect('gerenciar_categorias')

# Módulo 3: Listar Transações
@login_required
def listar_transacoes(request):
    transacoes = Transacao.objects.filter(usuario=request.user).order_by('-data')
    return render(request, 'financeiro/lista_transacoes.html', {'transacoes': transacoes})

# Módulo 3: Adicionar Transação
@login_required
def adicionar_transacao(request):
    if request.method == 'POST':
        form = TransacaoForm(request.POST, user=request.user) 
        if form.is_valid():
            transacao = form.save(commit=False)
            transacao.usuario = request.user 
            transacao.save()
            return redirect('lista_transacoes')
    else:
        form = TransacaoForm(user=request.user) 

    return render(request, 'financeiro/form_transacao.html', {'form': form})

# Módulo 3: Deletar Transação
@login_required
def deletar_transacao(request, id):
    try:
        transacao = Transacao.objects.get(id=id, usuario=request.user)
        transacao.delete()
    except Transacao.DoesNotExist:
        pass
    return redirect('lista_transacoes')