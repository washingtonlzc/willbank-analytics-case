import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Caminhos
silver_path = 'data/silver/'
gold_path = 'data/gold/'

# Leitura da base enriquecida
df = pd.read_csv(silver_path + 'silver_pix_transacoes.csv')

# ====== 1. Distribuição de clientes por UF ======
clientes_por_uf = df.groupby('uf')['surrogate_key'].nunique().reset_index()
clientes_por_uf.columns = ['uf', 'total_clientes']
clientes_por_uf = clientes_por_uf.sort_values('uf')
clientes_por_uf.to_csv(gold_path + 'gold_clientes_por_uf.csv', index=False)

# ====== 2. Distribuição de idade dos clientes ======
df_validos = df.dropna(subset=['birth_date']).copy()
df_validos['birth_date'] = pd.to_datetime(df_validos['birth_date'], errors='coerce')
df_validos['idade'] = df_validos['birth_date'].apply(lambda x: relativedelta(datetime.today(), x).years)

# Estatísticas resumidas de idade
idade_descritiva = df_validos['idade'].describe(percentiles=[.25, .5, .75]).round(1)
idade_descritiva.to_frame(name='valor').to_csv(gold_path + 'gold_estatisticas_idade.csv')

print("KPIs demográficos gerados com sucesso!")
