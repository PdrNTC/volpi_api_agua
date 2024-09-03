from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Usuario, AguaIngerida

class AguaIngeridaTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.usuario = Usuario.objects.create(nome="PedroTEST", peso=75)

    ## TESTE PARA CONSUMO DE ÁGUA PASSANDO USER_ID QTD_AGUA E DATA ##
    def test_registrar_consumo_agua(self):
        response = self.client.post('/agua_ingerida/', {
            'usuario': self.usuario.id,
            'qtd_agua': 500,
            'data': '2024-09-04'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    ## TESTE - CONSULTAR HISTORICO ##
    def test_consultar_historico_agua(self):
        AguaIngerida.objects.create(usuario=self.usuario, qtd_agua=500, data='2024-09-04')
        response = self.client.get(reverse('agua_ingerida-list'), {'usuario_id': self.usuario.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
