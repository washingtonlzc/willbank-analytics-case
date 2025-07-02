import pandas as pd

df = pd.read_csv('data/silver/silver_pix_transacoes.csv')

print("Contagem dos valores na coluna 'status':")
print(df['status'].value_counts())

print("\nContagem dos valores na coluna 'uf' (incluindo nulos):")
print(df['uf'].value_counts(dropna=False))
