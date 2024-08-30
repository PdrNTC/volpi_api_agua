from rest_framework import serializers
from volpi_api_agua.models import Usuario, AguaIngerida
from django.db.models import Sum
from django.db import models
from django.utils import timezone

class UsuarioSerializer(serializers.ModelSerializer):
    meta_diaria = serializers.SerializerMethodField()
    total_agua_ingerida = serializers.SerializerMethodField()
    quantidade_faltante = serializers.SerializerMethodField()
    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'peso', 'meta_diaria', 'total_agua_ingerida', 'quantidade_faltante']

    def get_meta_diaria(self, obj):
        # Calcula a meta diária com base no peso do usuário
        return obj.peso * 35

    def get_total_agua_ingerida(self, obj):
        # Calcula a quantidade total de água ingerida hoje data atual
        today = timezone.now().date()
        total = AguaIngerida.objects.filter(usuario=obj, data=today).aggregate(total=Sum('qtd_agua'))['total'] or 0
        return total
    
    def get_quantidade_faltante(self, obj):
        # Calcula quanto falta para atingir a meta diária subtraindo a meta pela ingestão
        return self.get_meta_diaria(obj) - self.get_total_agua_ingerida(obj)

class AguaIngeridaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AguaIngerida
        fields = ['id', 'usuario', 'qtd_agua', 'data', 'meta_diaria', 'total_agua_ingerida', 'quantidade_faltante']
        #fields = '__all__' # Não estava retornando os gets #
 