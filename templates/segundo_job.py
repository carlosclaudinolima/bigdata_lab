from utils import setup_hive_connection
from pyspark.sql import SparkSession


def main():
    
    """
    Segundo job PySpark, lendo dados através do catálogo do Hive.
    """
    # Lê os hostnames das variáveis de ambiente.
    # Se a variável não for encontrada, usa 'localhost' como padrão.
    # spark_master_host = os.getenv("SPARK_MASTER_HOST", "localhost")
    # metastore_host = os.getenv("METASTORE_HOST", "localhost")
    # namenode_host = os.getenv("NAMENODE_HOST", "localhost")

    # spark = SparkSession.builder \
    #     .appName("JobFlexivel") \
    #     .master(f"spark://{spark_master_host}:7077") \
    #     .config("hive.metastore.uris", f"thrift://{metastore_host}:9083") \
    #     .config("spark.sql.warehouse.dir", f"hdfs://{namenode_host}:9000/user/hive/warehouse") \
    #     .enableHiveSupport() \
    #     .getOrCreate() 
        
    
    # A linha .enableHiveSupport() é crucial aqui!
    spark = SparkSession.builder \
        .appName("SegundoJobPySparkHive") \
        .master("spark://spark-master:7077") \
        .enableHiveSupport() \
        .getOrCreate()

    print("SparkSession criada com sucesso!")

    # --- MUDANÇA PRINCIPAL AQUI ---
    # 2. Em vez de ler o CSV diretamente, vamos ler a TABELA do Hive.
    table_name = "clientes"
    print(f"Lendo dados da tabela Hive: {table_name}")
    df_clientes = spark.table(table_name)
    # -----------------------------

    # 3. Mostrar o esquema que o Spark obteve do Hive Metastore
    print("Esquema obtido do Hive Metastore:")
    df_clientes.printSchema()

    # 4. Mostrar as 5 primeiras linhas do DataFrame
    print("Amostra dos dados:")
    df_clientes.show(5)

    # 5. Encerrar a sessão
    spark.stop()
    print("Job concluído.")

if __name__ == '__main__':
    main()