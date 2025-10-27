# 🍃 MongoDB - Guia de Configuração e Uso

## 📋 Sobre o Banco de Dados

Este projeto utiliza **MongoDB** como banco de dados principal, oferecendo:

- ✅ Flexibilidade de schema para documentos fiscais
- ✅ Alto desempenho em operações de leitura/escrita
- ✅ Escalabilidade horizontal
- ✅ Compatibilidade com Django através do Djongo

---

## 🚀 Instalação Local

### Opção 1: MongoDB Community (Recomendado para Dev)

#### Windows

```powershell
# Download do instalador
# https://www.mongodb.com/try/download/community

# Ou via Chocolatey
choco install mongodb

# Iniciar serviço
net start MongoDB
```

#### Linux (Ubuntu/Debian)

```bash
# Importar chave pública
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

# Adicionar repositório
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Instalar
sudo apt-get update
sudo apt-get install -y mongodb-org

# Iniciar
sudo systemctl start mongod
sudo systemctl enable mongod
```

#### macOS

```bash
# Via Homebrew
brew tap mongodb/brew
brew install mongodb-community@7.0

# Iniciar
brew services start mongodb-community@7.0
```

### Opção 2: Docker (Mais Fácil!)

```bash
# Rodar MongoDB no Docker
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=admin123 \
  -e MONGO_INITDB_DATABASE=aviladevops_fiscal \
  -v mongodb_data:/data/db \
  mongo:7

# Ou use o docker-compose.yml do projeto
docker-compose up -d mongodb
```

### Opção 3: MongoDB Atlas (Cloud - Gratuito)

1. Acesse [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Crie uma conta gratuita
3. Crie um cluster (tier gratuito: 512MB)
4. Configure acesso de rede (Allow Access from Anywhere para dev)
5. Crie um usuário de banco de dados
6. Obtenha a connection string

---

## ⚙️ Configuração do Django

### Djongo - Django + MongoDB

O projeto usa **Djongo** para integrar Django com MongoDB:

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'aviladevops_fiscal',
        'CLIENT': {
            'host': 'mongodb://localhost:27017/',
            # Ou para Atlas:
            # 'host': 'mongodb+srv://user:pass@cluster.mongodb.net/dbname'
        }
    }
}
```

### Variáveis de Ambiente

Configure no `.env`:

```env
# MongoDB Local
USE_MONGODB=true
MONGODB_DATABASE=aviladevops_fiscal
MONGODB_CONNECTION_STRING=mongodb://localhost:27017/aviladevops_fiscal

# MongoDB com autenticação
MONGODB_CONNECTION_STRING=mongodb://admin:admin123@localhost:27017/aviladevops_fiscal?authSource=admin

# MongoDB Atlas (Cloud)
MONGODB_CONNECTION_STRING=mongodb+srv://username:password@cluster0.mongodb.net/aviladevops_fiscal?retryWrites=true&w=majority
```

---

## 🗄️ Estrutura de Dados

### Collections Principais

```javascript
// nfes - Notas Fiscais Eletrônicas
{
  _id: ObjectId("..."),
  chave_acesso: "12345678901234567890123456789012345678901234",
  numero_nf: "123",
  serie: "1",
  data_emissao: ISODate("2025-10-27T10:30:00Z"),
  emitente: {
    cnpj: "12345678000190",
    nome: "Empresa XYZ Ltda",
    fantasia: "XYZ",
    endereco: "Rua Teste, 123",
    municipio: "São Paulo",
    uf: "SP"
  },
  destinatario: {
    cnpj_cpf: "98765432000100",
    nome: "Cliente ABC",
    endereco: "Av. Principal, 456",
    municipio: "Rio de Janeiro",
    uf: "RJ"
  },
  itens: [
    {
      numero_item: 1,
      codigo_produto: "PROD001",
      descricao: "Produto Teste",
      quantidade: 10.0,
      valor_unitario: 100.00,
      valor_total: 1000.00,
      ncm: "12345678",
      cfop: "5102"
    }
  ],
  totais: {
    valor_total: 1000.00,
    valor_produtos: 900.00,
    valor_icms: 100.00,
    valor_ipi: 0.00
  },
  status: "Autorizada",
  xml_content: "<?xml version...",
  usuario_importacao: "admin",
  data_importacao: ISODate("2025-10-27T11:00:00Z")
}

