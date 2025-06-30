import pandas as pd
from datetime import datetime

# Caminhos
bronze_path = 'data/bronze/'
silver_path = 'data/silver/'

# === Leitura dos arquivos bronze ===
df_pix = pd.read_csv(bronze_path + 'bronze_core_pix.csv')
df_account = pd.read_csv(bronze_path + 'bronze_core_account.csv')

# === Identifica inconsistências ===
# PIX cujo cd_seqlan NÃO existe em core_account
df_inconsistencias = df_pix[~df_pix['cd_seqlan'].isin(df_account['cd_seqlan'])].copy()

# === Adiciona data de ingestão ===
df_inconsistencias['dt_ingestion'] = datetime.today().strftime('%Y-%m-%d')

# === Salva na camada silver ===
df_inconsistencias.to_csv(silver_path + 'silver_inconsistencias.csv', index=False)

print("Arquivo 'silver_inconsistencias.csv' gerado com sucesso!")
