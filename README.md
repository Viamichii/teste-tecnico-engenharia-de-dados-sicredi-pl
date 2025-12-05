# 🏦 Desafio Técnico – Engenharia de Dados (Sicredi)

Pipeline ETL completa usando SQL Server, PySpark, Python e Docker

Este projeto implementa uma pipeline completa de ingestão e transformação de dados, simulando um fluxo real de engenharia de dados utilizado em ambientes corporativos.

## 📝 Observações (como solicitado no desafio)

### Por que optei por este design?

Escolhi estruturar o projeto com camadas Bronze → Silver, aplicando conceitos de pipelines modernas (Databricks/Lakehouse).
Assim, o fluxo fica organizado, escalável, testável e semelhante a ambientes reais.

### O que faria se tivesse mais tempo?

- Solucionario o problema no docker e comecaria o projeto por ele
- Criaria testes unitários para validação de cada etapa
- Construiria um BI consumindo o CSV Silver
- Automatizaria a criação do usuário SQL (sicredi_user) diretamente no Docker

### Dificuldades encontradas

**SQL Server + Docker:**
Usei Microsoft SQL Server, que roda nativamente em Windows, mas o container oficial utiliza Linux.
Isso exigiu atenção extra na integração, especialmente nos drivers JDBC/ODBC.

**Criação do usuário `sicredi_user`:**
A criação automática do usuário no primeiro login não funcionou como esperado dentro do Docker.
Recomendo que o avaliador crie o usuário manualmente antes de testar, garantindo melhor performance na ETL:

```sql
CREATE LOGIN sicredi_user WITH PASSWORD = 'SenhaForte123!';
CREATE USER sicredi_user FOR LOGIN sicredi_user;
ALTER ROLE db_owner ADD MEMBER sicredi_user;
```

**Tempo de build:**
O tempo de build do Docker é maior que o normal, pois Spark precisa ser instalado dentro da imagem.

## O objetivo é demonstrar:

- Criação e organização de um ambiente de dados
- Geração automática de dados transacionais
- Leitura a partir de um banco SQL Server
- Processamento Bronze → Silver com PySpark
- Transformações, normalização e flatten
- Salvamento em Parquet (Bronze) e CSV (Silver)
- Execução automatizada em Docker (bonus)

## 📁 Arquitetura do Projeto

```
teste-tecnico-engenharia-de-dados-sicredi-pl/
│
├── sql/
│   ├── schema.sql               # Criação das tabelas e usuário
│   └── data_generator.py        # Geração dos dados fictícios no SQL Server
│
├── etl/
│   └── etl_sicooperative.py     # Pipeline completa (Bronze + Silver)
│
├── data/
│   ├── bronze/                  # Armazena Parquet
│   └── silver/                  # Armazena CSV final
│
├── configs.py                   # Configurações globais
├── Dockerfile                   # Executa a ETL no container
├── docker-compose.yml           # Subir SQL Server + ETL
└── README.md                    # Este arquivo
```

## 🧠 Lógica do Projeto (Pipeline)

O pipeline foi projetado simulando uma arquitetura de dados moderna, semelhante à utilizada em squads de engenharia, seguindo os padrões Bronze → Silver.

### 1️⃣ Camada SQL (Fonte dos Dados)

O arquivo `schema.sql` cria as tabelas:
- associado
- conta
- cartao
- movimento

**Observação:** Não foi possível criar a coluna data de criação do cartão, pois ela não existe no modelo fornecido.

### 2️⃣ Geração de Dados Fictícios (data_generator.py)

- Gera 100 associados aleatórios
- Para cada associado:
  - Cria conta
  - Cria cartão
  - Gera 3–8 movimentos
- Usa Faker + pyodbc
- Apenas insere dados válidos (PK autoincremento garante não duplicação)

Esse script simula um ambiente produtivo recebendo dados transacionais.

### 3️⃣ Camada Bronze (Parquet)

O PySpark lê diretamente o SQL Server usando JDBC:
- associado
- conta
- cartao
- movimento

