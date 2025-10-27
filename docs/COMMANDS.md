# ⚡ Comandos Úteis - Referência Rápida

Todos os comandos mais usados em um só lugar!

---

## 🚀 Instalação & Inicialização

### Primeira Instalação

```bash
# Clone
git clone <repository-url>
cd web_app

# Ambiente virtual (Windows)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Ambiente virtual (Linux/Mac)
python3 -m venv venv
source venv/bin/activate

# Configurar
cp .env.example .env
# Edite o .env

# Instalar
pip install -r requirements.txt

# Inicializar
python scripts/init_project.py

# Rodar
python manage.py runserver
```

---

## 🐳 Docker

```bash
# Build
docker build -t fiscal-app .

# Run
docker run -p 8080:8080 --env-file .env fiscal-app

# Docker Compose
docker-compose up -d              # Subir
docker-compose down               # Parar
docker-compose logs -f            # Ver logs
docker-compose exec web bash     # Shell no container
```

---

## 🛠️ Makefile (Recomendado!)

```bash
make help              # Ver todos os comandos
make install           # Instalar dependências
make install-dev       # Instalar deps de dev
make run               # Rodar servidor
make test              # Executar testes
make coverage          # Testes com cobertura
make lint              # Verificar código (flake8)
make format            # Formatar código (black + isort)
make check             # Verificar qualidade completa
make migrate           # Executar migrations
make makemigrations    # Criar migrations
make superuser         # Criar superusuário
make collectstatic     # Coletar estáticos
make init              # Inicializar projeto
make clean             # Limpar temp files
make docker-build      # Build Docker
make docker-up         # Docker Compose up
make docker-down       # Docker Compose down
make shell             # Django shell
make dbshell           # Database shell
```

---

## 📦 Django Management

### Desenvolvimento

```bash
# Servidor
python manage.py runserver
python manage.py runserver 0.0.0.0:8000  # Todas as interfaces
python manage.py runserver 8080          # Porta customizada

# Shell
python manage.py shell           # Python shell
python manage.py dbshell         # Database shell

# Verificações
python manage.py check           # Verificar projeto
python manage.py check --deploy  # Verificar para produção
```

### Banco de Dados

```bash
# Migrations
python manage.py makemigrations          # Criar migrations
python manage.py migrate                 # Aplicar migrations
python manage.py migrate --fake          # Marcar como aplicada
python manage.py showmigrations          # Ver status
python manage.py sqlmigrate core 0001    # Ver SQL

# Dados
python manage.py loaddata fixture.json   # Carregar dados
python manage.py dumpdata > data.json    # Exportar dados
python manage.py flush                   # Limpar database
```

### Usuários

```bash
# Criar superusuário
python manage.py createsuperuser
python scripts/create_superuser.py       # Automatizado

# Mudar senha
python manage.py changepassword admin
```

### Arquivos Estáticos

```bash
# Coletar estáticos
python manage.py collectstatic
python manage.py collectstatic --noinput
python manage.py collectstatic --clear   # Limpar primeiro
```

---

## 🧪 Testes

```bash
# Todos os testes
python manage.py test

# Teste específico
python manage.py test core.tests
python manage.py test core.tests.test_models
python manage.py test core.tests.test_models.NFeTestCase

# Com verbose
python manage.py test --verbosity=2

# Manter database
python manage.py test --keepdb

# Paralelo
python manage.py test --parallel

# Coverage
coverage run --source='.' manage.py test
coverage report
coverage html
# Abrir htmlcov/index.html
```

---

## 🎨 Code Quality

```bash
# Black (formatação)
black .                          # Formatar tudo
black core/ api/                 # Formatar pastas
black --check .                  # Apenas verificar
black --diff .                   # Ver diferenças

# isort (imports)
isort .                          # Organizar imports
isort --check-only .             # Apenas verificar
isort --diff .                   # Ver diferenças

# Flake8 (linting)
flake8 .                         # Verificar tudo
flake8 core/                     # Verificar pasta
flake8 --statistics .            # Com estatísticas

# Pylint
pylint core/ api/

# Mypy (type checking)
mypy .

# Verificação completa
python scripts/check_quality.py
```

---

## 📊 Git

```bash
# Configurar
git config user.name "Seu Nome"
git config user.email "seu@email.com"

# Branch
git checkout -b feature/nova-feature
git branch -D nome-branch         # Deletar local
git push origin --delete branch   # Deletar remoto

# Commit
git add .
git commit -m "feat: adiciona feature X"
git push origin feature/nova-feature

# Atualizar
git pull origin main
git fetch --all

# Stash
git stash                        # Guardar mudanças
git stash pop                    # Recuperar mudanças
git stash list                   # Listar stashes

# Log
git log --oneline --graph
git log --author="Nome"
```