// ctes - Conhecimentos de Transporte Eletrônicos
{
  _id: ObjectId("..."),
  chave_acesso: "...",
  numero_cte: "456",
  // ... estrutura similar
}

// users - Usuários (Django auth)
{
  _id: ObjectId("..."),
  username: "admin",
  email: "admin@fiscal.com",
  // ... campos Django User
}
```

---

## 🔍 Operações Comuns

### MongoDB Shell (mongosh)

```bash
# Conectar
mongosh mongodb://localhost:27017/aviladevops_fiscal

# Ou com autenticação
mongosh "mongodb://admin:admin123@localhost:27017/aviladevops_fiscal?authSource=admin"
```

### Comandos Úteis

```javascript
// Ver databases
show dbs

// Usar database
use aviladevops_fiscal

// Ver collections
show collections

// Contar documentos
db.nfes.countDocuments()

// Buscar NFes
db.nfes.find({ "emitente.cnpj": "12345678000190" })

// Buscar com limite
db.nfes.find().limit(10)

// Buscar por data
db.nfes.find({
  data_emissao: {
    $gte: ISODate("2025-10-01"),
    $lt: ISODate("2025-11-01")
  }
})

// Agregar valores
db.nfes.aggregate([
  {
    $group: {
      _id: "$emitente.cnpj",
      total: { $sum: "$totais.valor_total" },
      quantidade: { $sum: 1 }
    }
  }
])

// Criar índices
db.nfes.createIndex({ "chave_acesso": 1 }, { unique: true })
db.nfes.createIndex({ "data_emissao": -1 })
db.nfes.createIndex({ "emitente.cnpj": 1 })

// Ver índices
db.nfes.getIndexes()

// Estatísticas da collection
db.nfes.stats()

// Drop collection (CUIDADO!)
db.nfes.drop()
```

---

## 🔐 Segurança

### Criar Usuário Administrativo

```javascript
// Conectar como admin
mongosh

use admin

// Criar admin
db.createUser({
  user: "admin",
  pwd: "senha-segura-aqui",
  roles: [
    { role: "userAdminAnyDatabase", db: "admin" },
    { role: "readWriteAnyDatabase", db: "admin" }
  ]
})

// Criar usuário específico da aplicação
use aviladevops_fiscal

db.createUser({
  user: "fiscal_app",
  pwd: "senha-app",
  roles: [
    { role: "readWrite", db: "aviladevops_fiscal" }
  ]
})
```

### Habilitar Autenticação

```yaml
# /etc/mongod.conf
security:
  authorization: enabled
```

---

## 📊 Índices Recomendados

```javascript
// NFes
db.nfes.createIndex({ "chave_acesso": 1 }, { unique: true })
db.nfes.createIndex({ "data_emissao": -1 })
db.nfes.createIndex({ "emitente.cnpj": 1, "data_emissao": -1 })
db.nfes.createIndex({ "destinatario.cnpj_cpf": 1 })
db.nfes.createIndex({ "numero_nf": 1, "serie": 1 })

// CTes
db.ctes.createIndex({ "chave_acesso": 1 }, { unique: true })
db.ctes.createIndex({ "data_emissao": -1 })
db.ctes.createIndex({ "emit_cnpj": 1, "data_emissao": -1 })

// Full-text search (opcional)
db.nfes.createIndex({
  "emitente.nome": "text",
  "destinatario.nome": "text",
  "itens.descricao": "text"
})
```

---

## 🚀 Performance

### Dicas de Otimização

1. **Use Índices Adequados**
   - Crie índices para campos frequentemente consultados
   - Use compound indexes para queries com múltiplos filtros

2. **Projections**
   ```javascript
   // Buscar apenas campos necessários
   db.nfes.find(
     { "emitente.cnpj": "12345678000190" },
     { numero_nf: 1, data_emissao: 1, "totais.valor_total": 1 }
   )
   ```

3. **Limit e Skip**
   ```javascript
   // Paginação eficiente
   db.nfes.find().sort({ data_emissao: -1 }).limit(20).skip(0)
   ```

4. **Aggregation Pipeline**
   ```javascript
   // Use aggregation para consultas complexas
   db.nfes.aggregate([
     { $match: { "emitente.uf": "SP" } },
     { $group: { _id: "$emitente.municipio", total: { $sum: "$totais.valor_total" } } },
     { $sort: { total: -1 } },
     { $limit: 10 }
   ])
   ```

---

## 🔄 Backup e Restore

### Backup

```bash
# Backup completo
mongodump --uri="mongodb://localhost:27017/aviladevops_fiscal" --out=/backup/$(date +%Y%m%d)

