# Arquitetura do Sistema Fiscal

## Visão Geral

Sistema web para gestão de documentos fiscais eletrônicos (NFe e CTe) com interface responsiva mobile-first e API REST para integração com aplicações mobile.

## Stack Tecnológica

### Backend
- **Framework:** Django 4.2
- **API:** Django REST Framework 3.15
- **Banco de Dados:** 
  - Desenvolvimento: MySQL 8.0
  - Produção: Azure Cosmos DB (recomendado)
- **Autenticação:** JWT (JSON Web Tokens)
- **WSGI Server:** Gunicorn

### Frontend
- **Templates:** Django Templates
- **CSS Framework:** Bootstrap 5
- **JavaScript:** Vanilla JS + Fetch API
- **PWA:** Service Worker + Manifest

### Infraestrutura
- **Containerização:** Docker
- **Cloud:** Azure / Google Cloud
- **CI/CD:** GitHub Actions / Azure DevOps
- **Monitoramento:** Azure Monitor / Sentry

## Arquitetura de Componentes

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Web Browser │  │  Mobile App  │  │  PWA         │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                  │              │
└─────────┼─────────────────┼──────────────────┼──────────────┘
          │                 │                  │
          └─────────────────┼──────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────┐
│                    Application Layer                         │
│                          │                                   │
│  ┌───────────────────────┴───────────────────────┐          │
│  │         Django Application Server             │          │
│  │                                                │          │
│  │  ┌─────────────┐       ┌─────────────┐       │          │
│  │  │  Web Views  │       │  REST API   │       │          │
│  │  │  (core)     │       │  (api)      │       │          │
│  │  └─────────────┘       └─────────────┘       │          │
│  │                                                │          │
│  │  ┌──────────────────────────────────┐        │          │
│  │  │      Business Logic Layer        │        │          │
│  │  │  - Models (NFe, CTe)             │        │          │
│  │  │  - Services (SEFAZ)              │        │          │
│  │  │  - Validators                    │        │          │
│  │  └──────────────────────────────────┘        │          │
│  └────────────────────────────────────────────────┘          │
│                                                               │
└───────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────┐
│                    Data Layer                                │
│                          │                                   │
│  ┌───────────────────────┴───────────────────────┐          │
│  │                                                │          │
│  │  ┌─────────────┐       ┌─────────────┐       │          │
│  │  │   MySQL     │       │  Cosmos DB  │       │          │
│  │  │   (Dev)     │       │  (Prod)     │       │          │
│  │  └─────────────┘       └─────────────┘       │          │
│  │                                                │          │
│  │  ┌─────────────┐       ┌─────────────┐       │          │
│  │  │   Redis     │       │  Azure Blob │       │          │
│  │  │   (Cache)   │       │  (Storage)  │       │          │
│  │  └─────────────┘       └─────────────┘       │          │
│  └────────────────────────────────────────────────┘          │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

## Módulos Principais

### 1. Core (core/)
Módulo principal de negócio

**Responsabilidades:**
- Models de dados (NFe, CTe, Certificado)
- Views web (Dashboard, Listas, Formulários)
- Integração com SEFAZ
- Processamento de XMLs
- Autenticação e autorização

**Arquivos principais:**
```
core/
├── models.py              # Modelos de dados
├── models_certificado.py  # Certificados digitais
├── views.py               # Views web
├── views_certificado.py   # Views de certificados
├── sefaz_service.py       # Integração SEFAZ
├── admin.py               # Admin do Django
└── urls.py                # Rotas web
```

### 2. API (api/)
API REST para integração mobile

**Responsabilidades:**
- Endpoints REST
- Serialização de dados
- Autenticação JWT
- Versionamento de API

**Arquivos principais:**
```
api/
├── views.py         # ViewSets da API
├── serializers.py   # Serializadores
└── urls.py          # Rotas da API
```

### 3. XML Manager (xml_manager/)
Configurações do projeto Django

**Responsabilidades:**
- Settings de ambiente
- Configuração de middlewares
- Roteamento global
- WSGI configuration

**Arquivos principais:**
```
xml_manager/
├── settings.py            # Configurações gerais
├── settings_production.py # Configurações de produção
├── urls.py                # Roteamento principal
└── wsgi.py                # WSGI app
```

## Fluxo de Dados

### 1. Importação de NFe/CTe

```
┌─────────┐     ┌──────────┐     ┌───────────┐     ┌──────────┐
│ Upload  │────▶│ Validação│────▶│  Parser   │────▶│   Save   │
│  XML    │     │  Schema  │     │   XML     │     │    DB    │
└─────────┘     └──────────┘     └───────────┘     └──────────┘
                                       │
                                       ▼
                                 ┌──────────┐
                                 │   SEFAZ  │
                                 │  Consult │
                                 └──────────┘
```

### 2. Consulta SEFAZ

```
┌─────────┐     ┌──────────┐     ┌───────────┐     ┌──────────┐
│  User   │────▶│  Request │────▶│   SEFAZ   │────▶│ Response │
│ Request │     │  + Cert  │     │   WS/API  │     │   + Log  │
└─────────┘     └──────────┘     └───────────┘     └──────────┘
```

### 3. API Mobile

```
┌─────────┐     ┌──────────┐     ┌───────────┐     ┌──────────┐
│  Mobile │────▶│   JWT    │────▶│    API    │────▶│   JSON   │
│   App   │     │   Auth   │     │  Endpoint │     │ Response │
└─────────┘     └──────────┘     └───────────┘     └──────────┘
```

