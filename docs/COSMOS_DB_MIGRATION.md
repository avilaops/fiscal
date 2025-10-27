# Guia de Migração para Azure Cosmos DB

## Por que Azure Cosmos DB?

Azure Cosmos DB é altamente recomendado para este sistema fiscal pelas seguintes razões:

### ✅ Vantagens

1. **Distribuição Global com Baixa Latência**
   - Replicação automática em múltiplas regiões
   - Latência de single-digit milliseconds
   - 99.999% de disponibilidade SLA

2. **Escalabilidade Elástica**
   - Escalonamento automático baseado em carga
   - Sem necessidade de gerenciar infraestrutura
   - Custos otimizados com provisioning automático

3. **Modelo de Dados Flexível**
   - Ideal para documentos fiscais (NFe, CTe) com estrutura variável
   - Suporte nativo a JSON
   - Schema-less para diferentes tipos de documentos

4. **Isolamento Multi-Tenant**
   - Particionamento hierárquico (HPK) para isolar dados por cliente
   - Ideal para aplicações SaaS
   - Supera o limite de 20GB por partition key lógica

5. **Vector Search**
   - Busca semântica de documentos fiscais
   - Recomendações baseadas em contexto
   - Análise inteligente de padrões

6. **Casos de Uso Ideais**
   - ✅ Gestão de documentos fiscais por tenant/empresa
   - ✅ Histórico de transações e auditoria
   - ✅ Busca contextual de NFes/CTes
   - ✅ Dashboard com estatísticas em tempo real

---

## Arquitetura Proposta

### Estrutura de Dados

```
fiscal_db (Database)
├── empresas (Container)
│   └── Partition Key: /tenantId
├── nfes (Container)
│   └── Partition Key: [/tenantId, /ano, /mes]  # Hierarchical Partition Key
├── ctes (Container)
│   └── Partition Key: [/tenantId, /ano, /mes]  # Hierarchical Partition Key
├── usuarios (Container)
│   └── Partition Key: /tenantId
└── logs (Container)
    └── Partition Key: [/tenantId, /data]
```

### Hierarchical Partition Keys (HPK)

Para NFes e CTes, use HPK para:
- **Superar o limite de 20GB** por tenant
- **Melhorar performance** de queries filtradas por tenant + período
- **Reduzir RUs** ao limitar queries a poucos partitions

Exemplo:
```json
{
  "id": "nfe-123456",
  "tenantId": "empresa-abc",
  "ano": 2025,
  "mes": 10,
  "chaveAcesso": "12345678901234567890123456789012345678901234",
  "numeroNF": "123",
  "emitente": {
    "cnpj": "12345678000190",
    "nome": "Empresa XYZ"
  },
  "valorTotal": 1000.00
}
```

Query eficiente:
```python
# Busca limitada a: tenant "empresa-abc", ano 2025, mês 10
items = container.query_items(
    query="SELECT * FROM c WHERE c.emitente.cnpj = @cnpj",
    parameters=[{"name": "@cnpj", "value": "12345678000190"}],
    partition_key=["empresa-abc", 2025, 10]  # HPK
)
```

---

## Passo a Passo da Migração

### 1. Criar Recursos no Azure

```bash
# Login no Azure
az login

# Criar Resource Group
az group create --name fiscal-rg --location brazilsouth

# Criar Conta Cosmos DB
az cosmosdb create \
  --name fiscal-cosmosdb \
  --resource-group fiscal-rg \
  --locations regionName=brazilsouth failoverPriority=0 \
  --capabilities EnableServerless  # ou StandardProvisionedThroughput

# Criar Database
az cosmosdb sql database create \
  --account-name fiscal-cosmosdb \
  --resource-group fiscal-rg \
  --name fiscal_db

# Criar Container NFes com HPK
az cosmosdb sql container create \
  --account-name fiscal-cosmosdb \
  --database-name fiscal_db \
  --name nfes \
  --partition-key-path /tenantId /ano /mes \
  --partition-key-version 2 \
  --throughput 400  # ou use autoscale
```

### 2. Instalar SDK

```bash
pip install azure-cosmos
```

Adicione ao `requirements.txt`:
```
azure-cosmos>=4.5.0
```

### 3. Configurar Django

Crie `core/cosmos_client.py`:

