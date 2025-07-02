import pandas as pd

# Caminho do arquivo
file_path = 'data/raw/customer.csv'

# Ler CSV
df = pd.read_csv(file_path)

# Mostrar colunas disponíveis
print("Colunas no customer.csv:", df.columns.tolist())

# Mostrar as primeiras linhas para verificar os dados da coluna UF (se existir)
if 'uf' in df.columns:
    print("Primeiras linhas da coluna 'uf':")
    print(df['uf'].head(20))
else:
    print("Coluna 'uf' não encontrada no arquivo customer.csv")
