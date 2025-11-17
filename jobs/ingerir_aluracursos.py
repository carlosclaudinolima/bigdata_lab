import requests
from pyspark.sql import SparkSession

def main():
    spark = (
        SparkSession.builder.appName("IngerirAluraCursos")
        .master("spark://spark-master:7077")
        .enableHiveSupport()
        .getOrCreate()
    )
    print("SparkSession criada com sucesso!")

    # --- ETAPA DE INGESTÃO (Roda só no Driver) ---
    print("Buscando dados da API da Alura...")
    response = requests.get("https://www.alura.com.br/api/cursos")
    dados_json = response.json() 
    
    # ---------------------------------------------
    # --- ETAPA DE PROCESSAMENTO (Distribuído) ---
    # 1. O Driver paraleliza os dados (o JSON) para os Executors
    rdd = spark.sparkContext.parallelize(dados_json)

    # 2. Converte para DataFrame
    df = spark.createDataFrame(rdd)

    print("Dados ingeridos e paralelizados:")
    df.show()

    # 3. Salva no HDFS (na camada raw)
    df.write.mode("overwrite").format("parquet").save("hdfs://namenode:9000/datalake/raw/alura_cursos")

    spark.stop()

if __name__ == "__main__":
    main()