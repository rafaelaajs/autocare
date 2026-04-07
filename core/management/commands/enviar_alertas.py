from django.core.management.base import BaseCommand
from core.services.alert_service import verificar_e_enviar_alertas


class Command(BaseCommand):
    help = 'Envia alertas de manutenção por email'

    def handle(self, *args, **kwargs):
        verificar_e_enviar_alertas()
        self.stdout.write(self.style.SUCCESS('Alertas enviados com sucesso!'))