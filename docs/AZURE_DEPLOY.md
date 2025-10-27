# 🚀 Guia de Deploy no Azure

Este guia cobre o deploy do Sistema Fiscal em Azure usando diferentes serviços.

---

## 📋 Pré-requisitos

1. **Conta Azure ativa**
2. **Azure CLI instalado**
3. **Docker instalado**
4. **Projeto configurado localmente**

---

## 🎯 Opções de Deploy

### Opção 1: Azure App Service (Recomendado para começar)
### Opção 2: Azure Container Instances (Simples)
### Opção 3: Azure Kubernetes Service (Produção em escala)

---

## 1️⃣ Azure App Service

### Passo 1: Login no Azure

```bash
# Login
az login

# Configurar subscription
az account set --subscription "Nome-da-Subscription"
```

### Passo 2: Criar Resource Group

```bash
az group create \
  --name fiscal-rg \
  --location brazilsouth
```

### Passo 3: Criar App Service Plan

```bash
# Plan básico
az appservice plan create \
  --name fiscal-plan \
  --resource-group fiscal-rg \
  --location brazilsouth \
  --is-linux \
  --sku B1

# Para produção, use P1V2 ou superior
# --sku P1V2
```

### Passo 4: Criar Web App

```bash
az webapp create \
  --name fiscal-app-seu-nome \
  --resource-group fiscal-rg \
  --plan fiscal-plan \
  --runtime "PYTHON:3.11"
```

### Passo 5: Configurar Variáveis de Ambiente

```bash
az webapp config appsettings set \
  --name fiscal-app-seu-nome \
  --resource-group fiscal-rg \
  --settings \
    DJANGO_SECRET_KEY="sua-chave-secreta" \
    DJANGO_DEBUG="False" \
    ALLOWED_HOSTS="fiscal-app-seu-nome.azurewebsites.net" \
    DB_NAME="fiscal_db" \
    DB_USER="fiscal_user" \
    DB_PASS="senha-segura" \
    DB_HOST="fiscal-mysql.mysql.database.azure.com" \
    DB_PORT="3306" \
    CSRF_TRUSTED_ORIGINS="https://fiscal-app-seu-nome.azurewebsites.net"
```

### Passo 6: Criar Azure Database for MySQL

```bash
# Criar servidor MySQL
az mysql flexible-server create \
  --name fiscal-mysql \
  --resource-group fiscal-rg \
  --location brazilsouth \
  --admin-user fiscal_admin \
  --admin-password "SenhaSegura123!" \
  --sku-name Standard_B1ms \
  --storage-size 32 \
  --version 8.0.21

# Criar database
az mysql flexible-server db create \
  --resource-group fiscal-rg \
  --server-name fiscal-mysql \
  --database-name fiscal_db

# Configurar firewall (permitir Azure services)
az mysql flexible-server firewall-rule create \
  --resource-group fiscal-rg \
  --name fiscal-mysql \
  --rule-name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

### Passo 7: Deploy do Código

```bash
# Via Git local
az webapp deployment source config-local-git \
  --name fiscal-app-seu-nome \
  --resource-group fiscal-rg

# Obter URL do Git
az webapp deployment list-publishing-credentials \
  --name fiscal-app-seu-nome \
  --resource-group fiscal-rg \
  --query scmUri \
  --output tsv

# Adicionar remote e push
git remote add azure <URL_DO_GIT>
git push azure main
```

### Passo 8: Executar Migrations

```bash
# Via SSH
az webapp ssh --name fiscal-app-seu-nome --resource-group fiscal-rg

# Dentro do SSH
python manage.py migrate
python scripts/create_superuser.py
exit
```

### Passo 9: Verificar Deploy

```bash
# Abrir no navegador
az webapp browse --name fiscal-app-seu-nome --resource-group fiscal-rg
```

---

## 2️⃣ Azure Container Instances

### Passo 1: Build e Push para Azure Container Registry

```bash
# Criar Container Registry
az acr create \
  --name fiscalacr \
  --resource-group fiscal-rg \
  --sku Basic \
  --admin-enabled true

