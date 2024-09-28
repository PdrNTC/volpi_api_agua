from django.contrib import admin
from django.urls import path, include

from volpi_api_agua.views import UsuarioViewSet, AguaIngeridaViewSet, GerarPDFView
from rest_framework import routers

# Criando Objeto Router #
router = routers.DefaultRouter()
router.register('usuarios', UsuarioViewSet, basename='Usuarios') 
router.register('agua_ingerida', AguaIngeridaViewSet, basename='agua_ingerida') 
#router.register('gerar-pdf', GerarPDFView, basename='gerar-pdf') 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)), # Incluindo todas as rota com o objeto router #
    path('gerar-pdf/', GerarPDFView.as_view(), name='gerar-pdf'),
]
