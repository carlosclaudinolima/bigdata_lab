from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# Definição da DAG
with DAG(
    dag_id='dag_de_teste_simples',
    start_date=datetime(2025, 9, 28),
    schedule_interval=None,
    catchup=False,
    tags=['teste'],
) as dag:
    
    # Esta é a única tarefa da DAG.
    # Ela simplesmente executa um comando 'echo' no terminal.
    tarefa_de_teste = BashOperator(
        task_id='tarefa_de_teste',
        bash_command='echo ">>> A DAG de teste executou com sucesso em $(date)!"',
    )