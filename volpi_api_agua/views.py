from volpi_api_agua.models import Usuario, AguaIngerida
from volpi_api_agua.serializers import UsuarioSerializer, AguaIngeridaSerializer
from rest_framework import viewsets

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all() #Retornando todos os campos
    serializer_class = UsuarioSerializer

class AguaIngeridaViewSet(viewsets.ModelViewSet):
    queryset = AguaIngerida.objects.all()
    serializer_class = AguaIngeridaSerializer