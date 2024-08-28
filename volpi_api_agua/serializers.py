from rest_framework import serializers
from volpi_api_agua.models import Usuario, AguaIngerida

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class AguaIngeridaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AguaIngerida
        fields = ['id', 'usuario', 'qtd_agua', 'data', 'meta_diaria', 'total_agua_ingerida', 'quantidade_faltante']
        #fields = '__all__' # Não estava retornando os gets #

    def get_meta_diaria(self, obj):
        return obj.meta_diaria()

    def get_total_agua_ingerida(self, obj):
        return obj.total_agua_ingerida()

    def get_quantidade_faltante(self, obj):
        return obj.quantidade_faltante()        