from django.urls import path
from . import views
from .views import dashboard

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('adicionar/', views.adicionar_manutencao, name='adicionar_manutencao'),
    path('historico/', views.historico, name='historico'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('veiculos/', views.veiculos, name='veiculos'),
    path('veiculo/novo/', views.adicionar_veiculo, name='adicionar_veiculo'),
    path('veiculo/<int:id>/editar/', views.editar_veiculo, name='editar_veiculo'),
    path('veiculo/<int:id>/deletar/', views.deletar_veiculo, name='deletar_veiculo'),
    path('', dashboard, name='dashboard'),
]