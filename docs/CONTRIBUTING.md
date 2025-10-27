# Guia de Contribuição

Obrigado por considerar contribuir com o Sistema Fiscal! Este documento fornece diretrizes para contribuir com o projeto.

## 🎯 Como Contribuir

### 1. Reportar Bugs

Ao reportar bugs, inclua:
- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs. atual
- Screenshots (se aplicável)
- Versão do Python e Django
- Sistema operacional

**Template:**
```markdown
**Descrição do Bug:**
[Descrição clara]

**Para Reproduzir:**
1. Faça X
2. Clique em Y
3. Veja erro Z

**Esperado:**
[O que deveria acontecer]

**Atual:**
[O que acontece]

**Ambiente:**
- Python: 3.11
- Django: 4.2.25
- OS: Windows 11
```

### 2. Sugerir Melhorias

Para sugestões de features:
- Descreva o problema que resolve
- Explique a solução proposta
- Considere alternativas
- Impacto em usuários existentes

### 3. Pull Requests

#### Antes de Submeter

1. **Fork o repositório**
2. **Crie uma branch:**
   ```bash
   git checkout -b feature/minha-feature
   # ou
   git checkout -b fix/meu-bugfix
   ```

3. **Faça suas alterações**
4. **Teste suas mudanças:**
   ```bash
   python manage.py test
   ```

5. **Commit com mensagem clara:**
   ```bash
   git commit -m "feat: adiciona validação de CNPJ"
   # ou
   git commit -m "fix: corrige cálculo de impostos"
   ```

6. **Push para o fork:**
   ```bash
   git push origin feature/minha-feature
   ```

7. **Abra o Pull Request**

#### Mensagens de Commit

