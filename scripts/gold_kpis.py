import pandas as pd

# Caminho de entrada (Silver) e saída (Gold)
silver_path = 'data/silver/'
gold_path = 'data/gold/'

# Leitura do arquivo consolidado da Silver
df = pd.read_csv(silver_path + 'silver_pix_transacoes.csv')

# 1. Valor médio das transações PIX por mês
df['dt_transaction'] = pd.to_datetime(df['dt_transaction'])
df['mes_ano'] = df['dt_transaction'].dt.to_period('M')
valor_medio_por_mes = df.groupby('mes_ano')['vl_transaction'].mean().reset_index()
valor_medio_por_mes.columns = ['mes_ano', 'vl_medio_pix']

# 2. Total de transações por UF
total_por_uf = df.groupby('uf')['id_transaction'].count().reset_index()
total_por_uf.columns = ['uf', 'total_transacoes_pix']

# 3. Total por tipo de transação
total_por_tipo = df.groupby('ds_transaction_type')['id_transaction'].count().reset_index()
total_por_tipo.columns = ['tipo_transacao', 'total']

# 4. Taxa de sucesso nas transações (percentual)
status_counts_percentual = df['status'].value_counts(normalize=True).reset_index()
status_counts_percentual.columns = ['status', 'percentual']

# 5. Taxa de sucesso nas transações (quantidade absoluta)
status_counts_quantidade = df['status'].value_counts().reset_index()
status_counts_quantidade.columns = ['status', 'quantidade']

# === Salvando outputs individuais da camada Gold ===
valor_medio_por_mes.to_csv(gold_path + 'gold_valor_medio_pix_mensal.csv', index=False)
total_por_uf.to_csv(gold_path + 'gold_total_pix_por_uf.csv', index=False)
total_por_tipo.to_csv(gold_path + 'gold_total_pix_por_tipo.csv', index=False)
status_counts_percentual.to_csv(gold_path + 'gold_taxa_sucesso_pix_percentual.csv', index=False)
status_counts_quantidade.to_csv(gold_path + 'gold_taxa_sucesso_pix_quantidade.csv', index=False)

print("Arquivos Gold gerados com sucesso!")
