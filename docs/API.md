# API Documentation

## Base URL

```
Development: http://localhost:8000/api
Production: https://seu-dominio.com/api
```

## Authentication

A API utiliza autenticação JWT (JSON Web Tokens).

### Obter Token

```http
POST /api/token/
Content-Type: application/json

{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Usar Token

Inclua o token no header `Authorization`:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Renovar Token

```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## Endpoints

### NFe (Notas Fiscais Eletrônicas)

#### Listar NFes

```http
GET /api/nfe/
Authorization: Bearer {token}
```

**Query Parameters:**
- `search` - Buscar por texto (número, emitente, destinatário, chave)
- `cnpj` - Filtrar por CNPJ do emitente
- `ordering` - Ordenar por campo (ex: `-data_emissao`)
- `page` - Número da página (paginação)

**Response:**
```json
[
  {
    "id": 1,
    "chave_acesso": "12345678901234567890123456789012345678901234",
    "numero_nf": "123",
    "serie": "1",
    "data_emissao": "2025-10-27T10:30:00Z",
    "emit_cnpj": "12345678000190",
    "emit_nome": "Empresa XYZ Ltda",
    "dest_cnpj_cpf": "98765432000100",
    "dest_nome": "Cliente ABC",
    "valor_total": "1000.00",
    "status_nfe": "Autorizada"
  }
]
```

#### Detalhes de NFe

```http
GET /api/nfe/{id}/
Authorization: Bearer {token}
```

**Response:**
```json
{
  "id": 1,
  "chave_acesso": "12345678901234567890123456789012345678901234",
  "numero_nf": "123",
  "serie": "1",
  "data_emissao": "2025-10-27T10:30:00Z",
  "emit_cnpj": "12345678000190",
  "emit_nome": "Empresa XYZ Ltda",
  "emit_fantasia": "XYZ",
  "emit_endereco": "Rua Teste, 123",
  "emit_municipio": "São Paulo",
  "emit_uf": "SP",
  "dest_cnpj_cpf": "98765432000100",
  "dest_nome": "Cliente ABC",
  "valor_total": "1000.00",
  "valor_produtos": "900.00",
  "valor_icms": "100.00",
  "status_nfe": "Autorizada",
  "itens": [
    {
      "numero_item": 1,
      "codigo_produto": "PROD001",
      "descricao": "Produto Teste",
      "quantidade": "10.0000",
      "valor_unitario": "90.00",
      "valor_total": "900.00"
    }
  ]
}
```

#### Buscar NFes

```http
GET /api/nfe/search/?q=termo
Authorization: Bearer {token}
```

#### Filtrar por Emitente

```http
GET /api/nfe/by_emitente/?cnpj=12345678000190
Authorization: Bearer {token}
```

---

### CTe (Conhecimentos de Transporte Eletrônicos)

#### Listar CTes

```http
GET /api/cte/
Authorization: Bearer {token}
```

**Query Parameters:**
- `search` - Buscar por texto
- `remetente_cnpj` - Filtrar por CNPJ do remetente
- `ordering` - Ordenar por campo
- `page` - Número da página

**Response:**
```json
[
  {
    "id": 1,
    "chave_acesso": "12345678901234567890123456789012345678901234",
    "numero_cte": "456",
    "serie": "1",
    "data_emissao": "2025-10-27T11:00:00Z",
    "emit_cnpj": "12345678000190",
    "emit_nome": "Transportadora ABC",
    "remetente_nome": "Empresa XYZ",
    "destinatario_nome": "Cliente 123",
    "valor_total": "500.00"
  }
]
```

#### Detalhes de CTe

```http
GET /api/cte/{id}/
Authorization: Bearer {token}
```

---

### Dashboard

#### Estatísticas Gerais

```http
GET /api/dashboard/
Authorization: Bearer {token}
```

**Response:**
```json
{
  "nfe_stats": {
    "total": 1000,
    "mes_atual": 50,
    "valor_total": "1000000.00",
    "valor_mes": "50000.00"
  },
  "cte_stats": {
    "total": 500,
    "mes_atual": 25,
    "valor_total": "500000.00",
    "valor_mes": "25000.00"
  },
  "ultimos_logs": [
    {
      "data_importacao": "2025-10-27T10:00:00Z",
      "usuario": "admin",
      "status": "sucesso",
      "quantidade": 10
    }
  ]
}
```

#### Estatísticas Detalhadas

```http
GET /api/statistics/
Authorization: Bearer {token}
```

**Query Parameters:**
- `periodo` - Período (7, 30, 90 dias ou 'all')
- `tipo` - Tipo de documento ('nfe' ou 'cte')

**Response:**
```json
{
  "totais": {
    "documentos": 100,
    "valor_total": "100000.00",
    "media_valor": "1000.00"
  },
  "por_mes": [
    {
      "mes": "2025-10",
      "quantidade": 50,
      "valor": "50000.00"
    }
  ],
  "top_emitentes": [
    {
      "cnpj": "12345678000190",
      "nome": "Empresa XYZ",
      "quantidade": 25,
      "valor_total": "25000.00"
    }
  ]
}
```

---

## Erros

A API retorna erros em formato JSON padronizado:

```json
{
  "detail": "Mensagem de erro descritiva"
}
```

### Códigos de Status HTTP

- `200 OK` - Sucesso
- `201 Created` - Recurso criado
- `400 Bad Request` - Requisição inválida
- `401 Unauthorized` - Não autenticado
- `403 Forbidden` - Sem permissão
- `404 Not Found` - Recurso não encontrado
- `500 Internal Server Error` - Erro no servidor

---

## Exemplos de Uso

### Python (requests)

```python
import requests

# Obter token
response = requests.post('http://localhost:8000/api/token/', json={
    'username': 'admin',
    'password': 'senha123'
})
token = response.json()['access']

# Listar NFes
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:8000/api/nfe/', headers=headers)
nfes = response.json()
```

### JavaScript (fetch)

```javascript
// Obter token
const response = await fetch('http://localhost:8000/api/token/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'admin', password: 'senha123' })
});
const { access } = await response.json();

// Listar NFes
const nfes = await fetch('http://localhost:8000/api/nfe/', {
  headers: { 'Authorization': `Bearer ${access}` }
}).then(r => r.json());
```

### cURL

```bash
# Obter token
TOKEN=$(curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"senha123"}' \
  | jq -r .access)

# Listar NFes
curl -X GET http://localhost:8000/api/nfe/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## Paginação

Endpoints de listagem retornam resultados paginados:

```json
{
  "count": 100,
  "next": "http://localhost:8000/api/nfe/?page=2",
  "previous": null,
  "results": [...]
}
```

**Query Parameters:**
- `page` - Número da página (padrão: 1)
- `page_size` - Itens por página (padrão: 20, máximo: 100)

---

## Rate Limiting

- **Desenvolvimento:** Sem limites
- **Produção:** 100 requisições por minuto por usuário

---

## Versionamento

A API está na versão **v1**. Mudanças incompatíveis serão introduzidas em novas versões (v2, v3, etc.).
