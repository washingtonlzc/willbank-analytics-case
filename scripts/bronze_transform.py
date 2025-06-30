import pandas as pd
from datetime import datetime

# Caminhos de leitura (raw) e salvamento (bronze)
raw_path = 'data/raw/'
bronze_path = 'data/bronze/'

# === Leitura dos arquivos ===
df_account = pd.read_csv(raw_path + 'core_account.csv')
df_pix = pd.read_csv(raw_path + 'core_pix.csv')
df_customer = pd.read_csv(raw_path + 'customer.csv')

# === Conversão de tipos ===
df_account['dt_transaction'] = pd.to_datetime(df_account['dt_transaction'], errors='coerce')
df_account['dt_month'] = pd.to_datetime(df_account['dt_month'], errors='coerce')
df_account['vl_transaction'] = pd.to_numeric(df_account['vl_transaction'], errors='coerce')

df_pix['dt_transaction'] = pd.to_datetime(df_pix['dt_transaction'], errors='coerce')
df_pix['dt_month'] = pd.to_datetime(df_pix['dt_month'], errors='coerce')
df_pix['vl_transaction'] = pd.to_numeric(df_pix['vl_transaction'], errors='coerce')

df_customer['entry_date'] = pd.to_datetime(df_customer['entry_date'], errors='coerce')
df_customer['birth_date'] = pd.to_datetime(df_customer['birth_date'], errors='coerce')

# === Adiciona coluna de ingestão ===
ingestion_date = datetime.today().strftime('%Y-%m-%d')
df_account['dt_ingestion'] = ingestion_date
df_pix['dt_ingestion'] = ingestion_date
df_customer['dt_ingestion'] = ingestion_date

# === Salva os arquivos na camada Bronze ===
df_account.to_csv(bronze_path + 'bronze_core_account.csv', index=False)
df_pix.to_csv(bronze_path + 'bronze_core_pix.csv', index=False)
df_customer.to_csv(bronze_path + 'bronze_customer.csv', index=False)

print("Dados Bronze salvos com sucesso!")