---

## ☁️ Azure CLI

### Login & Config

```bash
# Login
az login
az account list
az account set --subscription "Nome"

# Ver recursos
az group list
az resource list --resource-group fiscal-rg
```

### App Service

```bash
# Listar apps
az webapp list --output table

# Ver config
az webapp config appsettings list \
  --name fiscal-app \
  --resource-group fiscal-rg

# Logs
az webapp log tail \
  --name fiscal-app \
  --resource-group fiscal-rg

# SSH
az webapp ssh \
  --name fiscal-app \
  --resource-group fiscal-rg

# Restart
az webapp restart \
  --name fiscal-app \
  --resource-group fiscal-rg
```

### Cosmos DB

```bash
# Listar databases
az cosmosdb sql database list \
  --account-name fiscal-cosmosdb \
  --resource-group fiscal-rg

# Ver connection string
az cosmosdb keys list \
  --name fiscal-cosmosdb \
  --resource-group fiscal-rg \
  --type connection-strings
```

---

## 🔐 Segurança

```bash
# Gerar SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Verificar vulnerabilidades
safety check
safety check --file requirements.txt

# Bandit (security linter)
bandit -r core/ api/
```

---

## 📦 Pip & Dependências

```bash
# Instalar
pip install -r requirements.txt
pip install -r requirements_dev.txt
pip install package_name

# Atualizar
pip install --upgrade package_name
pip list --outdated

# Freeze
pip freeze > requirements.txt

# Verificar
pip check
pip list
```

---

## 🔄 Comandos de Manutenção

```bash
# Limpar cache Python
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Limpar coverage
rm -rf htmlcov/ .coverage .pytest_cache/

# Resetar database (CUIDADO!)
python manage.py flush
python manage.py migrate --fake-initial

# Rebuild completo
make clean
rm -rf venv/
python -m venv venv
# Ativar venv
pip install -r requirements.txt
python scripts/init_project.py
```

---

## 🐛 Debug

```bash
# Ver settings
python manage.py diffsettings

# Shell com auto-reload
python manage.py shell_plus --print-sql

# Ver queries SQL
python manage.py debugsqlshell

# Ver URLs
python manage.py show_urls

# Verificar migrations pendentes
python manage.py showmigrations | grep "\[ \]"
```

---

## 📈 Performance

```bash
# Profile SQL queries
python manage.py sqlprofile

# Ver performance
python -m cProfile manage.py runserver

# Django Debug Toolbar
# Adicionar django-debug-toolbar e acessar /__debug__/
```

---

## 🔍 Troubleshooting

```bash
# Verificar instalação
python --version
pip --version
django-admin --version
python -c "import django; print(django.get_version())"

# Verificar imports
python -c "import core"
python -c "import api"

# Ver variáveis de ambiente
python -c "import os; print(os.getenv('DJANGO_DEBUG'))"

# Testar conexão DB
python manage.py dbshell
```

---

## 📝 Aliases Úteis (Bash/Zsh)

Adicione ao seu `.bashrc` ou `.zshrc`:

```bash
alias pm="python manage.py"
alias pms="python manage.py runserver"
alias pmt="python manage.py test"
alias pmm="python manage.py migrate"
alias pmmm="python manage.py makemigrations"
alias pmc="python manage.py collectstatic --noinput"
alias pms="python manage.py shell"

alias dk="docker-compose"
alias dku="docker-compose up -d"
alias dkd="docker-compose down"
alias dkl="docker-compose logs -f"

alias gst="git status"
alias gco="git checkout"
alias gcb="git checkout -b"
alias gp="git push"
alias gl="git pull"
```

---

## 🎯 Workflows Comuns

### Adicionar Nova Feature

```bash
git checkout -b feature/minha-feature
# Desenvolver...
python manage.py test
make format
make lint
git add .
git commit -m "feat: adiciona minha feature"
git push origin feature/minha-feature
# Abrir PR no GitHub
```

### Atualizar Produção

```bash
git checkout main
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
# Restart server
```

### Debug de Erro

```bash
# 1. Ver logs
python manage.py runserver --verbosity 3

# 2. Shell interativo
python manage.py shell

# 3. Ver SQL
python manage.py sqlprofile

# 4. Verificar configuração
python manage.py check --deploy
```

---

## 📚 Mais Informações

- [Makefile](../Makefile) - Todos os comandos make
- [README.md](../README.md) - Documentação principal
- [QUICKSTART.md](../QUICKSTART.md) - Guia rápido

---

**Salve este arquivo para referência rápida! 📌**
