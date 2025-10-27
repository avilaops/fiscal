# 📊 Sistema de Gestão de XMLs Fiscais

Sistema web mobile-first para gestão e consulta de documentos fiscais eletrônicos (NFe e CTe) com integração SEFAZ.

## 🚀 Funcionalidades

- ✅ Importação e processamento de XMLs fiscais (NFe e CTe)
- ✅ Dashboard com estatísticas e gráficos
- ✅ Consulta e filtros avançados
- ✅ API REST para integração mobile
- ✅ Interface responsiva mobile-first
- ✅ Gestão de certificados digitais
- ✅ Integração com SEFAZ

## 🛠️ Tecnologias

- **Backend:** Django 4.2 + Django REST Framework
- **Banco de Dados:** MongoDB (Primary) / Azure Cosmos DB (Produção recomendada)
- **Frontend:** HTML5, CSS3, JavaScript (Bootstrap)
- **Containerização:** Docker
- **Deploy:** Google Cloud Run / Azure App Service

## 📋 Pré-requisitos

- Python 3.11+
- MongoDB 7.0+ (desenvolvimento local) ou MongoDB Atlas
- Docker (opcional, para containerização)

## 🔧 Instalação Local

### 1. Clone o repositório

```bash
git clone <repository-url>
cd web_app
```

### 2. Crie e ative um ambiente virtual

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo `.env.example` para `.env` e configure:

```bash
cp .env.example .env
```

Edite o arquivo `.env`:

```env
# Django
DJANGO_SECRET_KEY=sua-chave-secreta-aqui
DJANGO_DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# MongoDB
USE_MONGODB=true
MONGODB_DATABASE=aviladevops_fiscal
MONGODB_CONNECTION_STRING=mongodb://localhost:27017/aviladevops_fiscal
# Ou para MongoDB Atlas:
# MONGODB_CONNECTION_STRING=mongodb+srv://user:pass@cluster.mongodb.net/aviladevops_fiscal?retryWrites=true&w=majority

# CSRF (em produção, adicione seu domínio)
CSRF_TRUSTED_ORIGINS=http://localhost:8000
```

### 5. Execute as migrações

```bash
python manage.py migrate
```

### 6. Crie um superusuário

```bash
python manage.py createsuperuser
```

### 7. Colete arquivos estáticos

```bash
python manage.py collectstatic --noinput
```

### 8. Execute o servidor de desenvolvimento

```bash
python manage.py runserver
```

Acesse: http://localhost:8000

## 🐳 Instalação com Docker

### 1. Build da imagem

```bash
docker build -t fiscal-web-app .
```

### 2. Execute o container

```bash
docker run -p 8080:8080 --env-file .env fiscal-web-app
```

### 3. Usando Docker Compose (recomendado)

```bash
docker-compose up -d
```

## 📁 Estrutura do Projeto

```
web_app/
├── api/                    # API REST (Django REST Framework)
│   ├── serializers.py      # Serializadores
│   ├── views.py            # Views da API
│   └── urls.py             # Rotas da API
├── core/                   # Aplicação principal
│   ├── models.py           # Modelos de dados (NFe, CTe, etc.)
│   ├── models_certificado.py  # Modelos de certificados
│   ├── views.py            # Views web
│   ├── views_certificado.py   # Views de certificados
│   ├── sefaz_service.py    # Serviço de integração SEFAZ
│   └── admin.py            # Configuração do admin
├── templates/              # Templates HTML
│   ├── base.html
│   └── core/
│       ├── login.html
│       ├── dashboard.html
│       └── partials/
├── static/                 # Arquivos estáticos (CSS, JS, imagens)
├── xml_manager/            # Configurações do projeto
│   ├── settings.py         # Configurações gerais
│   ├── settings_production.py  # Configurações de produção
│   ├── urls.py             # Rotas principais
│   └── wsgi.py             # WSGI application
├── tests/                  # Testes automatizados
├── docs/                   # Documentação adicional
├── scripts/                # Scripts utilitários
├── manage.py               # CLI do Django
├── requirements.txt        # Dependências Python
├── Dockerfile              # Configuração Docker
├── docker-compose.yml      # Docker Compose
└── README.md               # Este arquivo
```

