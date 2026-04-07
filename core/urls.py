from django.urls import path
from . import views
from .views import dashboard
from .views import alertas

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
    path('alertas/', alertas, name='alertas'),
    path('manutencao/editar/<int:id>/', views.editar_manutencao, name='editar_manutencao'),
    path('manutencao/deletar/<int:id>/', views.deletar_manutencao, name='deletar_manutencao'),
]