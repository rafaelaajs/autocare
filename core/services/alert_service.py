from datetime import timedelta
from django.utils import timezone

from core.services.email_service import enviar_alerta_email
from core.models import Manutencao  # ⚠️ ajustar se necessário


def verificar_e_enviar_alertas():
    hoje = timezone.now().date()

    manutencoes = Manutencao.objects.select_related(
        'veiculo', 'tipo', 'veiculo__usuario'
    )

    for m in manutencoes:
        usuario = m.veiculo.usuario
        proxima_data = m.proxima_data()
        proximo_km = m.proximo_km()

        # ------------------------
        # 📅 ALERTAS POR DATA
        # ------------------------
        if proxima_data:

            # ⏳ 7 dias antes
            if hoje == (proxima_data - timedelta(days=7)) and not m.alerta_7_dias_antes:
                enviar_email(m, usuario, "⏳ Sua manutenção está próxima (7 dias)")
                m.alerta_7_dias_antes = True
                m.save()

            # 🚨 no dia
            elif hoje == proxima_data and not m.alerta_no_dia:
                enviar_email(m, usuario, "🚨 Sua manutenção vence hoje")
                m.alerta_no_dia = True
                m.save()

            # ⚠️ 7 dias depois
            elif hoje == (proxima_data + timedelta(days=7)) and not m.alerta_7_dias_depois:
                enviar_email(m, usuario, "⚠️ Manutenção atrasada (7 dias)")
                m.alerta_7_dias_depois = True
                m.save()

        # ------------------------
        # 🚗 ALERTA POR KM
        # ------------------------
        if proximo_km:
            if m.veiculo.km_atual >= proximo_km and not m.alerta_no_dia:
                enviar_email(m, usuario, "🚨 Manutenção por KM atingida")
                m.alerta_no_dia = True
                m.save()


def enviar_email(manutencao, usuario, assunto):
    mensagem = f"""
Olá, {usuario.username}!

A manutenção "{manutencao.tipo.nome}" do seu veículo {manutencao.veiculo.modelo} precisa de atenção.

📅 Última manutenção: {manutencao.data}
🚗 KM na última manutenção: {manutencao.km}

Acesse o AutoCare para mais detalhes.

- Equipe AutoCare
"""
    enviar_alerta_email(usuario.email, assunto, mensagem)