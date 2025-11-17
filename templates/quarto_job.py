# from pyspark.sql import SparkSession


# from pyspark import SparkContext
# from pyspark.sql import SQLContext
# sc = SparkContext(appName="Phoenix test")
# sqlContext = SQLContext(sc)
# table = sqlContext.read.format("org.apache.phoenix.spark").option("table", "TESTE_PHOENIX").option("zkUrl", "zookeeper:2181").load()
# print(table.columns)

# sc.stop()

from pyspark.sql import SparkSession

def main():
    """
    Job PySpark com configuração de JARs e classpath via código,
    para uma execução limpa.
    """
    
    # Caminho para a pasta com TODOS os nossos JARs de dependência dentro do contêiner
    #jars_path = '"/spark/conf/:/opt/spark/jobs/zookeeper-3.5.2-alpha.jar:/opt/spark/jobs/phoenix-spark-4.14.1-HBase-1.2.jar:/opt/spark/jobs/phoenix-4.14.1-HBase-1.2-client.jar"'

    spark = SparkSession.builder \
        .appName("SparkPhoenixViaCodigo") \
        .master("spark://spark-master:7077") \
        .getOrCreate()

    print("--- SparkSession criada com Classpath customizado. Lendo dados... ---")

    df_phoenix = spark.read \
        .format("org.apache.phoenix.spark") \
        .option("table", "TESTE_PHOENIX") \
        .option("zkUrl", "zookeeper:2181") \
        .load()

    print("Dados lidos com sucesso da tabela 'TESTE_PHOENIX':")
    df_phoenix.show()

    spark.stop()
    print("--- Job Concluído ---")

if __name__ == '__main__':
    main()