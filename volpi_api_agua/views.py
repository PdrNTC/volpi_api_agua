from volpi_api_agua.models import Usuario
from volpi_api_agua.serializers import UsuarioSerializer
from rest_framework import viewsets

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all() #Retornando todos os campos
    serializer_class = UsuarioSerializer
