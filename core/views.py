from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Veiculo, Manutencao, TipoManutencao
from .forms import ManutencaoForm


# 🚗 DASHBOARD
@login_required
def dashboard(request):
    veiculos = Veiculo.objects.filter(usuario=request.user)
    tipos = TipoManutencao.objects.all()

    dados = []

    for veiculo in veiculos:

        # 🔥 PRIMEIRA manutenção (base inicial)
        primeira_manutencao = Manutencao.objects.filter(
            veiculo=veiculo
        ).order_by('km').first()

        # valor padrão (caso não exista nada)
        km_base = veiculo.km_atual

        if primeira_manutencao:
            km_base = primeira_manutencao.km

        for tipo in tipos:
            ultima = Manutencao.ultima_manutencao(veiculo, tipo)

            if ultima:
                dados.append({
                    'veiculo': veiculo,
                    'tipo': tipo,
                    'ultima_data': ultima.data,
                    'ultimo_km': ultima.km,
                    'proxima_data': ultima.proxima_data(),
                    'proximo_km': ultima.proximo_km(),
                    'alerta': ultima.precisa_alerta(),
                    'sem_historico': False
                })
            else:
                proximo_km = None

                if tipo.frequencia_km:
                    proximo_km = km_base + tipo.frequencia_km

                dados.append({
                    'veiculo': veiculo,
                    'tipo': tipo,
                    'ultima_data': None,
                    'ultimo_km': km_base,
                    'proxima_data': None,
                    'proximo_km': proximo_km,
                    'alerta': True,
                    'sem_historico': True
                })

    return render(request, 'dashboard.html', {'dados': dados})


# ➕ ADICIONAR MANUTENÇÃO
@login_required
def adicionar_manutencao(request):
    if request.method == 'POST':
        form = ManutencaoForm(request.POST)
        if form.is_valid():
            manutencao = form.save(commit=False)
            manutencao.save()
            return redirect('dashboard')
    else:
        initial_data = {}

        # 🔥 parâmetros da URL (pré-preenchimento)
        veiculo_id = request.GET.get('veiculo')
        tipo_id = request.GET.get('tipo')

        if veiculo_id:
            initial_data['veiculo'] = veiculo_id

        if tipo_id:
            initial_data['tipo'] = tipo_id

        form = ManutencaoForm(initial=initial_data)

    # 🔒 filtrar veículos do usuário
    form.fields['veiculo'].queryset = Veiculo.objects.filter(usuario=request.user)

    return render(request, 'adicionar_manutencao.html', {'form': form})


# 📊 HISTÓRICO
@login_required
def historico(request):
    manutencoes = Manutencao.objects.filter(
        veiculo__usuario=request.user
    ).order_by('-data')

    return render(request, 'historico.html', {
        'manutencoes': manutencoes
    })

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()

    return render(request, 'cadastro.html', {'form': form})

@login_required
def veiculos(request):
    veiculos = Veiculo.objects.filter(usuario=request.user)

    return render(request, 'veiculos.html', {
        'veiculos': veiculos
    })

from .forms import VeiculoForm
from django.shortcuts import get_object_or_404


# ➕ CADASTRAR
@login_required
def adicionar_veiculo(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            veiculo = form.save(commit=False)
            veiculo.usuario = request.user
            veiculo.save()
            return redirect('veiculos')
    else:
        form = VeiculoForm()

    return render(request, 'veiculo_form.html', {'form': form})


# ✏️ EDITAR
@login_required
def editar_veiculo(request, id):
    veiculo = get_object_or_404(Veiculo, id=id, usuario=request.user)

    if request.method == 'POST':
        form = VeiculoForm(request.POST, instance=veiculo)
        if form.is_valid():
            form.save()
            return redirect('veiculos')
    else:
        form = VeiculoForm(instance=veiculo)

    return render(request, 'veiculo_form.html', {'form': form})


# ❌ DELETAR
@login_required
def deletar_veiculo(request, id):
    veiculo = get_object_or_404(Veiculo, id=id, usuario=request.user)

    if request.method == 'POST':
        veiculo.delete()
        return redirect('veiculos')

    return render(request, 'confirmar_delete.html', {'veiculo': veiculo})