# Backup específico de collection
mongodump --uri="mongodb://localhost:27017/aviladevops_fiscal" --collection=nfes --out=/backup/nfes

# Com autenticação
mongodump --uri="mongodb://admin:pass@localhost:27017/aviladevops_fiscal?authSource=admin" --out=/backup
```

### Restore

```bash
# Restore completo
mongorestore --uri="mongodb://localhost:27017" /backup/20251027

# Restore específico
mongorestore --uri="mongodb://localhost:27017/aviladevops_fiscal" --collection=nfes /backup/nfes/nfes.bson
```

---

## 🌐 MongoDB Atlas (Cloud)

### Vantagens

- ✅ **Free tier:** 512MB gratuitos
- ✅ **Gerenciado:** Sem necessidade de manutenção
- ✅ **Backups automáticos**
- ✅ **Escalabilidade fácil**
- ✅ **Monitoramento integrado**
- ✅ **Replicação global**

### Configuração

1. **Criar Cluster**
   - Acesse [MongoDB Atlas](https://cloud.mongodb.com)
   - Crie um cluster (M0 - Free)
   - Escolha região (Brazil/São Paulo disponível)

2. **Configurar Acesso**
   ```
   Network Access → Add IP Address → Allow Access from Anywhere (0.0.0.0/0)
   ```

3. **Criar Usuário**
   ```
   Database Access → Add New Database User
   Username: fiscal_app
   Password: (gere uma senha segura)
   Role: Atlas Admin ou Read/Write
   ```

4. **Obter Connection String**
   ```
   Clusters → Connect → Connect your application
   mongodb+srv://fiscal_app:password@cluster0.xxxxx.mongodb.net/aviladevops_fiscal?retryWrites=true&w=majority
   ```

5. **Configurar no .env**
   ```env
   MONGODB_CONNECTION_STRING=mongodb+srv://fiscal_app:password@cluster0.xxxxx.mongodb.net/aviladevops_fiscal?retryWrites=true&w=majority
   ```

---

## 🔧 Troubleshooting

### Erro: "Connection refused"

```bash
# Verificar se MongoDB está rodando
sudo systemctl status mongod  # Linux
net start MongoDB  # Windows
brew services list  # macOS

# Iniciar se parado
sudo systemctl start mongod
```

### Erro: "Authentication failed"

```bash
# Verificar credenciais
mongosh "mongodb://username:password@localhost:27017/dbname?authSource=admin"

# Ou resetar senha
mongosh
use admin
db.changeUserPassword("username", "nova-senha")
```

### Erro: "Database connection timeout"

- Verificar firewall
- Verificar IP whitelisting (Atlas)
- Verificar connection string

### Django: "No module named 'djongo'"

```bash
pip install djongo pymongo dnspython
```

---

## 📚 Recursos Adicionais

- [MongoDB Documentation](https://docs.mongodb.com/)
- [Djongo Documentation](https://www.djongomapper.com/)
- [MongoDB University](https://university.mongodb.com/) - Cursos gratuitos
- [MongoDB Compass](https://www.mongodb.com/products/compass) - GUI para MongoDB

---

## 💡 Migração de MySQL para MongoDB

Se você tiver dados em MySQL e quiser migrar:

```python
# Script de migração (exemplo)
from core.models import NFe as MySQLNFe
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['aviladevops_fiscal']

for nfe in MySQLNFe.objects.all():
    doc = {
        'chave_acesso': nfe.chave_acesso,
        'numero_nf': nfe.numero_nf,
        # ... mapear campos
    }
    db.nfes.insert_one(doc)
```

---

**MongoDB configurado e pronto para uso! 🚀**
