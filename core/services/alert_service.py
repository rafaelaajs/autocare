from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from core.models import Manutencao


def enviar_email(manutencao, usuario, mensagem):
    send_mail(
        subject='🚗 AutoCare - Alerta de Manutenção',
        message=f'{mensagem}\n\n{manutencao.tipo.nome} - {manutencao.veiculo.modelo}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[usuario.email],
    )
    


def verificar_e_enviar_alertas():
    hoje = timezone.now().date()
    manutencoes = Manutencao.objects.all()

    for m in manutencoes:
        proxima_data = m.proxima_data()

        if not proxima_data:
            continue

        usuario = m.veiculo.usuario
        dias = (proxima_data - hoje).days

        # 🔔 7 dias antes
        if dias == 7 and not getattr(m, 'alerta_7_dias_antes', False):
            enviar_email(m, usuario, "🔔 Sua manutenção vence em 7 dias")
            m.alerta_7_dias_antes = True
            m.save()

        # 🔔 no dia
        elif dias == 0 and not getattr(m, 'alerta_no_dia', False):
            enviar_email(m, usuario, "⚠️ Sua manutenção vence hoje")
            m.alerta_no_dia = True
            m.save()

        # 🔔 atrasado (qualquer dia depois)
        elif dias < 0 and not getattr(m, 'alerta_atrasado', False):
            enviar_email(m, usuario, "🚨 Manutenção atrasada")
            m.alerta_atrasado = True
            m.save()