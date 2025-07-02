import pandas as pd

# Carrega o arquivo
df = pd.read_csv('data/silver/silver_pix_transacoes.csv')

# Imprime todas as colunas
print("Colunas no silver_pix_transacoes.csv:", df.columns.tolist())

# Se quiser, imprima as primeiras linhas para ver os dados
print(df.head())