## Modelo de Dados

### Entidades Principais

```
┌─────────────┐       ┌─────────────┐
│     NFe     │       │     CTe     │
├─────────────┤       ├─────────────┤
│ id          │       │ id          │
│ chave_acesso│       │ chave_acesso│
│ numero_nf   │       │ numero_cte  │
│ emit_*      │       │ emit_*      │
│ dest_*      │       │ remetente_* │
│ valor_*     │       │ destinatario│
└──────┬──────┘       └─────────────┘
       │
       │ 1:N
       ▼
┌─────────────┐
│   NFeItem   │
├─────────────┤
│ id          │
│ nfe_id      │
│ numero_item │
│ descricao   │
│ quantidade  │
│ valor_*     │
└─────────────┘

┌──────────────┐      ┌─────────────┐
│ Certificado  │      │  ImportLog  │
├──────────────┤      ├─────────────┤
│ id           │      │ id          │
│ nome         │      │ data        │
│ arquivo_pfx  │      │ usuario     │
│ senha        │      │ status      │
│ validade     │      │ quantidade  │
└──────────────┘      └─────────────┘
```

## Padrões de Design

### 1. Repository Pattern (com Cosmos DB)
```python
class NFeRepository:
    def __init__(self):
        self.container = CosmosDBClient.get_nfes_container()
    
    def find_by_chave(self, chave):
        # Query implementation
        pass
    
    def create(self, nfe_data):
        # Create implementation
        pass
```

### 2. Service Layer
```python
class SefazService:
    def consultar_situacao(self, chave_acesso):
        # Business logic
        pass
    
    def enviar_evento(self, nfe, evento):
        # Business logic
        pass
```

### 3. Serializer Pattern (API)
```python
class NFeSerializer(serializers.ModelSerializer):
    itens = NFeItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = NFe
        fields = '__all__'
```

## Segurança

### Camadas de Segurança

1. **Autenticação**
   - Web: Django Session Authentication
   - API: JWT (JSON Web Tokens)
   - Admin: Django Admin Authentication

2. **Autorização**
   - Permissions por usuário
   - Multi-tenancy (isolamento por empresa)
   - RBAC (Role-Based Access Control)

3. **Proteções**
   - CSRF Protection
   - XSS Prevention
   - SQL Injection Prevention (ORM)
   - HTTPS Obrigatório (produção)
   - Rate Limiting (API)

4. **Certificados**
   - Armazenamento criptografado
   - Senha protegida
   - Validação de validade

## Escalabilidade

### Horizontal Scaling

```
┌────────────────────────────────────────────┐
│           Load Balancer (Azure)            │
└───────┬────────────┬────────────┬──────────┘
        │            │            │
   ┌────▼───┐   ┌────▼───┐   ┌────▼───┐
   │ App 1  │   │ App 2  │   │ App N  │
   │ (Pod)  │   │ (Pod)  │   │ (Pod)  │
   └────┬───┘   └────┬───┘   └────┬───┘
        │            │            │
        └────────────┼────────────┘
                     │
              ┌──────▼─────┐
              │ Cosmos DB  │
              │ (Multi-AZ) │
              └────────────┘
```

### Estratégias

1. **Stateless Applications**
   - Sessões em Redis/Cosmos DB
   - Sem estado local no app

2. **Database Sharding**
   - Particionamento por tenant
   - Hierarchical Partition Keys

3. **Caching**
   - Redis para queries frequentes
   - CDN para assets estáticos

4. **Background Jobs**
   - Celery para processamento assíncrono
   - Azure Functions para triggers

## Monitoramento

### Métricas

- **Application:**
  - Request/Response times
  - Error rates
  - API usage

- **Database:**
  - Query performance
  - RU consumption (Cosmos DB)
  - Connection pool

- **Infrastructure:**
  - CPU/Memory usage
  - Network I/O
  - Disk I/O

### Tools

- Azure Monitor
- Application Insights
- Log Analytics
- Sentry (Error Tracking)

## Deployment

### Ambientes

1. **Development**
   - Docker Compose local
   - SQLite/MySQL
   - Debug ON

2. **Staging**
   - Azure App Service
   - Cosmos DB (dev tier)
   - Debug OFF

3. **Production**
   - Azure Kubernetes Service (AKS)
   - Cosmos DB (prod tier)
   - Multi-region replication
   - Auto-scaling

### CI/CD Pipeline

```
┌──────────┐     ┌─────────┐     ┌──────────┐     ┌────────┐
│   Git    │────▶│  Build  │────▶│   Test   │────▶│ Deploy │
│  Commit  │     │  Docker │     │   Run    │     │  Azure │
└──────────┘     └─────────┘     └──────────┘     └────────┘
```

## Performance

### Otimizações

1. **Database:**
   - Indexes estratégicos
   - Query optimization
   - Connection pooling

2. **Caching:**
   - Template caching
   - Query result caching
   - Static files CDN

3. **Frontend:**
   - Minification (CSS/JS)
   - Lazy loading
   - Service Worker (PWA)

4. **API:**
   - Pagination
   - Field selection
   - Compression (gzip)

---

## Referências

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Azure Cosmos DB Best Practices](https://learn.microsoft.com/azure/cosmos-db/best-practices)
- [Azure Well-Architected Framework](https://learn.microsoft.com/azure/well-architected/)
