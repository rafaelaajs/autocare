from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.utils import timezone

from .models import Veiculo, Manutencao, TipoManutencao
from .forms import ManutencaoForm, VeiculoForm


# 🚗 DASHBOARD
@login_required
def dashboard(request):
    veiculos = Veiculo.objects.filter(usuario=request.user)
    tipos = TipoManutencao.objects.all()

    dados = []

    for veiculo in veiculos:

        primeira_manutencao = Manutencao.objects.filter(
            veiculo=veiculo
        ).order_by('km').first()

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

    tem_veiculo = veiculos.exists()
    tem_manutencao = Manutencao.objects.filter(
        veiculo__usuario=request.user
    ).exists()

    contexto = {
        'dados': dados,
        'tem_veiculo': tem_veiculo,
        'tem_manutencao': tem_manutencao
    }

    return render(request, 'dashboard.html', contexto)


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

        veiculo_id = request.GET.get('veiculo')
        tipo_id = request.GET.get('tipo')

        if veiculo_id:
            initial_data['veiculo'] = veiculo_id

        if tipo_id:
            initial_data['tipo'] = tipo_id

        form = ManutencaoForm(initial=initial_data)

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


# ✏️ EDITAR MANUTENÇÃO
@login_required
def editar_manutencao(request, id):
    manutencao = get_object_or_404(
        Manutencao,
        id=id,
        veiculo__usuario=request.user
    )

    if request.method == 'POST':
        form = ManutencaoForm(request.POST, instance=manutencao)
        if form.is_valid():
            form.save()
            return redirect('historico')  # 🔥 melhor UX
    else:
        form = ManutencaoForm(instance=manutencao)

    return render(request, 'adicionar_manutencao.html', {'form': form})


# ❌ DELETAR MANUTENÇÃO
@login_required
def deletar_manutencao(request, id):
    manutencao = get_object_or_404(
        Manutencao,
        id=id,
        veiculo__usuario=request.user
    )

    if request.method == 'POST':
        manutencao.delete()
        return redirect('historico')

    return render(request, 'confirmar_delete_manutencao.html'), {
        'manutencao': manutencao
    }


# 👤 CADASTRO
def cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('veiculos')
    else:
        form = UserCreationForm()

    return render(request, 'cadastro.html', {'form': form})


# 🚗 VEÍCULOS
@login_required
def veiculos(request):
    veiculos = Veiculo.objects.filter(usuario=request.user)

    return render(request, 'veiculos.html', {
        'veiculos': veiculos
    })


# ➕ ADICIONAR VEÍCULO
@login_required
def adicionar_veiculo(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            veiculo = form.save(commit=False)
            veiculo.usuario = request.user
            veiculo.save()
            return redirect('dashboard')
    else:
        form = VeiculoForm()

    return render(request, 'veiculo_form.html', {'form': form})


# ✏️ EDITAR VEÍCULO
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


# ❌ DELETAR VEÍCULO
@login_required
def deletar_veiculo(request, id):
    veiculo = get_object_or_404(Veiculo, id=id, usuario=request.user)

    if request.method == 'POST':
        veiculo.delete()
        return redirect('veiculos')

    return render(request, 'confirmar_delete.html', {'veiculo': veiculo})


# 🚨 ALERTAS
@login_required
def alertas(request):
    veiculos = Veiculo.objects.filter(usuario=request.user)
    tipos = TipoManutencao.objects.all()

    hoje = timezone.now().date()
    lista_alertas = []

    for veiculo in veiculos:
        for tipo in tipos:
            ultima = Manutencao.ultima_manutencao(veiculo, tipo)

            if not ultima:
                continue

            proxima_data = ultima.proxima_data()

            if not proxima_data:
                continue

            dias = (proxima_data - hoje).days
            dias_exibicao = abs(dias)

            if dias <= 0:
                nivel = "vencido"
            elif dias <= 7:
                nivel = "proximo"
            else:
                continue

            lista_alertas.append({
                "veiculo": veiculo,
                "tipo": tipo,
                "proxima_data": proxima_data,
                "dias": dias,
                "dias_exibicao": dias_exibicao,
                "nivel": nivel
            })

    lista_alertas = sorted(lista_alertas, key=lambda x: x["dias"])

    return render(request, "alertas.html", {
        "alertas": lista_alertas
    })