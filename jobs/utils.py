import os
import shutil
import filecmp

def setup_hive_connection():
    """
    Localiza a pasta de configuração do PySpark na venv e copia o 
    hive-site.xml, garantindo a conexão com o Hive Metastore.
    """
    print("--- Verificando configuração do Hive Metastore ---")
    
    # Encontra o caminho do pacote pyspark dinamicamente
    try:
        import pyspark
        pyspark_path = os.path.dirname(pyspark.__file__)
    except ImportError:
        print("Erro: PySpark não encontrado. Por favor, instale com 'pip install pyspark'.")
        return

    # Define os caminhos de origem e destino
    source_file = './hive-conf/hive-site.xml'
    dest_dir = os.path.join(pyspark_path, 'conf')
    dest_file = os.path.join(dest_dir, 'hive-site.xml')

    # Verifica se o arquivo de origem existe
    if not os.path.exists(source_file):
        print(f"Aviso: Arquivo de configuração de origem não encontrado em '{source_file}'.")
        print("O Spark pode não conseguir se conectar ao Hive Metastore.")
        return

    # Garante que o diretório de destino exista
    os.makedirs(dest_dir, exist_ok=True)

    # Compara os arquivos e copia apenas se forem diferentes ou se o destino não existir
    should_copy = True
    if os.path.exists(dest_file):
        if filecmp.cmp(source_file, dest_file, shallow=False):
            print("Configuração do hive-site.xml já está atualizada.")
            should_copy = False

    if should_copy:
        print(f"Copiando '{source_file}' para '{dest_dir}'...")
        shutil.copy(source_file, dest_file)
        print("Cópia concluída.")
    
    print("-------------------------------------------------")