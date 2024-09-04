from volpi_api_agua.models import Usuario, AguaIngerida
from volpi_api_agua.serializers import UsuarioSerializer, AguaIngeridaSerializer, AguaIngeridaCreateSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Sum, F, BooleanField,When, Case
from django_q.tasks import async_task  # Importar Django-Q para tarefas assíncronas

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
    
## VIEW para gerar o pdf no endpoint 'gerar-pdf' ##
class GerarPDFView(APIView):
    def post(self, request, *args, **kwargs):
        usuario_id = request.data.get('usuario_id')
        if not usuario_id:
            return Response({"error": "ID do usuário é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Enfileirar a tarefa assíncrona para gerar o PDF usando Django-Q
        async_task('volpi_api_agua.tasks.gerar_pdf_historico_usuario', usuario_id)

        return Response({"message": "PDF sendo gerado, você será notificado quando estiver pronto."}, status=status.HTTP_200_OK)