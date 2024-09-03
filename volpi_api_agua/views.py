from volpi_api_agua.models import Usuario, AguaIngerida
from volpi_api_agua.serializers import UsuarioSerializer, AguaIngeridaSerializer, AguaIngeridaCreateSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Sum, F, BooleanField,When, Case
from django.db.models.functions import Coalesce

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all() #Retornando todos os campos
    serializer_class = UsuarioSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['data'] = self.request.query_params.get('data', timezone.now().date())
        return context

class AguaIngeridaViewSet(viewsets.ModelViewSet):
    serializer_class = AguaIngeridaSerializer

    ## FILTRANDO O USUÁRIO E APLICANDO A LÓGICA DE CÁLCULO DE PESO X 35 ##
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AguaIngeridaCreateSerializer
        return AguaIngeridaSerializer

    def get_queryset(self):
        usuario_id = self.request.query_params.get('usuario_id', None)
        if usuario_id is not None:
            queryset = AguaIngerida.objects.filter(usuario_id=usuario_id).values('data', 'usuario__nome', 'usuario__peso').annotate(
                total_agua=Sum('qtd_agua'),
                meta_diaria=F('usuario__peso') * 35,
                nome_usuario=F('usuario__nome'),
                peso_usuario=F('usuario__peso')
            ).order_by('data')

            # Adicionar a lógica de atingiu_meta
            queryset = queryset.annotate(
                atingiu_meta=Case(
                    When(total_agua__gte=F('meta_diaria'), then=True),
                    default=False,
                    output_field=BooleanField()
                )
            )
            return queryset
        return AguaIngerida.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)