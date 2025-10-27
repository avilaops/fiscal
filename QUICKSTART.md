# 🚀 Guia Rápido de Início

Comece a usar o Sistema Fiscal em menos de 5 minutos!

## ⚡ Início Rápido

### Opção 1: Usando Scripts Automatizados (Recomendado)

#### Windows (PowerShell)

```powershell
# 1. Clone o repositório
git clone <repository-url>
cd web_app

# 2. Crie ambiente virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Configure ambiente
copy .env.example .env
# Edite .env com suas configurações

# 4. Instale dependências
pip install -r requirements.txt

# 5. Inicialize o projeto (faz tudo automaticamente!)
python scripts\init_project.py

# 6. Rode o servidor
python manage.py runserver
```

#### Linux/Mac

```bash
# 1. Clone o repositório
git clone <repository-url>
cd web_app

# 2. Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 3. Configure ambiente
cp .env.example .env
# Edite .env com suas configurações

# 4. Instale dependências
pip install -r requirements.txt

# 5. Inicialize o projeto
python scripts/init_project.py

# 6. Rode o servidor
python manage.py runserver
```

Acesse: http://localhost:8000

---

### Opção 2: Usando Docker (Mais Rápido!)

```bash
# 1. Clone o repositório
git clone <repository-url>
cd web_app

# 2. Configure ambiente (opcional)
cp .env.example .env

# 3. Suba os containers
docker-compose up -d

# 4. Execute migrations
docker-compose exec web python manage.py migrate

# 5. Crie superusuário
docker-compose exec web python scripts/create_superuser.py
```

Acesse: http://localhost:8000

---

### Opção 3: Usando Makefile

```bash
# Instalar dependências
make install

# Inicializar projeto
make init

# Rodar servidor
make run
```

---

## 📝 Primeiros Passos

### 1. Login

**URL:** http://localhost:8000/login/

**Credenciais padrão:**
- Usuário: `admin`
- Senha: `admin123`

⚠️ **IMPORTANTE:** Altere a senha após o primeiro login!

### 2. Dashboard

Após login, você será redirecionado para o dashboard:
- Estatísticas de NFes e CTes
- Últimas importações
- Top emitentes

### 3. Importar XMLs

1. Vá para "Importar NFe/CTe"
2. Selecione arquivo(s) XML
3. Clique em "Importar"
4. Aguarde processamento

### 4. Consultar Documentos

- **NFes:** `/nfes/`
- **CTes:** `/ctes/`

Use os filtros para buscar:
- Por período
- Por CNPJ
- Por valor
- Por status

---

## 🔧 Configuração Básica

### Arquivo .env

Configurações mínimas necessárias:

```env
# Django
DJANGO_SECRET_KEY=sua-chave-secreta-aqui
DJANGO_DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# MongoDB
USE_MONGODB=true
MONGODB_DATABASE=aviladevops_fiscal
MONGODB_CONNECTION_STRING=mongodb://localhost:27017/aviladevops_fiscal

# CSRF
CSRF_TRUSTED_ORIGINS=http://localhost:8000
```

### Configurar MongoDB

#### Opção 1: MongoDB Local

```bash
# Windows (via Chocolatey)
choco install mongodb

# Linux (Ubuntu)
sudo apt-get install mongodb-org

# macOS (via Homebrew)
brew install mongodb-community
```

#### Opção 2: MongoDB Atlas (Cloud - Gratuito!)

1. Acesse [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Crie uma conta e cluster gratuito (512MB)
3. Configure Network Access (Allow Access from Anywhere para dev)
4. Crie usuário de database
5. Obtenha connection string
6. Configure no `.env`:

```env
MONGODB_CONNECTION_STRING=mongodb+srv://user:pass@cluster0.mongodb.net/aviladevops_fiscal?retryWrites=true&w=majority
```

#### Opção 3: Docker (Mais Fácil!)

```bash
# MongoDB já incluído no docker-compose.yml
docker-compose up -d mongodb
```

> 📚 **Mais detalhes:** Veja [docs/MONGODB.md](docs/MONGODB.md)

---

## 🔐 Segurança

### Gerar SECRET_KEY

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Criar Novo Superusuário

```bash
python scripts/create_superuser.py
```

Ou interativamente:

```bash
python manage.py createsuperuser
```

---

## 📱 Testar API

### Obter Token JWT

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### Listar NFes

```bash
curl -X GET http://localhost:8000/api/nfe/ \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

---

## 🧪 Executar Testes

```bash
# Todos os testes
python manage.py test

# Com cobertura
make coverage

# Ver relatório
# Windows: start htmlcov\index.html
# Linux/Mac: open htmlcov/index.html
```

---

## 🐛 Troubleshooting

### Erro: "No module named 'django'"

```bash
# Ative o ambiente virtual
# Windows:
.\venv\Scripts\Activate.ps1

# Linux/Mac:
source venv/bin/activate

# Reinstale dependências
pip install -r requirements.txt
```

### Erro: "Access denied for user"

Verifique credenciais do banco no `.env`:
- `DB_USER`
- `DB_PASS`
- `DB_HOST`
- `DB_PORT`

### Erro: "Table doesn't exist"

Execute migrations:

```bash
python manage.py migrate
```

### Porta 8000 em uso

Use outra porta:

```bash
python manage.py runserver 8080
```

---

## 📚 Próximos Passos

1. **Leia a Documentação Completa:** [README.md](README.md)
2. **Entenda a Arquitetura:** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
3. **Explore a API:** [docs/API.md](docs/API.md)
4. **Configure Produção:** [docs/COSMOS_DB_MIGRATION.md](docs/COSMOS_DB_MIGRATION.md)
5. **Contribua:** [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)

---

## 💬 Suporte

Precisa de ajuda?

- 📧 Email: suporte@aviladevops.com.br
- 🐛 Issues: Use GitHub Issues
- 💬 Discussões: Use GitHub Discussions

---

**Pronto! Agora você está rodando o Sistema Fiscal! 🎉**
