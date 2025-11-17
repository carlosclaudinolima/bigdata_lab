from pyspark.sql import SparkSession

def main():
    spark = (
        SparkSession.builder.appName("ProcessarAluraCursos")
        .master("spark://spark-master:7077")
        .enableHiveSupport()
        .getOrCreate()
    )    
    print("SparkSession criada com sucesso!")
    
    # Extract
    raw_parquet_path = "hdfs://namenode:9000/datalake/raw/alura_cursos/"
    df_raw = spark.read.parquet(raw_parquet_path)
    print('Dados extraídos com sucesso!')
    
    # Transform    
    df_processed = df_raw.withColumnRenamed("slug", "pasta_curso")
    print('Dados Trsnaformados com sucesso!')
    
    # Load
    # 1. Definimos o nome da tabela e o caminho customizado na camada 'processed'
    processed_table_name = "alura_cursos_processados"
    hdfs_processed_path = f"hdfs://namenode:9000/datalake/processed/{processed_table_name}"
    # -----------------------------
    
    print(f"Salvando dados processados na tabela Hive '{processed_table_name}' no local: {hdfs_processed_path}")
    # 2. Usamos .option("path", ...) para especificar o local
    df_processed.write \
        .mode("overwrite") \
        .format("parquet") \
        .option("path", hdfs_processed_path) \
        .saveAsTable(processed_table_name)
    # -----------------------------
    
    print("Tabela externa salva com sucesso em formato Parquet e catalogada no Hive")

    print("Amostra da nova tabela 'clientes_processados':")
    spark.table(processed_table_name).show(5)

    spark.stop()
    print("Job concluido.")
    

if __name__ == "__main__":
    main()