## 🔐 Segurança

- ✅ Variáveis sensíveis em `.env` (nunca commite!)
- ✅ SECRET_KEY único por ambiente
- ✅ DEBUG=False em produção
- ✅ ALLOWED_HOSTS configurado corretamente
- ✅ CSRF_TRUSTED_ORIGINS definido
- ✅ HTTPS obrigatório em produção

## 📡 API REST

### Endpoints Disponíveis

#### Autenticação
- `POST /api/token/` - Obter token JWT
- `POST /api/token/refresh/` - Renovar token

#### NFe
- `GET /api/nfe/` - Listar NFes
- `GET /api/nfe/{id}/` - Detalhes de NFe
- `GET /api/nfe/search/?q=termo` - Buscar NFe
- `GET /api/nfe/by_emitente/?cnpj=123` - Filtrar por emitente

#### CTe
- `GET /api/cte/` - Listar CTes
- `GET /api/cte/{id}/` - Detalhes de CTe

#### Dashboard
- `GET /api/dashboard/` - Estatísticas gerais
- `GET /api/statistics/` - Estatísticas detalhadas

### Exemplo de Uso

```bash
# Obter token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"senha123"}'

# Listar NFes (com token)
curl -X GET http://localhost:8000/api/nfe/ \
  -H "Authorization: Bearer seu-token-aqui"
```

## 🧪 Testes

Execute os testes:

```bash
# Todos os testes
python manage.py test

# Testes específicos
python manage.py test core.tests
python manage.py test api.tests

# Com cobertura
coverage run --source='.' manage.py test
coverage report
```

## 🚀 Deploy

### Google Cloud Run

```bash
# Build e push da imagem
gcloud builds submit --tag gcr.io/seu-projeto/fiscal-app

# Deploy
gcloud run deploy fiscal-app \
  --image gcr.io/seu-projeto/fiscal-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure App Service

```bash
# Login no Azure
az login

# Criar App Service
az webapp create --resource-group seu-grupo \
  --plan seu-plano \
  --name fiscal-app \
  --deployment-container-image-name sua-imagem
```

## 🗄️ Migração para Azure Cosmos DB

Para melhor escalabilidade e performance em produção, recomenda-se Azure Cosmos DB:

### Vantagens
- ✅ Distribuição global com baixa latência
- ✅ Escalabilidade elástica automática
- ✅ Isolamento de dados por tenant/usuário
- ✅ Ideal para aplicações multi-tenant
- ✅ Vector Search para busca semântica

### Configuração

1. Instale o SDK do Cosmos DB:
```bash
pip install azure-cosmos
```

2. Configure as variáveis de ambiente:
```env
COSMOS_ENDPOINT=https://sua-conta.documents.azure.com:443/
COSMOS_KEY=sua-chave-aqui
COSMOS_DATABASE=fiscal_db
```

3. Consulte `docs/COSMOS_DB_MIGRATION.md` para guia completo

## 📚 Documentação Adicional

- [Guia de Contribuição](docs/CONTRIBUTING.md)
- [Arquitetura do Sistema](docs/ARCHITECTURE.md)
- [API Documentation](docs/API.md)
- [Migração Cosmos DB](docs/COSMOS_DB_MIGRATION.md)

## 🐛 Troubleshooting

### Erro de conexão com banco de dados
- Verifique se o MySQL está rodando
- Confirme credenciais no `.env`
- Teste conexão: `python manage.py dbshell`

### Erro de certificado SSL
- Verifique formato do certificado (.pfx)
- Confirme senha do certificado
- Veja logs em: `logs/certificado.log`

### Problemas com imports
- Verifique estrutura do XML
- Consulte logs de importação
- Use `python manage.py import_xml --debug`

## 📝 Licença

Este projeto é proprietário. Todos os direitos reservados.

## 👥 Autores

- Avila DevOps - [aviladevops.com.br](https://aviladevops.com.br)

## 📞 Suporte

Para suporte, abra uma issue ou entre em contato pelo email: suporte@aviladevops.com.br

---

**Versão:** 1.0.0
**Última atualização:** Outubro 2025
