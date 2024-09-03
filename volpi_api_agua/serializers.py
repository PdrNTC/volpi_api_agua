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
        return obj.peso * 35

    def get_total_agua_ingerida(self, obj):
        data = self.context.get('data', timezone.now().date())  # Obtém a data do contexto
        total = AguaIngerida.objects.filter(usuario=obj, data=data).aggregate(total=Sum('qtd_agua'))['total'] or 0
        return total


    def get_quantidade_faltante(self, obj):
        return self.get_meta_diaria(obj) - self.get_total_agua_ingerida(obj)


class AguaIngeridaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AguaIngerida
        fields = ['usuario', 'qtd_agua', 'data']


class AguaIngeridaSerializer(serializers.ModelSerializer):
    data = serializers.DateField()
    total_agua = serializers.IntegerField()
    meta_diaria = serializers.IntegerField()
    atingiu_meta = serializers.BooleanField()
    nome_usuario = serializers.CharField()
    peso_usuario = serializers.FloatField()  # Novo campo para exibir o peso do usuário
    class Meta:
        model = AguaIngerida
        fields = ['data', 'total_agua', 'meta_diaria', 'atingiu_meta', 'nome_usuario', 'peso_usuario']