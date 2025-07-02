import pandas as pd

df = pd.read_csv('data/silver/silver_pix_falhou_registro.csv')

print(f"Total de linhas: {len(df)}")
print(f"Total de valores não nulos na coluna 'uf': {df['uf'].notna().sum()}")
print(f"Total de valores nulos na coluna 'uf': {df['uf'].isna().sum()}")

# Mostrar as primeiras linhas com uf preenchido
print("Exemplos de linhas com UF preenchido:")
print(df[df['uf'].notna()].head())
