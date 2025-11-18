
-----

# Laboratório de Estudos de Big Data: Stack Hadoop & Spark com Docker

## 🎯 Objetivo do Projeto

Este repositório documenta a jornada de construção de um ecossistema completo de Big Data, do zero, utilizando Docker Compose. O objetivo principal é o aprendizado prático e aprofundado dos componentes fundamentais de uma arquitetura de dados moderna, desde o armazenamento distribuído até o processamento em larga escala para ETL, Machine Learning e visualização de dados.

O projeto foi construído de forma incremental, peça por peça, para permitir o entendimento das dependências e da interação entre cada serviço, replicando em um ambiente local os desafios de configuração e depuração (e compatibilidade de versões) encontrados em sistemas de produção.

## 🏛️ Arquitetura da Solução

A arquitetura implementada segue o padrão de um Data Lake moderno, com camadas bem definidas para ingestão, armazenamento, processamento e consumo de dados.

  * **Camada de Armazenamento (Data Lake):** Utiliza **HDFS** para armazenar dados em seu formato bruto (`raw`) e processado (`processed`).
  * **Camada de Gerenciamento de Recursos:** O **YARN** atua como o "sistema operacional" do cluster, gerenciando os recursos de CPU e memória para as aplicações.
  * **Camada de Catálogo de Metadados:** O **Apache Hive**, através do **Hive Metastore** (com backend em PostgreSQL), serve como um catálogo central para todos os dados do Data Lake.
  * **Camada de Processamento (ETL & ML):** O **Apache Spark** é o motor principal para o processamento de dados, executando pipelines de ETL e preparando dados para Machine Learning.
  * **Camada de Serviço (Serving Layer):** Para acesso de baixa latência, utilizamos **Apache HBase**. Para habilitar o acesso SQL, criamos **imagens Docker customizadas** (`thedarklordottm/hbase-phoenix-*`) que embutem o **Apache Phoenix** diretamente nos serviços do HBase.
  * **Camada de Visualização (BI):** O **Apache Superset** é usado para criar dashboards e visualizações. Para garantir a conectividade com todas as nossas fontes de dados (PostgreSQL, Hive, Phoenix, MySQL, etc.), foi criada uma **imagem Docker customizada** do Superset que inclui bibliotecas essenciais como `Pillow` (para exportação de imagens), `psycopg2`, `sqlalchemy-phoenix`, `mysqlclient`, `pyhive` e outras.
  * **Camada de Automação:** O **n8n** é utilizado para a automação de workflows e integração entre serviços.
  * **Camada de Orquestração:** O **Apache Airflow** (com backend em MySQL) está configurado para agendar, executar e monitorar os pipelines de dados de forma programática.

## 🛠️ Tecnologias Utilizadas (Stack)

| Categoria | Componente | Status |
| :--- | :--- | :--- |
| **Infraestrutura** | Docker & Docker Compose | ✅ **Implementado** |
| **Armazenamento (Storage)** | HDFS (Namenode, Datanode) | ✅ **Implementado** |
| **Gerenciamento de Recursos** | YARN (ResourceManager, NodeManager) | ✅ **Implementado** |
| **Catálogo de Metadados** | Hive Metastore + PostgreSQL | ✅ **Implementado** |
| **Acesso SQL (Data Lake)** | Hive Server | ✅ **Implementado** |
| **Processamento Distribuído** | Apache Spark (Master, Worker) | ✅ **Implementado** |
| **Coordenação** | Apache ZooKeeper | ✅ **Implementado** |
| **Banco NoSQL (Serving Layer)**| Apache HBase (Master, RegionServer) | ✅ **Implementado** |
| **Camada SQL para NoSQL** | Apache Phoenix (embutido no HBase) | ✅ **Implementado** |
| **Orquestração de Pipeline** | Apache Airflow + MySQL | ✅ **Implementado** |
| **Visualização de Dados (BI)**| Apache Superset | ✅ **Implementado** |
| **Automação de Workflow** | n8n | ✅ **Implementado** |


## 🚀 Como Executar o Projeto

1.  **Pré-requisitos:**

      * Docker e Docker Compose instalados.
      * Git para clonar o repositório.

2.  **Configuração:**

      * Clone este repositório: `git clone <URL_DO_SEU_REPOSITÓRIO>`
      * Navegue para a pasta do projeto: `cd <NOME_DA_PASTA>`
      * Certifique-se de que todos os arquivos de configuração (`hadoop.env`, `hive-conf/hive-site.xml`, `hbase-conf/hbase-site.xml`, `zoo-conf/zoo.cfg`) estão presentes.

3.  **Execução:**

      * Para subir todo o ambiente em segundo plano, execute:
        ```bash
        docker-compose up -d
        ```
      * Para verificar o status dos serviços:
        ```bash
        docker-compose ps
        ```

4.  **Acessando as Interfaces Web:**

      * **HDFS (Namenode):** `http://localhost:9870`
      * **YARN (ResourceManager):** `http://localhost:8088`
      * **Spark (Master):** `http://localhost:8081`
      * **Hive (Server2 UI):** `http://localhost:10002`
      * **HBase (Master):** `http://localhost:16010`
      * **HBase (RegionServer):** `http://localhost:16030`
      * **Superset (BI):** `http://localhost:8090`
      * **n8n (Automação):** `http://localhost:5678`
      * **Airflow (Orquestração):** `http://localhost:8080` (Quando reativado)

## ⚡ Exemplos de Uso

### Conectar ao Hive via Beeline

```bash
# Entrar no contêiner do hive-server
docker exec -it hive-server /bin/bash

# Conectar ao serviço
beeline -u jdbc:hive2://localhost:10000
```

### Submeter um Job PySpark

```bash
# Submeter o script 'meu_job.py' localizado na pasta 'jobs'
docker exec spark-master /spark/bin/spark-submit /opt/spark/jobs/meu_job.py
```

### Conectar ao HBase/Phoenix via SQL

O HBase por si só não fala SQL. Nossas imagens customizadas usam o Apache Phoenix para criar uma camada de acesso SQL.

**1. Iniciar o Phoenix Query Server (PQS):**
Este serviço atua como um "tradutor" que recebe SQL e o converte em chamadas HBase. Ele precisa ser iniciado manualmente:

```bash
docker exec -d hbase-master /opt/phoenix/bin/queryserver.py start
```


**2. Conectar via Superset:**
Na UI do Superset, adicione um novo banco de dados usando a seguinte string de conexão (SQLAlchemy URI):
`phoenix://hbase-master:8765/`

**3. (Alternativo) Conectar via Cliente de Linha de Comando:**

```bash
# Entrar no contêiner do hbase-master
docker exec -it hbase-master /bin/bash

# Iniciar o cliente sqlline (requer python2 na imagem)
python2 /opt/phoenix/bin/sqlline.py zookeeper:2181
```

### Inicializando o Apache Superset (Primeira Vez)

O Superset não cria um usuário administrador automaticamente. Após subir os serviços `superset-db` e `superset-redis`, você precisa rodar os seguintes comandos **em ordem** para inicializar a aplicação:

```bash
# 1. Atualiza o banco de dados interno do Superset
docker-compose run --rm superset superset db upgrade

# 2. Cria um usuário administrador (siga os prompts interativos)
docker-compose run --rm superset superset fab create-admin

# 3. Inicializa as permissões e papéis padrão
docker-compose run --rm superset superset init

# 4. Inicie o serviço principal
docker-compose up -d superset
```


-----

*Este projeto é um ambiente de estudos e não se destina ao uso em produção.*