```python
"""
Cliente Azure Cosmos DB
"""
import os
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.exceptions import CosmosResourceNotFoundError


class CosmosDBClient:
    """Cliente singleton para Cosmos DB"""
    
    _instance = None
    _client = None
    _database = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CosmosDBClient, cls).__new__(cls)
            cls._initialize()
        return cls._instance
    
    @classmethod
    def _initialize(cls):
        """Inicializa conexão com Cosmos DB"""
        endpoint = os.getenv('COSMOS_ENDPOINT')
        key = os.getenv('COSMOS_KEY')
        database_name = os.getenv('COSMOS_DATABASE', 'fiscal_db')
        
        if not endpoint or not key:
            raise ValueError("COSMOS_ENDPOINT e COSMOS_KEY devem estar configurados")
        
        cls._client = CosmosClient(endpoint, key)
        cls._database = cls._client.get_database_client(database_name)
    
    @classmethod
    def get_container(cls, container_name):
        """Retorna container específico"""
        return cls._database.get_container_client(container_name)
    
    @classmethod
    def get_nfes_container(cls):
        """Container de NFes"""
        return cls.get_container('nfes')
    
    @classmethod
    def get_ctes_container(cls):
        """Container de CTes"""
        return cls.get_container('ctes')


# Helper functions
def query_nfes(tenant_id, ano=None, mes=None, filters=None):
    """
    Query NFes com HPK otimizado
    
    Args:
        tenant_id: ID do tenant
        ano: Ano (opcional, para HPK)
        mes: Mês (opcional, para HPK)
        filters: Filtros adicionais SQL
    """
    container = CosmosDBClient.get_nfes_container()
    
    query = "SELECT * FROM c WHERE c.tenantId = @tenantId"
    parameters = [{"name": "@tenantId", "value": tenant_id}]
    
    if filters:
        query += f" AND {filters}"
    
    # Define partition key para otimizar query
    if ano and mes:
        partition_key = [tenant_id, ano, mes]
    elif ano:
        partition_key = [tenant_id, ano]  # Parcial HPK
    else:
        partition_key = None  # Cross-partition query (evite!)
    
    items = container.query_items(
        query=query,
        parameters=parameters,
        partition_key=partition_key,
        enable_cross_partition_query=(partition_key is None)
    )
    
    return list(items)


def create_nfe(nfe_data, tenant_id):
    """Cria nova NFe no Cosmos DB"""
    container = CosmosDBClient.get_nfes_container()
    
    # Adiciona campos para HPK
    nfe_data['tenantId'] = tenant_id
    nfe_data['ano'] = nfe_data['dataEmissao'].year
    nfe_data['mes'] = nfe_data['dataEmissao'].month
    
    return container.create_item(body=nfe_data)
```

### 4. Atualizar Models

Crie `core/cosmos_models.py`:

```python
"""
Models para Cosmos DB (Document-based)
"""
from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass, asdict


@dataclass
class NFe:
    """NFe para Cosmos DB"""
    
    id: str
    tenantId: str
    ano: int
    mes: int
    chaveAcesso: str
    numeroNF: str
    serie: str
    dataEmissao: datetime
    
    # Emitente
    emitente: dict
    
    # Destinatário
    destinatario: dict
    
    # Totais
    valorTotal: float
    valorProdutos: float
    valorICMS: float
    valorIPI: float
    
    # Itens
    itens: List[dict]
    
    # Metadados
    dataImportacao: datetime
    usuarioImportacao: str
    xmlContent: Optional[str] = None
    
    def to_dict(self):
        """Converte para dict para Cosmos DB"""
        data = asdict(self)
        # Converte datetime para ISO string
        data['dataEmissao'] = self.dataEmissao.isoformat()
        data['dataImportacao'] = self.dataImportacao.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Cria instância a partir de dict"""
        data['dataEmissao'] = datetime.fromisoformat(data['dataEmissao'])
        data['dataImportacao'] = datetime.fromisoformat(data['dataImportacao'])
        return cls(**data)
```

### 5. Migrar Dados Existentes

Crie script `scripts/migrate_to_cosmos.py`:

