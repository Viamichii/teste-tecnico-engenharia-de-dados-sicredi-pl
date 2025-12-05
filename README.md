# 🏦 Desafio Técnico – Engenharia de Dados (Sicredi)

Pipeline ETL completa usando SQL Server, PySpark, Python e Docker

Este projeto implementa uma pipeline completa de ingestão e transformação de dados, simulando um fluxo real de engenharia de dados utilizado em ambientes corporativos.

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

## 🚀 Execução Completa Automatizada (Pipeline Única)

O arquivo `etl_sicooperative.py` orquestra:
1. Criação da SparkSession
2. Execução do data_generator
3. Geração da Bronze
4. Geração da Silver
5. Fechamento da sessão Spark

Esse script é usado pelo Docker como ponto de entrada para rodar tudo automaticamente.

## 🐳 Execução com Docker (Bônus do Desafio)

O ambiente foi containerizado com `docker-compose.yml`, que sobe:
- Um container SQL Server
- Um container Python que executa a pipeline completa

### Para rodar:

```bash
docker compose up --build
```

Durante a execução:
1. O SQL Server é iniciado
2. Gera dados fictícios
3. Produz Bronze
4. Produz Silver

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

## 📌 Observações Importantes

- Estamos simulando um sistema real, onde a aplicação consome dados armazenados em SQL Server.
- O Docker representa um cenário de ambiente separado (como Produção x Desenvolvimento).
- A coluna data de criação do cartão não pôde ser implementada porque não existe no modelo fornecido.

## 🧪 Como Executar Localmente

### 1. Criar ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Rodar somente a ETL:
```bash
python etl/etl_sicooperative.py
```

### 3. Rodar tudo com Docker:
```bash
docker compose up --build
```

## 🏁 Como executar o ETL — passo a passo

1) Rodar localmente (venv)
- Criar e ativar virtualenv:
  - Windows:
    - python -m venv venv
    - venv\Scripts\activate
  - Linux/macOS:
    - python -m venv venv
    - source venv/bin/activate
- Instalar dependências:
  - pip install -r requirements.txt
- Verificar configs:
  - Ajuste variáveis em configs.py ou via env vars (DB_HOST, DB_PORT, DB_USER, DB_PASSWORD).
- Rodar gerador de dados (opcional, popula o banco):
  - python sql/data_generator.py
- Rodar pipeline completa:
  - python etl/etl_sicooperative.py

2) Rodar com Docker (recomendado para reproducibilidade)
- Subir todo o ambiente (SQL Server + ETL):
  - docker compose up --build
- Executar apenas o ETL (após subir o SQL Server):
  - docker compose up -d sqlserver
  - docker compose run --rm etl python etl/etl_sicooperative.py
- Ver logs:
  - docker compose logs -f etl
  - docker compose logs -f sqlserver

3) Verificações e troubleshooting rápido
- A ETL falha por conexão:
  - Verifique se o SQL Server está healthy (checar logs e healthcheck do compose).
  - Confirme credenciais e host em configs.py / variáveis de ambiente.
- Erro ODBC / pyodbc:
  - Dentro do container, teste conexão via um pequeno script pyodbc ou rodando sql/data_generator.py isolado.
  - Se faltar driver ODBC, considere instalar `unixodbc`/driver apropriado ou ajustar Dockerfile, mas prefira a imagem sugerida (bitnami/spark) e unixodbc.
- Se o build Docker demora:
  - Use a imagem base com PySpark pré-instalado (já configurada no Dockerfile do projeto).
  - Evite reinstalar pyspark no pip dentro do container.
- Teste incremental:
  - Primeiro execute sql/data_generator.py para verificar inserção no DB.
  - Depois execute apenas a parte de leitura (ex.: rodar um script que lê uma tabela via pandas/pyodbc).

4) Dicas finais
- Para depurar rapidamente, rode os scripts localmente fora do Docker (isso isola problemas de driver/build).
- Ajuste spark.conf ("spark.sql.shuffle.partitions") no etl_sicooperative.py para volumes pequenos (já definido para 1 no projeto).

## ✔️ Resultado Final

Ao final da execução você terá:

### 📁 Bronze
Parquets organizados por tabela.

### 📁 Silver
CSV analítico final contendo os movimentos flatenados.

### 🎯 Pipeline concluída de ponta a ponta
Simulando um ambiente real com:
- Dados transacionais
- Processamento estruturado
- Workflow completo
- Automação via Docker