from hdfs import InsecureClient
import pandas as pd
import io
import matplotlib.pyplot as plt
import seaborn as sns

client = InsecureClient('http://localhost:9870', user='root')

print(client.list('/'))

# Caminho do arquivo no HDFS
file_path = '/datalake/raw/egressos/egressos.csv'

print(f"Lendo arquivo: {file_path}")

# 2. Lê o arquivo e carrega no Pandas
# O 'encoding' é importante para transformar os bytes em string para o Pandas
with client.read(file_path, encoding='utf-8') as reader:
    df = pd.read_csv(reader)


"""# 1.  Exploração"""

df.info()

df.isnull().sum()

df['Profissão'].unique()

"""#2.   Limpeza e Normalização de dados com Python

## Valores ausentes - Removendo Nulos/NaN
"""

df_cleaned = df.dropna()
print(df_cleaned.head())

"""## Renomeando colunas"""

df_cleaned.rename(columns={'Nome':'nome', 'Profissão': 'profissao', 'Data liberdade': 'dt_liberdade', 'Anos Reclusão': 'anos_reclusao', 'Anos sem trabalho na profissão': 'anos_fora_oficio'}, inplace=True)

""" ## Convertendo campo"""

df_cleaned.loc[:, 'dt_liberdade'] = pd.to_datetime(df_cleaned['dt_liberdade'])
print(df_cleaned.head())

"""## Normalizando Profissão"""

from numpy._core.defchararray import lower
import unicodedata

def normnalizar_texto(texto: str):
    # 1. Normaliza para NFD (separa letra do acento)
    # 2. Codifica para ASCII ignorando erros (os acentos soltos somem)
    # 3. Decodifica de volta para string
    # 4. Converte para minúsculo
    # 5. Remove espaços à esquerda e direita
    return unicodedata.normalize('NFD', texto)\
           .encode('ascii', 'ignore')\
           .decode('utf-8')\
           .lower().lstrip().rstrip()

df_cleaned.loc[:, 'profissao'] = df_cleaned.loc[:, 'profissao'].apply(normnalizar_texto)
print(df_cleaned.head())

"""#3. Estatística Descritiva"""

df_cleaned.describe()


plt.figure(figsize=(10, 6))
sns.histplot(df_cleaned['anos_reclusao'], color='blue', label='Anos Reclusão', kde=True, alpha=0.5)
sns.histplot(df_cleaned['anos_fora_oficio'], color='red', label='Anos sem trabalho na profissão', kde=True, alpha=0.5)
plt.title('Comparação da Frequência de Anos de Reclusão e Anos sem Trabalho na Profissão')
plt.xlabel('Anos')
plt.ylabel('Frequência')
plt.legend()
plt.grid(axis='y', alpha=0.75)
plt.show()

"""#4. Análise de correlação e associação"""

correlation = df_cleaned['anos_reclusao'].corr(df_cleaned['anos_fora_oficio'])
print(f"A correlação entre 'Anos Reclusão' e 'Anos sem trabalho na profissão' é: {correlation:.2f}")


plt.figure(figsize=(10, 6))
sns.scatterplot(x='anos_reclusao', y='anos_fora_oficio', data=df_cleaned, s=100, alpha=0.7)
sns.regplot(x='anos_reclusao', y='anos_fora_oficio', data=df_cleaned, scatter=False, color='red', line_kws={'linestyle': '--'})
plt.title('Gráfico de Dispersão: Anos de Reclusão vs. Anos sem Trabalho na Profissão')
plt.xlabel('Anos de Reclusão')
plt.ylabel('Anos sem Trabalho na Profissão')
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

"""Este gráfico de dispersão mostra a relação entre 'Anos de Reclusão' e 'Anos sem Trabalho na Profissão'. A linha tracejada vermelha é uma linha de regressão, que visualmente representa a tendência da correlação entre as duas variáveis. Quanto mais próximos os pontos estiverem dessa linha e quanto mais a linha se inclinar (positiva ou negativamente), mais forte será a correlação."""

