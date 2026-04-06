from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Veiculo, Manutencao, Categoria, TipoManutencao

admin.site.register(Veiculo)
admin.site.register(Manutencao)
admin.site.register(Categoria)
admin.site.register(TipoManutencao)
