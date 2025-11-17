from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def main():
    """
    Terceiro job: Lendo um CSV bruto e salvando como uma tabela Parquet EXTERNA
    em um local customizado.
    """
    spark = SparkSession.builder \
        .appName("ETLClientesParquetExterno") \
        .master("spark://spark-master:7077") \
        .enableHiveSupport() \
        .getOrCreate()

    print("SparkSession criada com sucesso!")

    raw_csv_path = "hdfs://namenode:9000/datalake/raw/clientes/clientes.csv"
    print(f"Lendo dados brutos de: {raw_csv_path}")
    
    df_raw = spark.read.csv(raw_csv_path, header=True, inferSchema=True)

    df_processed = df_raw.withColumnRenamed("id_cliente", "customer_id")


    # 1. Definimos o nome da tabela e o caminho customizado na camada 'processed'
    processed_table_name = "clientes_processados"
    hdfs_processed_path = f"hdfs://namenode:9000/datalake/processed/{processed_table_name}"
    
    
    print(f"Salvando dados processados na tabela Hive '{processed_table_name}' no local: {hdfs_processed_path}")
    
    
    # 2. Usamos .option("path", ...) para especificar o local
    df_processed.write \
        .mode("overwrite") \
        .format("parquet") \
        .option("path", hdfs_processed_path) \
        .saveAsTable(processed_table_name)
    # -----------------------------
    
    print("Tabela externa salva com sucesso em formato Parquet!")

    print("Amostra da nova tabela 'clientes_processados':")
    spark.table(processed_table_name).show(5)

    spark.stop()
    print("Job concluido.")

if __name__ == '__main__':
    main()