E salva em: `data/bronze/<tabela>/*.parquet`

A Bronze é sempre overwrite, imitando cargas full próximas do mundo real.

### 4️⃣ Camada Silver (Transformação Final)

Operações aplicadas:
- Joins entre as quatro tabelas
- Flatten para formato analítico
- Normalização
- Cast de tipos para strings (exigido no desafio)

Geração de CSV único: `data/silver/sicredi_movimentos.csv`

## 🚀 Como Executar

### Opção 1: Localmente com Python venv

#### 1. Criar e ativar o ambiente virtual:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

#### 2. Instalar dependências:

```bash
pip install -r requirements.txt
```

#### 3. Verificar configurações:

Ajuste as variáveis em `configs.py` ou configure via variáveis de ambiente:
- `DB_HOST` (padrão: localhost)
- `DB_PORT` (padrão: 1433)
- `DB_USER` (padrão: sicredi_user)
- `DB_PASSWORD`

#### 4. Popular o banco de dados (opcional):

Se o SQL Server estiver rodando localmente:
```bash
python sql/data_generator.py
```

#### 5. Executar a pipeline ETL completa:

```bash
python etl/etl_sicooperative.py
```

Isso irá:
1. Conectar ao SQL Server
2. Gerar dados fictícios (se necessário)
3. Criar a camada Bronze (Parquet)
4. Criar a camada Silver (CSV)
5. Salvar em `data/bronze/` e `data/silver/`

---

### Opção 2: Com Docker Compose (Recomendado)

O Docker automatiza todo o ambiente, subindo SQL Server + ETL em containers.

#### 1. Construir e executar:

```bash
docker compose up --build
```

Durante a execução:
1. ✅ SQL Server é inicializado
2. ✅ Tabelas são criadas automaticamente
3. ✅ Dados fictícios são gerados
4. ✅ Pipeline Bronze é produzida
5. ✅ Pipeline Silver é produzida
6. ✅ Logs são exibidos no console

#### 2. Executar componentes isolados:

Subir apenas o SQL Server (manter em background):
```bash
docker compose up -d sqlserver
```

Depois executar a ETL:
```bash
docker compose run --rm etl python etl/etl_sicooperative.py
```

#### 3. Ver logs:

```bash
# Logs da ETL
docker compose logs -f etl

# Logs do SQL Server
docker compose logs -f sqlserver
```

#### 4. Parar os containers:

```bash
docker compose down
```

---

### Opção 3: PowerShell Automatizado (Windows)

Se desejar automação completa via script PowerShell:

```powershell
# Permitir execução de scripts (uma vez por sessão)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Executar o fluxo completo
.\run_all.ps1
```

**Nota:** O primeiro build pode demorar vários minutos (PySpark é grande).

---

## 🛠 Tecnologias Utilizadas

| Tecnologia | Uso |
|------------|-----|
| SQL Server | Fonte transacional |
| PySpark | Processamento distribuído |
| Python | Orquestrações, geração de dados |
| Docker | Automação e provisionamento |
| Faker | Geração de dados simulados |
| Parquet | Armazenamento Bronze |
| CSV | Entrega Silver |

## 🔍 Troubleshooting

### A ETL falha por conexão com SQL Server
- **venv:** Verifique se o SQL Server está rodando localmente
- **Docker:** Aguarde alguns segundos para o SQL Server inicializar (verifique com `docker compose logs sqlserver`)
- Confirme credenciais em `configs.py` ou variáveis de ambiente

### Erro ODBC / pyodbc
- erro entre conexao do sqlserver e ubunto no docker, erro se refere ao conector e driver que o ubunto nao tem.

## 📌 Observações Importantes

- Estamos simulando um sistema real, onde a aplicação consome dados armazenados em SQL Server
- O Docker representa um cenário de ambiente separado (como Produção x Desenvolvimento)
- A coluna data de criação do cartão não pôde ser implementada porque não existe no modelo fornecido