# Login no registry
az acr login --name fiscalacr

# Build e push da imagem
docker build -t fiscalacr.azurecr.io/fiscal-app:latest .
docker push fiscalacr.azurecr.io/fiscal-app:latest
```

### Passo 2: Criar Container Instance

```bash
# Obter senha do ACR
ACR_PASSWORD=$(az acr credential show --name fiscalacr --query "passwords[0].value" -o tsv)

# Criar container
az container create \
  --name fiscal-container \
  --resource-group fiscal-rg \
  --image fiscalacr.azurecr.io/fiscal-app:latest \
  --registry-login-server fiscalacr.azurecr.io \
  --registry-username fiscalacr \
  --registry-password $ACR_PASSWORD \
  --dns-name-label fiscal-app-seu-nome \
  --ports 8080 \
  --environment-variables \
    DJANGO_SECRET_KEY="sua-chave" \
    DJANGO_DEBUG="False" \
    DB_HOST="fiscal-mysql.mysql.database.azure.com" \
  --secure-environment-variables \
    DB_PASS="senha-segura"
```

---

## 3️⃣ Azure Kubernetes Service (AKS)

### Passo 1: Criar AKS Cluster

```bash
az aks create \
  --name fiscal-aks \
  --resource-group fiscal-rg \
  --node-count 2 \
  --node-vm-size Standard_B2s \
  --generate-ssh-keys \
  --enable-managed-identity

# Obter credenciais
az aks get-credentials --name fiscal-aks --resource-group fiscal-rg
```

### Passo 2: Criar Kubernetes Manifests

**deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fiscal-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fiscal
  template:
    metadata:
      labels:
        app: fiscal
    spec:
      containers:
      - name: web
        image: fiscalacr.azurecr.io/fiscal-app:latest
        ports:
        - containerPort: 8080
        env:
        - name: DJANGO_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: fiscal-secrets
              key: secret-key
        - name: DB_HOST
          value: "fiscal-mysql.mysql.database.azure.com"
---
apiVersion: v1
kind: Service
metadata:
  name: fiscal-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8080
  selector:
    app: fiscal
```

### Passo 3: Deploy no AKS

```bash
# Criar secrets
kubectl create secret generic fiscal-secrets \
  --from-literal=secret-key="sua-chave-secreta"

# Deploy
kubectl apply -f deployment.yaml

# Verificar status
kubectl get pods
kubectl get services

# Obter IP público
kubectl get service fiscal-service
```

---

## 🗄️ Azure Cosmos DB (Recomendado para Produção)

### Criar Cosmos DB Account

```bash
az cosmosdb create \
  --name fiscal-cosmosdb \
  --resource-group fiscal-rg \
  --locations regionName=brazilsouth failoverPriority=0 \
  --capabilities EnableServerless

# Criar database
az cosmosdb sql database create \
  --account-name fiscal-cosmosdb \
  --resource-group fiscal-rg \
  --name fiscal_db

# Criar containers com HPK
az cosmosdb sql container create \
  --account-name fiscal-cosmosdb \
  --database-name fiscal_db \
  --name nfes \
  --partition-key-path /tenantId /ano /mes \
  --partition-key-version 2

az cosmosdb sql container create \
  --account-name fiscal-cosmosdb \
  --database-name fiscal_db \
  --name ctes \
  --partition-key-path /tenantId /ano /mes \
  --partition-key-version 2

# Obter connection string
az cosmosdb keys list \
  --name fiscal-cosmosdb \
  --resource-group fiscal-rg \
  --type connection-strings
```

---

## 🔐 Azure Key Vault (Segurança)

### Criar e Configurar Key Vault

