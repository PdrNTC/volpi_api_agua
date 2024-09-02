from django.db import models
from django.db.models import Sum
from django.utils import timezone

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    peso = models.FloatField(help_text="Informe seu peso em KG")

    ## Retornando o nome por default ##
    def __str__(self):
        return self.nome

class AguaIngerida(models.Model):
    # Relacionando o usuário como chave estrangeira, e caso for deletado apagar em ambos models #
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    qtd_agua = models.IntegerField(help_text="Informe a quantidade de água ingerida em ML.")
    data = models.DateField(default=timezone.now)  # Agora permite data customizada
    #data = models.DateField(auto_now_add=True)


    def meta_diaria(self):
        meta_ingestao = self.usuario.peso * 35
        return meta_ingestao
    
    def total_agua_ingerida(self):
        total = AguaIngerida.objects.filter(usuario=self.usuario, data=self.data).aggregate(total=Sum('qtd_agua'))['total'] or 0
        return total
    
    def quantidade_faltante(self):
        # Fazendo a subtração para encontrar a quantidade que falta a ser ingerida.
        qtd_a_ingerir = self.meta_diaria() - self.total_agua_ingerida()
        return qtd_a_ingerir