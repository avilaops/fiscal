"""
Script para verificar qualidade de código
Executa: formatação, linting, type checking e testes
"""
import subprocess
import sys


def run_command(command, description):
    """Executa comando e retorna resultado"""
    print(f"\n{'='*60}")
    print(f"▶ {description}")
    print(f"{'='*60}")
    
    result = subprocess.run(command, shell=True, capture_output=False)
    
    if result.returncode != 0:
        print(f"✗ {description} - FALHOU")
        return False
    
    print(f"✓ {description} - OK")
    return True


def main():
    """Executa todas as verificações"""
    
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║           Verificação de Qualidade de Código               ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    checks = [
        ("black --check .", "Verificar formatação (Black)"),
        ("isort --check-only .", "Verificar imports (isort)"),
        ("flake8 .", "Linting (Flake8)"),
        ("python manage.py check", "Verificar configuração Django"),
        ("python manage.py test", "Executar testes"),
    ]
    
    results = []
    
    for command, description in checks:
        success = run_command(command, description)
        results.append((description, success))
    
    # Resumo
    print(f"\n{'='*60}")
    print("RESUMO")
    print(f"{'='*60}")
    
    failed = 0
    for description, success in results:
        status = "✓ PASSOU" if success else "✗ FALHOU"
        print(f"{status}: {description}")
        if not success:
            failed += 1
    
    print(f"\n{'='*60}")
    if failed == 0:
        print("✓ Todas as verificações passaram!")
        print(f"{'='*60}")
        return 0
    else:
        print(f"✗ {failed} verificação(ões) falharam")
        print(f"{'='*60}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