```bash
# Criar Key Vault
az keyvault create \
  --name fiscal-keyvault \
  --resource-group fiscal-rg \
  --location brazilsouth

# Adicionar secrets
az keyvault secret set \
  --vault-name fiscal-keyvault \
  --name django-secret-key \
  --value "sua-chave-secreta"

az keyvault secret set \
  --vault-name fiscal-keyvault \
  --name db-password \
  --value "senha-do-banco"

# Dar permissão ao App Service
APP_IDENTITY=$(az webapp identity assign \
  --name fiscal-app-seu-nome \
  --resource-group fiscal-rg \
  --query principalId \
  --output tsv)

az keyvault set-policy \
  --name fiscal-keyvault \
  --object-id $APP_IDENTITY \
  --secret-permissions get list

# Configurar referências no App Service
az webapp config appsettings set \
  --name fiscal-app-seu-nome \
  --resource-group fiscal-rg \
  --settings \
    DJANGO_SECRET_KEY="@Microsoft.KeyVault(SecretUri=https://fiscal-keyvault.vault.azure.net/secrets/django-secret-key/)"
```

---

## 📊 Azure Monitor

### Configurar Application Insights

```bash
# Criar Application Insights
az monitor app-insights component create \
  --app fiscal-insights \
  --location brazilsouth \
  --resource-group fiscal-rg \
  --application-type web

# Obter instrumentation key
az monitor app-insights component show \
  --app fiscal-insights \
  --resource-group fiscal-rg \
  --query instrumentationKey

# Adicionar ao App Service
az webapp config appsettings set \
  --name fiscal-app-seu-nome \
  --resource-group fiscal-rg \
  --settings \
    APPINSIGHTS_INSTRUMENTATIONKEY="sua-key"
```

---

## 🔄 CI/CD com Azure DevOps

### Azure Pipeline (azure-pipelines.yml)

```yaml
trigger:
  branches:
    include:
    - main

pool:
  vmImage: 'ubuntu-latest'

variables:
  azureSubscription: 'Sua-Service-Connection'
  webAppName: 'fiscal-app-seu-nome'
  pythonVersion: '3.11'

stages:
- stage: Build
  jobs:
  - job: BuildJob
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '$(pythonVersion)'

    - script: |
        pip install -r requirements.txt
        python manage.py test
      displayName: 'Install dependencies and test'

    - task: Docker@2
      inputs:
        command: buildAndPush
        repository: 'fiscal-app'
        dockerfile: 'Dockerfile'
        tags: '$(Build.BuildId)'

- stage: Deploy
  dependsOn: Build
  jobs:
  - job: DeployJob
    steps:
    - task: AzureWebApp@1
      inputs:
        azureSubscription: '$(azureSubscription)'
        appName: '$(webAppName)'
        package: '$(System.DefaultWorkingDirectory)/**/*.zip'
```

---

## 🧹 Limpeza de Recursos

```bash
# CUIDADO: Isso deleta TUDO!
az group delete --name fiscal-rg --yes --no-wait
```

---

## 📈 Custos Estimados (USD/mês)

| Serviço | Tier | Custo Estimado |
|---------|------|----------------|
| App Service (B1) | Basic | ~$13 |
| MySQL Flexible (B1ms) | Basic | ~$15 |
| Cosmos DB | Serverless | ~$25 |
| Container Registry | Basic | ~$5 |
| Application Insights | - | ~$10 |
| **Total Básico** | | **~$68/mês** |

---

## 🔗 Links Úteis

- [Azure CLI Reference](https://learn.microsoft.com/cli/azure/)
- [App Service Documentation](https://learn.microsoft.com/azure/app-service/)
- [Azure Cosmos DB](https://learn.microsoft.com/azure/cosmos-db/)
- [AKS Documentation](https://learn.microsoft.com/azure/aks/)
- [Azure Monitor](https://learn.microsoft.com/azure/azure-monitor/)

---

## 📞 Suporte

Problemas com deploy?
- 📧 Email: suporte@aviladevops.com.br
- 📖 Docs Azure: https://docs.microsoft.com/azure

---

**Bom deploy! 🚀**
