"""
Testes para o módulo Core
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from core.models import NFe, NFeItem, CTe
from datetime import datetime
from decimal import Decimal


class NFeModelTest(TestCase):
    """Testes para o modelo NFe"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.nfe = NFe.objects.create(
            chave_acesso='12345678901234567890123456789012345678901234',
            numero_nf='123',
            serie='1',
            emit_cnpj='12345678000190',
            emit_nome='Empresa Teste',
            valor_total=Decimal('1000.00'),
            usuario_importacao=self.user
        )

    def test_nfe_creation(self):
        """Testa criação de NFe"""
        self.assertEqual(self.nfe.numero_nf, '123')
        self.assertEqual(self.nfe.emit_cnpj, '12345678000190')
        self.assertEqual(self.nfe.valor_total, Decimal('1000.00'))

    def test_nfe_str(self):
        """Testa representação string de NFe"""
        expected = f"NFe {self.nfe.numero_nf} - {self.nfe.emit_nome}"
        self.assertEqual(str(self.nfe), expected)

    def test_chave_acesso_unique(self):
        """Testa unicidade da chave de acesso"""
        with self.assertRaises(Exception):
            NFe.objects.create(
                chave_acesso='12345678901234567890123456789012345678901234',
                numero_nf='124',
                usuario_importacao=self.user
            )


class NFeItemModelTest(TestCase):
    """Testes para o modelo NFeItem"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.nfe = NFe.objects.create(
            chave_acesso='12345678901234567890123456789012345678901234',
            numero_nf='123',
            usuario_importacao=self.user
        )
        
        self.item = NFeItem.objects.create(
            nfe=self.nfe,
            numero_item=1,
            descricao='Produto Teste',
            quantidade=Decimal('10.00'),
            valor_unitario=Decimal('100.00'),
            valor_total=Decimal('1000.00')
        )

    def test_item_creation(self):
        """Testa criação de item de NFe"""
        self.assertEqual(self.item.numero_item, 1)
        self.assertEqual(self.item.descricao, 'Produto Teste')
        self.assertEqual(self.item.nfe, self.nfe)

    def test_item_relationship(self):
        """Testa relacionamento NFe -> Items"""
        self.assertEqual(self.nfe.itens.count(), 1)
        self.assertEqual(self.nfe.itens.first(), self.item)


class ViewsTest(TestCase):
    """Testes para as views"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_login_view_get(self):
        """Testa acesso à página de login"""
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')

    def test_login_view_post_valid(self):
        """Testa login com credenciais válidas"""
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect

    def test_login_view_post_invalid(self):
        """Testa login com credenciais inválidas"""
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'inválid')

    def test_dashboard_requires_login(self):
        """Testa que dashboard requer autenticação"""
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_dashboard_authenticated(self):
        """Testa acesso ao dashboard autenticado"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/dashboard.html')
