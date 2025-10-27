# Makefile para Sistema Fiscal

.PHONY: help install install-dev run test coverage lint format check migrate makemigrations superuser clean docker-build docker-up docker-down

# Variáveis
PYTHON = python
PIP = pip
MANAGE = $(PYTHON) manage.py

help:
	@echo "╔════════════════════════════════════════════════════════════╗"
	@echo "║           Sistema Fiscal - Comandos Disponíveis            ║"
	@echo "╚════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "  make install          - Instalar dependências de produção"
	@echo "  make install-dev      - Instalar dependências de desenvolvimento"
	@echo "  make run              - Executar servidor de desenvolvimento"
	@echo "  make test             - Executar testes"
	@echo "  make coverage         - Executar testes com cobertura"
	@echo "  make lint             - Verificar código (flake8)"
	@echo "  make format           - Formatar código (black + isort)"
	@echo "  make check            - Verificar qualidade de código"
	@echo "  make migrate          - Executar migrations"
	@echo "  make makemigrations   - Criar migrations"
	@echo "  make superuser        - Criar superusuário"
	@echo "  make clean            - Limpar arquivos temporários"
	@echo "  make docker-build     - Build Docker image"
	@echo "  make docker-up        - Iniciar containers"
	@echo "  make docker-down      - Parar containers"
	@echo ""

install:
	@echo "▶ Instalando dependências..."
	$(PIP) install -r requirements.txt

install-dev:
	@echo "▶ Instalando dependências de desenvolvimento..."
	$(PIP) install -r requirements_dev.txt

run:
	@echo "▶ Iniciando servidor de desenvolvimento..."
	$(MANAGE) runserver

test:
	@echo "▶ Executando testes..."
	$(MANAGE) test

coverage:
	@echo "▶ Executando testes com cobertura..."
	coverage run --source='.' $(MANAGE) test
	coverage report
	coverage html
	@echo "✓ Relatório HTML gerado em: htmlcov/index.html"

lint:
	@echo "▶ Verificando código com flake8..."
	flake8 .

format:
	@echo "▶ Formatando código..."
	black .
	isort .
	@echo "✓ Código formatado"

check:
	@echo "▶ Verificando qualidade de código..."
	$(PYTHON) scripts/check_quality.py

migrate:
	@echo "▶ Executando migrations..."
	$(MANAGE) migrate

makemigrations:
	@echo "▶ Criando migrations..."
	$(MANAGE) makemigrations

superuser:
	@echo "▶ Criando superusuário..."
	$(PYTHON) scripts/create_superuser.py

collectstatic:
	@echo "▶ Coletando arquivos estáticos..."
	$(MANAGE) collectstatic --noinput

init:
	@echo "▶ Inicializando projeto..."
	$(PYTHON) scripts/init_project.py

clean:
	@echo "▶ Limpando arquivos temporários..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage .pytest_cache/
	@echo "✓ Limpeza concluída"

docker-build:
	@echo "▶ Building Docker image..."
	docker build -t fiscal-web-app .

docker-up:
	@echo "▶ Iniciando containers..."
	docker-compose up -d

docker-down:
	@echo "▶ Parando containers..."
	docker-compose down

docker-logs:
	@echo "▶ Visualizando logs..."
	docker-compose logs -f

shell:
	@echo "▶ Abrindo Django shell..."
	$(MANAGE) shell

dbshell:
	@echo "▶ Abrindo database shell..."
	$(MANAGE) dbshell
