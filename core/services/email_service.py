from django.core.mail import send_mail

def enviar_alerta_email(usuario_email, assunto, mensagem):
    send_mail(
        assunto,
        mensagem,
        None,
        [usuario_email],
        fail_silently=False,
    )