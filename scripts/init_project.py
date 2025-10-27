"""
Script para inicializar o projeto
Cria banco, executa migrations e cria superusuário
"""
import os
import sys
import subprocess


def run_command(command, description):
    """Executa comando shell"""
    print(f"\n{'='*60}")
    print(f"▶ {description}")
    print(f"{'='*60}")
    
    result = subprocess.run(command, shell=True)
    
    if result.returncode != 0:
        print(f"✗ Erro ao executar: {description}")
        return False
    
    print(f"✓ {description} - Concluído")
    return True


def main():
    """Inicializa o projeto"""
    
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║           Sistema Fiscal - Inicialização                   ║
    ║                                                             ║
    ║   Este script irá:                                         ║
    ║   1. Verificar dependências                                ║
    ║   2. Executar migrations                                   ║
    ║   3. Coletar arquivos estáticos                            ║
    ║   4. Criar superusuário                                    ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # 1. Verificar se arquivo .env existe
    if not os.path.exists('.env'):
        print("⚠️  Arquivo .env não encontrado!")
        print("   Copie .env.example para .env e configure as variáveis")
        print("   Comando: cp .env.example .env")
        sys.exit(1)
    
    print("✓ Arquivo .env encontrado")
    
    # 2. Executar migrations
    if not run_command('python manage.py makemigrations', 'Criando migrations'):
        sys.exit(1)
    
    if not run_command('python manage.py migrate', 'Executando migrations'):
        sys.exit(1)
    
    # 3. Coletar arquivos estáticos
    if not run_command('python manage.py collectstatic --noinput', 'Coletando arquivos estáticos'):
        print("⚠️  Erro ao coletar estáticos (pode ser ignorado em dev)")
    
    # 4. Criar superusuário
    if not run_command('python scripts/create_superuser.py', 'Criando superusuário'):
        print("⚠️  Erro ao criar superusuário (pode já existir)")
    
    print(f"""
    ╔════════════════════════════════════════════════════════════╗
    ║                  ✓ Inicialização Concluída                 ║
    ╚════════════════════════════════════════════════════════════╝
    
    Para iniciar o servidor de desenvolvimento:
    
      python manage.py runserver
    
    Acesse: http://localhost:8000
    
    Login padrão:
      Usuário: admin
      Senha: admin123
    
    ⚠️  IMPORTANTE: Altere a senha do admin em produção!
    """)


if __name__ == '__main__':
    main()
