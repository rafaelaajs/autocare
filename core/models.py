from django.db import models
from django.contrib.auth.models import User

# 🔹 Categoria (nível mais alto)
class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


# 🔹 Tipo de manutenção (ligado à categoria)
class TipoManutencao(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    frequencia_dias = models.IntegerField(null=True, blank=True)
    frequencia_km = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nome


# 🔹 Veículo

class Veiculo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    marca = models.CharField(max_length=100, default="")
    modelo = models.CharField(max_length=100)
    ano = models.IntegerField()
    km_atual = models.IntegerField()

    def __str__(self):
        return f"{self.marca} {self.modelo}"


from datetime import timedelta
from django.utils import timezone

class Manutencao(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoManutencao, on_delete=models.CASCADE)
    data = models.DateField()
    km = models.IntegerField()
    observacoes = models.TextField(blank=True)

      # NOVOS CAMPOS DE ALERTAS
    alerta_7_dias_antes = models.BooleanField(default=False)
    alerta_no_dia = models.BooleanField(default=False)
    alerta_7_dias_depois = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tipo.nome} - {self.veiculo}"

    # 🔥 MÉTODOS

    def proxima_data(self):
        if self.tipo.frequencia_dias:
            return self.data + timedelta(days=self.tipo.frequencia_dias)
        return None

    def proximo_km(self):
        if self.tipo.frequencia_km:
            return self.km + self.tipo.frequencia_km
        return None

    def precisa_alerta(self):
        hoje = timezone.now().date()
        km_atual = self.veiculo.km_atual

        alerta_data = False
        alerta_km = False

        proxima_data = self.proxima_data()
        proximo_km = self.proximo_km()

        if proxima_data:
            alerta_data = hoje >= proxima_data

        if proximo_km:
            alerta_km = km_atual >= proximo_km

        return alerta_data or alerta_km

    # 🔥 NOVO MÉTODO (IMPORTANTE)
    @classmethod
    def ultima_manutencao(cls, veiculo, tipo):
        return cls.objects.filter(
            veiculo=veiculo,
            tipo=tipo
        ).order_by('-data').first()