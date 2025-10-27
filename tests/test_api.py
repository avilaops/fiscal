"""
Testes para a API REST
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from core.models import NFe, CTe
from decimal import Decimal


class NFeAPITest(TestCase):
    """Testes para a API de NFe"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Criar NFe de teste
        self.nfe = NFe.objects.create(
            chave_acesso='12345678901234567890123456789012345678901234',
            numero_nf='123',
            serie='1',
            emit_cnpj='12345678000190',
            emit_nome='Empresa Teste',
            valor_total=Decimal('1000.00'),
            usuario_importacao=self.user
        )

    def test_nfe_list_requires_authentication(self):
        """Testa que listar NFes requer autenticação"""
        response = self.client.get('/api/nfe/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_nfe_list_authenticated(self):
        """Testa listagem de NFes autenticado"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/nfe/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_nfe_detail(self):
        """Testa detalhes de uma NFe"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/nfe/{self.nfe.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['numero_nf'], '123')

    def test_nfe_search(self):
        """Testa busca de NFes"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/nfe/?search=Teste')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_nfe_filter_by_cnpj(self):
        """Testa filtro por CNPJ"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/nfe/?cnpj=12345678000190')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DashboardAPITest(TestCase):
    """Testes para a API de Dashboard"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_dashboard_requires_authentication(self):
        """Testa que dashboard requer autenticação"""
        response = self.client.get('/api/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_dashboard_authenticated(self):
        """Testa acesso ao dashboard autenticado"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica estrutura da resposta
        self.assertIn('nfe_stats', response.data)
        self.assertIn('cte_stats', response.data)
