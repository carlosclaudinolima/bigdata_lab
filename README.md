-----

# Laboratório de Estudos de Big Data: Stack Hadoop & Spark com Docker

## 🎯 Objetivo do Projeto

Este repositório documenta a jornada de construção de um ecossistema completo de Big Data, do zero, utilizando Docker Compose. O objetivo principal é o aprendizado prático e aprofundado dos componentes fundamentais de uma arquitetura de dados moderna, desde o armazenamento distribuído até o processamento em larga escala para ETL e Machine Learning.

O projeto foi construído de forma incremental, peça por peça, para permitir o entendimento das dependências e da interação entre cada serviço, replicando em um ambiente local os desafios de configuração e depuração encontrados em sistemas de produção.

## 🏛️ Arquitetura da Solução

A arquitetura implementada segue o padrão de um Data Lake moderno, com camadas bem definidas para ingestão, armazenamento, processamento e consumo de dados.

  * **Camada de Armazenamento (Data Lake):** Utiliza **HDFS** para armazenar dados em seu formato bruto (`raw`) e processado (`processed`), garantindo escalabilidade e resiliência.
  * **Camada de Gerenciamento de Recursos:** O **YARN** atua como o "sistema operacional" do cluster, gerenciando os recursos de CPU e memória para as aplicações.
  * **Camada de Catálogo de Metadados:** O **Apache Hive**, através do **Hive Metastore**, serve como um catálogo central e persistente para todos os dados do Data Lake, provendo uma camada de abstração sobre os arquivos físicos. O **Hive Server** oferece um endpoint SQL para consultas ad-hoc e integração com ferramentas de BI.
  * **Camada de Processamento (ETL & ML):** O **Apache Spark** é o motor principal para o processamento de dados em larga escala. Ele é usado para executar pipelines de ETL (lendo dados brutos, aplicando transformações e salvando em formatos otimizados como Parquet) e para o treinamento de modelos de Machine Learning.
  * **Camada de Orquestração:** O **Apache Airflow** é utilizado para agendar, executar e monitorar os pipelines de dados de forma programática.

## 🛠️ Tecnologias Utilizadas (Stack)

| Categoria | Componente | Status |
| :--- | :--- | :--- |
| **Infraestrutura** | Docker & Docker Compose | **Implementado** |
| **Armazenamento (Storage)** | HDFS (Namenode, Datanode) | **Implementado** |
| **Gerenciamento de Recursos** | YARN (ResourceManager, NodeManager) | **Implementado** |
| **Catálogo de Metadados** | Hive Metastore + PostgreSQL | **Implementado** |
| **Acesso SQL** | Hive Server | **Implementado** |
| **Processamento Distribuído** | Apache Spark (Master, Worker) | **Implementado** |
| **Orquestração de Pipeline** | Apache Airflow + MySQL | Implementado (Inativo) |
| **Banco NoSQL (Serving Layer)** | Apache HBase (Master, RegionServer) | Para Implementar |
| **Coordenação** | Apache ZooKeeper | Para Implementar |
| **Camada SQL para NoSQL** | Apache Phoenix | Para Implementar |
| **Visualização de Dados (BI)**| Apache Superset ou Metabase | Para Implementar |

## 🚀 Como Executar o Projeto

1.  **Pré-requisitos:**

      * Docker e Docker Compose instalados.
      * Git para clonar o repositório.

2.  **Configuração:**

      * Clone este repositório: `git clone <URL_DO_SEU_REPOSITÓRIO>`
      * Navegue para a pasta do projeto: `cd <NOME_DA_PASTA>`
      * Certifique-se de que os arquivos de configuração `hadoop.env` e `hive-conf/hive-site.xml` estão presentes e corretos.

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

## ⚡ Exemplos de Uso

### Executar um Job MapReduce (WordCount)

```bash
# Entrar no contêiner do namenode
docker exec -it namenode /bin/bash

# Criar dados de exemplo e submeter o job
hdfs dfs -mkdir -p /test
echo "hello world hello hadoop" > test.txt
hdfs dfs -put test.txt /test
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar wordcount /test /output
hdfs dfs -cat /output/part-r-00000
```

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

-----

*Este projeto é um ambiente de estudos e não se destina ao uso em produção.*