import pandas as pd

silver_path = 'data/silver/'
gold_path = 'data/gold/'

df = pd.read_csv(silver_path + 'silver_pix_falhou_registro.csv')

# Filtra falhas com UF preenchida
df_falhas_com_uf = df[df['uf'].notna()]

# Agrupa por UF e conta falhas
falhas_por_uf = df_falhas_com_uf.groupby('uf').size().reset_index(name='total_falhas')

print(falhas_por_uf)

# Salva para gold
falhas_por_uf.to_csv(gold_path + 'gold_falhas_por_uf.csv', index=False)
