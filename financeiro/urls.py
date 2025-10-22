# financeiro/urls.py
from django.urls import path
from . import views 

urlpatterns = [
    # Módulo 2: Dashboard (Raiz do site)
    path('', views.dashboard, name='dashboard'), 

    # Módulo 1: Registro
    path('registrar/', views.RegisterView.as_view(), name='register'),

    # Módulo 4: Categorias
    path('categorias/', views.gerenciar_categorias, name='gerenciar_categorias'),
    path('categorias/deletar/<int:id>/', views.deletar_categoria, name='deletar_categoria'),

    # Módulo 3: Transações
    path('transacoes/', views.listar_transacoes, name='lista_transacoes'),
    path('transacoes/adicionar/', views.adicionar_transacao, name='adicionar_transacao'),
    path('transacoes/deletar/<int:id>/', views.deletar_transacao, name='deletar_transacao'),
]