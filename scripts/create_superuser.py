"""
Script para criar superusuário no Django
"""
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xml_manager.settings')
django.setup()

from django.contrib.auth.models import User


def create_superuser():
    """Cria superusuário se não existir"""
    
    username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@fiscal.com')
    password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin123')
    
    if User.objects.filter(username=username).exists():
        print(f"✓ Superusuário '{username}' já existe")
        return
    
    try:
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✓ Superusuário '{username}' criado com sucesso")
        print(f"  Email: {email}")
        print(f"  Senha: {password}")
        print("\n⚠️  IMPORTANTE: Altere a senha em produção!")
    
    except Exception as e:
        print(f"✗ Erro ao criar superusuário: {e}")
        sys.exit(1)


if __name__ == '__main__':
    create_superuser()
