import pandas as pd
from datetime import datetime

# Caminhos
silver_path = 'data/silver/'
gold_path = 'data/gold/'

# Leitura da base enriquecida
df = pd.read_csv(silver_path + 'silver_pix_transacoes.csv')

# ====== 1. Distribuição de clientes por UF ======
clientes_por_uf = df.groupby('uf')['surrogate_key'].nunique().reset_index()
clientes_por_uf.columns = ['uf', 'total_clientes']
clientes_por_uf.to_csv(gold_path + 'gold_clientes_por_uf.csv', index=False)

# ====== 2. Distribuição de idade dos clientes ======
# Calcula idade a partir de birth_date
df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce')
df['idade'] = datetime.today().year - df['birth_date'].dt.year

# Estatísticas resumidas de idade
idade_descritiva = df['idade'].describe(percentiles=[.25, .5, .75]).round(1)
idade_descritiva.to_frame(name='valor').to_csv(gold_path + 'gold_estatisticas_idade.csv')

print("KPIs demográficos gerados com sucesso!")
