from django.urls import path
from . import views 

urlpatterns = [

    path('', views.dashboard, name='dashboard'), 


    path('registrar/', views.RegisterView.as_view(), name='register'),
    

    path('categorias/', views.gerenciar_categorias, name='gerenciar_categorias'),
    path('categorias/deletar/<int:id>/', views.deletar_categoria, name='deletar_categoria'),
    

    path('transacoes/', views.listar_transacoes, name='lista_transacoes'),
    path('transacoes/adicionar/', views.adicionar_transacao, name='adicionar_transacao'),
    

    path('transacoes/editar/<int:id>/', views.editar_transacao, name='editar_transacao'),
    path('transacoes/deletar/<int:id>/', views.deletar_transacao, name='deletar_transacao'),
    
]