Use o padrão [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação de código
- `refactor:` Refatoração
- `test:` Testes
- `chore:` Tarefas de manutenção

**Exemplos:**
```bash
feat: adiciona endpoint para exportar NFes em PDF
fix: corrige validação de data de emissão
docs: atualiza README com instruções Docker
refactor: reorganiza estrutura de models
test: adiciona testes para NFeSerializer
```

## 📝 Padrões de Código

### Python/Django

Siga [PEP 8](https://pep8.org/) e [Django Coding Style](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/):

**Boas práticas:**
```python
# ✅ BOM
class NFe(models.Model):
    """Nota Fiscal Eletrônica"""
    
    chave_acesso = models.CharField(
        max_length=44,
        unique=True,
        db_index=True,
        help_text="Chave de acesso de 44 dígitos"
    )
    
    def __str__(self):
        return f"NFe {self.numero_nf} - {self.emit_nome}"


# ❌ RUIM
class NFe(models.Model):
    chave_acesso=models.CharField(max_length=44)
    def __str__(self): return f"NFe {self.numero_nf}"
```

### Docstrings

Use docstrings em módulos, classes e funções:

```python
def processar_xml_nfe(xml_content, usuario):
    """
    Processa XML de NFe e salva no banco de dados.
    
    Args:
        xml_content (str): Conteúdo do XML da NFe
        usuario (User): Usuário que está importando
    
    Returns:
        NFe: Instância da NFe criada
    
    Raises:
        ValidationError: Se o XML for inválido
        IntegrityError: Se a chave já existir
    """
    # Implementação
    pass
```

### Imports

Organize imports em grupos:

```python
# 1. Standard library
import os
import sys
from datetime import datetime

# 2. Django
from django.db import models
from django.contrib.auth.models import User

# 3. Third party
from rest_framework import serializers

# 4. Local
from core.models import NFe
from .utils import validar_cnpj
```

### Nomes

- **Classes:** `PascalCase` (ex: `NFeSerializer`)
- **Funções/Métodos:** `snake_case` (ex: `processar_xml`)
- **Constantes:** `UPPER_CASE` (ex: `MAX_UPLOAD_SIZE`)
- **Variáveis:** `snake_case` (ex: `chave_acesso`)

## 🧪 Testes

### Escreva Testes

Todo código novo deve ter testes:

```python
from django.test import TestCase
from core.models import NFe


class NFeTestCase(TestCase):
    def setUp(self):
        self.nfe = NFe.objects.create(
            chave_acesso='12345678901234567890123456789012345678901234',
            numero_nf='123'
        )
    
    def test_nfe_creation(self):
        """Testa criação de NFe"""
        self.assertEqual(self.nfe.numero_nf, '123')
    
    def test_chave_acesso_unique(self):
        """Testa unicidade da chave de acesso"""
        with self.assertRaises(Exception):
            NFe.objects.create(
                chave_acesso='12345678901234567890123456789012345678901234'
            )
```

### Executar Testes

```bash
# Todos os testes
python manage.py test

# Teste específico
python manage.py test core.tests.test_models.NFeTestCase

# Com cobertura
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Cobertura Mínima

Mantenha cobertura de testes > 80%:
- Models: 90%+
- Views: 80%+
- Serializers: 80%+
- Utils: 90%+

## 📚 Documentação

### README

Atualize `README.md` ao adicionar:
- Novas dependências
- Variáveis de ambiente
- Comandos de instalação
- Funcionalidades principais

### Código

Documente:
- Funções complexas
- Classes públicas
- APIs
- Algoritmos não triviais

### API

Atualize `docs/API.md` ao:
- Adicionar endpoints
- Modificar responses
- Alterar autenticação

## 🔍 Code Review

Antes de aprovar um PR, verifique:

### Funcionalidade
- [ ] Código funciona como esperado
- [ ] Edge cases tratados
- [ ] Sem regressões

### Qualidade
- [ ] Segue padrões de código
- [ ] Variáveis bem nomeadas
- [ ] Funções pequenas e focadas
- [ ] Sem código duplicado

### Testes
- [ ] Testes passam
- [ ] Cobertura adequada
- [ ] Casos edge testados

### Documentação
- [ ] Código documentado
- [ ] README atualizado (se necessário)
- [ ] API docs atualizados (se necessário)

### Segurança
- [ ] Sem dados sensíveis expostos
- [ ] Validação de inputs
- [ ] Autorização verificada
- [ ] SQL injection prevenido

## 🚀 Fluxo de Trabalho

```
┌──────────────┐
│  Fork Repo   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Create Branch│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Code + Test │◄────┐
└──────┬───────┘     │
       │             │
       ▼             │
┌──────────────┐     │
│    Commit    │     │
└──────┬───────┘     │
       │             │
       ▼             │
┌──────────────┐     │
│  Push Branch │     │
└──────┬───────┘     │
       │             │
       ▼             │
┌──────────────┐     │
│  Open PR     │     │
└──────┬───────┘     │
       │             │
       ▼             │
┌──────────────┐     │
│ Code Review  │     │
└──────┬───────┘     │
       │             │
       ▼             │
┌──────────────┐     │
│  Requested   │─────┘
│   Changes?   │
└──────┬───────┘
       │ No
       ▼
┌──────────────┐
│    Merge     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│    Deploy    │
└──────────────┘
```

## 📋 Checklist do PR

Ao abrir um PR, verifique:

```markdown
## Descrição
[Descreva as mudanças]

## Tipo de Mudança
- [ ] Bug fix
- [ ] Nova feature
- [ ] Breaking change
- [ ] Documentação

## Checklist
- [ ] Código segue padrões do projeto
- [ ] Self-review realizado
- [ ] Comentários em código complexo
- [ ] Documentação atualizada
- [ ] Sem warnings
- [ ] Testes adicionados/atualizados
- [ ] Todos os testes passam
- [ ] Mudanças dependentes mergeadas

## Como Testar
1. [Passo 1]
2. [Passo 2]

## Screenshots (se aplicável)
[Adicione screenshots]
```

## 🤝 Código de Conduta

### Nossa Promessa

Criar um ambiente aberto e acolhedor para todos.

### Comportamento Esperado

- Use linguagem acolhedora e inclusiva
- Respeite diferentes pontos de vista
- Aceite críticas construtivas
- Foque no que é melhor para a comunidade
- Mostre empatia

### Comportamento Inaceitável

- Linguagem ou imagens sexualizadas
- Trolling ou comentários insultuosos
- Assédio público ou privado
- Publicar informações privadas sem permissão
- Conduta não profissional

## 📧 Contato

Dúvidas sobre contribuição?

- **Email:** suporte@aviladevops.com.br
- **Issues:** Use o GitHub Issues
- **Discussões:** Use GitHub Discussions

---

**Obrigado por contribuir! 🎉**
