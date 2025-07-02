import pandas as pd
from datetime import datetime

# Caminhos
bronze_path = 'data/bronze/'
silver_path = 'data/silver/'

# Leitura
df_account = pd.read_csv(bronze_path + 'bronze_core_account.csv')
df_pix = pd.read_csv(bronze_path + 'bronze_core_pix.csv')

# Filtra apenas transações PIX no core_account (pega qualquer variação de PIX)
df_pix_account = df_account[df_account['ds_transaction_type'].str.upper().str.contains('PIX', na=False)].copy()
df_pix_core = df_pix[df_pix['ds_transaction_type'].str.upper().str.contains('PIX', na=False)].copy()

# Identifica PIX que não estão no core_pix pelo id_transaction
df_falhas = df_pix_account[~df_pix_account['id_transaction'].isin(df_pix_core['id_transaction'])].copy()

# Adiciona data de ingestão
df_falhas['dt_ingestion'] = datetime.today().strftime('%Y-%m-%d')

# Salva resultado
df_falhas.to_csv(silver_path + 'silver_pix_falhou_registro.csv', index=False)

print("Arquivo 'silver_pix_falhou_registro.csv' gerado com sucesso!")
print(f"Total de falhas detectadas: {len(df_falhas)}")