```python
"""
Script de migração MySQL -> Cosmos DB
"""
import os
import sys
from datetime import datetime

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xml_manager.settings')
import django
django.setup()

from core.models import NFe as MySQLNFe
from core.cosmos_client import CosmosDBClient, create_nfe


def migrate_nfes(tenant_id, batch_size=100):
    """Migra NFes do MySQL para Cosmos DB"""
    
    total = MySQLNFe.objects.count()
    migrated = 0
    
    print(f"Migrando {total} NFes para Cosmos DB...")
    
    for nfe in MySQLNFe.objects.all().iterator(chunk_size=batch_size):
        # Converte modelo MySQL para formato Cosmos DB
        nfe_data = {
            'id': f"nfe-{nfe.id}",
            'chaveAcesso': nfe.chave_acesso,
            'numeroNF': nfe.numero_nf,
            'serie': nfe.serie,
            'dataEmissao': nfe.data_emissao,
            'emitente': {
                'cnpj': nfe.emit_cnpj,
                'nome': nfe.emit_nome,
                'fantasia': nfe.emit_fantasia,
                'endereco': nfe.emit_endereco,
                'municipio': nfe.emit_municipio,
                'uf': nfe.emit_uf
            },
            'destinatario': {
                'cnpjCpf': nfe.dest_cnpj_cpf,
                'nome': nfe.dest_nome,
                'endereco': nfe.dest_endereco,
                'municipio': nfe.dest_municipio,
                'uf': nfe.dest_uf
            },
            'valorTotal': float(nfe.valor_total or 0),
            'valorProdutos': float(nfe.valor_produtos or 0),
            'valorICMS': float(nfe.valor_icms or 0),
            'valorIPI': float(nfe.valor_ipi or 0),
            'itens': [
                {
                    'numeroItem': item.numero_item,
                    'codigoProduto': item.codigo_produto,
                    'descricao': item.descricao,
                    'quantidade': float(item.quantidade or 0),
                    'valorUnitario': float(item.valor_unitario or 0),
                    'valorTotal': float(item.valor_total or 0)
                }
                for item in nfe.itens.all()
            ],
            'dataImportacao': nfe.data_importacao,
            'usuarioImportacao': nfe.usuario_importacao.username if nfe.usuario_importacao else 'system',
            'xmlContent': nfe.xml_content
        }
        
        try:
            create_nfe(nfe_data, tenant_id)
            migrated += 1
            
            if migrated % 100 == 0:
                print(f"Migrados: {migrated}/{total}")
        
        except Exception as e:
            print(f"Erro ao migrar NFe {nfe.id}: {e}")
    
    print(f"Migração concluída: {migrated}/{total} NFes")


if __name__ == '__main__':
    tenant_id = input("Digite o Tenant ID: ")
    migrate_nfes(tenant_id)
```

Execute:
```bash
python scripts/migrate_to_cosmos.py
```

### 6. Atualizar Views

Adapte views para usar Cosmos DB:

```python
from core.cosmos_client import query_nfes, create_nfe


@login_required
def nfe_list_cosmos(request):
    """Lista NFes do Cosmos DB"""
    
    tenant_id = request.user.profile.tenant_id
    ano = request.GET.get('ano')
    mes = request.GET.get('mes')
    
    # Query otimizada com HPK
    nfes = query_nfes(
        tenant_id=tenant_id,
        ano=int(ano) if ano else None,
        mes=int(mes) if mes else None
    )
    
    return render(request, 'core/nfe_list.html', {'nfes': nfes})
```

---

## Best Practices

### 1. Particionamento
- Use HPK para documentos com crescimento > 20GB por tenant
- Sempre inclua `partition_key` em queries quando possível
- Evite cross-partition queries em produção

### 2. Indexação
```python
# Customize indexação no container
indexing_policy = {
    "indexingMode": "consistent",
    "includedPaths": [
        {"path": "/emitente/cnpj/?"},
        {"path": "/destinatario/cnpjCpf/?"},
        {"path": "/dataEmissao/?"}
    ],
    "excludedPaths": [
        {"path": "/xmlContent/?"}  # Não indexa XML completo
    ]
}
```

### 3. Request Units (RUs)
- Comece com **400 RU/s** por container (serverless ou provisionado)
- Use **autoscale** para ajustar automaticamente
- Monitore uso com Azure Monitor

### 4. Logging de Diagnóstico
```python
# Sempre capture diagnóstico em queries lentas
result = container.query_items(...)
print(f"RU charge: {container.client_connection.last_response_headers['x-ms-request-charge']}")
```

---

## Custos Estimados

| Modelo | NFes/mês | RU/s | Custo/mês (USD) |
|--------|----------|------|-----------------|
| Serverless | < 10k | Auto | ~$15-30 |
| Provisioned | 10k-100k | 400 | ~$24 |
| Autoscale | 100k+ | 400-4000 | ~$40-200 |

💡 **Recomendação:** Comece com **Serverless** para testes, migre para **Autoscale** em produção.

---

## Monitoramento

Use Azure Monitor para:
- Latência de queries
- Consumo de RUs
- Throttling (429 errors)
- Distribuição de dados por partition

---

## Documentação Oficial

- [Azure Cosmos DB Documentation](https://learn.microsoft.com/azure/cosmos-db/)
- [Python SDK](https://learn.microsoft.com/azure/cosmos-db/sql/sdk-python)
- [Hierarchical Partition Keys](https://learn.microsoft.com/azure/cosmos-db/hierarchical-partition-keys)
- [Well-Architected Framework](https://learn.microsoft.com/azure/well-architected/service-guides/cosmos-db)
