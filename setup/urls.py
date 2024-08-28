from django.contrib import admin
from django.urls import path, include

from volpi_api_agua.views import UsuarioViewSet
from rest_framework import routers

# Criando Objeto Router #
router = routers.DefaultRouter()
router.register('usuarios', UsuarioViewSet, basename='Usuarios') 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)), # Incluindo a rota com o objeto router #
]
