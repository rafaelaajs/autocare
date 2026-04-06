from django import forms
from .models import Manutencao
from .models import Veiculo

class ManutencaoForm(forms.ModelForm):
    class Meta:
        model = Manutencao
        fields = ['veiculo', 'tipo', 'data', 'km', 'observacoes']

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['modelo', 'ano', 'km_atual']