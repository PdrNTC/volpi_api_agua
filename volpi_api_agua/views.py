from volpi_api_agua.models import Usuario, AguaIngerida
from volpi_api_agua.serializers import UsuarioSerializer, AguaIngeridaSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from django.utils import timezone

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all() #Retornando todos os campos
    serializer_class = UsuarioSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['data'] = self.request.query_params.get('data', timezone.now().date())
        return context

class AguaIngeridaViewSet(viewsets.ModelViewSet):
    serializer_class = AguaIngeridaSerializer

    def get_queryset(self):
        queryset = AguaIngerida.objects.all()
        usuario_id = self.request.query_params.get('usuario_id', None)
        data = self.request.query_params.get('data', None)
        if usuario_id is not None:
            queryset = queryset.filter(usuario_id=usuario_id).order_by('data')
        if data is not None:
            queryset = queryset.filter(data=data)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)