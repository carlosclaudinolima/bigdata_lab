from pyspark.sql import SparkSession


def main():
    
    # 1. Criar a SparkSession, o ponto de entrada para o Spark
    # .master() aponta para nosso Spark Master no Docker
    # .enableHiveSupport() permite que o Spark se comunique com o Hive Metastore
    spark = (
        SparkSession.builder.appName("PrimeiroJobPySpark")
        .master("spark://spark-master:7077")
        .enableHiveSupport()
        .getOrCreate()
    )

    print("SparkSession criada com sucesso!")

    # 2. Definir o caminho para o nosso arquivo no HDFS

    #hdfs_path = "hdfs://namenode:9000/datalake/raw/clientes/clientes.csv"
    hdfs_path = "hdfs://namenode:9000/datalake/raw/clientes/clientes.csv"

    # 3. Ler o arquivo CSV usando o Spark
    #header=True:Usa a primeira linha como cabecalho (nomes das colunas)
    # inferSchema=True: Tenta adivinhar os tipos de dados de cada coluna
    #print(f'Lendo dados de: {hdfs_path}')
    df_clientes = spark.read.csv(hdfs_path, header=True, inferSchema=True)

    # 4. Mostrar o esquema que o Spark inferiu
    print("Esquema inferido pelo Spark:")
    df_clientes.printSchema()

    # 5. Mostrar as 5 primeiras linhas do DataFrame
    print("Amostra dos dados:")
    df_clientes.show(5)

    # 6. Encerrar a sessao
    spark.stop()
    print("Job concluído.")


if __name__ == "__main__":
    main()
