import pandas as pd

# Carregar o arquivo silver_pix_transacoes.csv
df = pd.read_csv('data/silver/silver_pix_transacoes.csv')

# Mostrar as primeiras linhas do DataFrame
print("Colunas disponíveis:", df.columns.tolist())

# Filtrar as linhas com status 'Falha'
df_falhas = df[df['status'] == 'Falha']

# Mostrar algumas linhas das falhas para verificar a coluna 'uf'
print(df_falhas[['status', 'uf']].head(20))

# Contar quantas falhas possuem uf preenchido e quantas estão vazias/nulas
print("Quantidade de falhas com UF preenchido:", df_falhas['uf'].notna().sum())
print("Quantidade de falhas com UF vazio ou nulo:", df_falhas['uf'].isna().sum())
