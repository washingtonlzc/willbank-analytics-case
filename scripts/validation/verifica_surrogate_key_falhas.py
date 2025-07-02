import pandas as pd

# Carrega o arquivo das falhas
df_falhas = pd.read_csv('data/silver/silver_pix_falhou_registro.csv')

# Total de falhas
print(f"Total de falhas: {len(df_falhas)}")

# Quantidade de surrogate_key nulo (ausente) nas falhas
print(f"Quantidade de surrogate_key nulo nas falhas: {df_falhas['surrogate_key'].isna().sum()}")

# Exemplos de surrogate_key presentes (não nulos) nas falhas - mostra até 10
print("Exemplos de surrogate_key nas falhas:")
print(df_falhas['surrogate_key'].dropna().unique()[:10])
