from django.urls import path
from . import views

urlpatterns = [
    # 🚗 Dashboard
    path('', views.dashboard, name='dashboard'),

    # 👤 Cadastro
    path('cadastro/', views.cadastro, name='cadastro'),

    # 🚘 Veículos
    path('veiculos/', views.veiculos, name='veiculos'),
    path('veiculo/novo/', views.adicionar_veiculo, name='adicionar_veiculo'),
    path('veiculo/<int:id>/editar/', views.editar_veiculo, name='editar_veiculo'),
    path('veiculo/<int:id>/deletar/', views.deletar_veiculo, name='deletar_veiculo'),

    # 🔧 Manutenções
    path('adicionar/', views.adicionar_manutencao, name='adicionar_manutencao'),
    path('historico/', views.historico, name='historico'),
    path('manutencao/editar/<int:id>/', views.editar_manutencao, name='editar_manutencao'),
    path('manutencao/deletar/<int:id>/', views.deletar_manutencao, name='deletar_manutencao'),

    # 🚨 Alertas
    path('alertas/', views.alertas, name='alertas'),

    # 🚨 Minha Conta
    path('minha-conta/', views.minha_conta, name='minha_conta'),

]