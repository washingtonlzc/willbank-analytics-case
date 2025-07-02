import pandas as pd
from datetime import datetime

# Caminhos de leitura e salvamento
bronze_path = 'data/bronze/'
silver_path = 'data/silver/'

# === Leitura dos arquivos Bronze ===
df_pix = pd.read_csv(bronze_path + 'bronze_core_pix.csv')
df_account = pd.read_csv(bronze_path + 'bronze_core_account.csv')
df_customer = pd.read_csv(bronze_path + 'bronze_customer.csv')

# === Join PIX com ACCOUNT via id_transaction ===
pix_account = pd.merge(
    df_pix,
    df_account[['id_transaction', 'surrogate_key']],
    on='id_transaction',
    how='left'
)

# === Join com CUSTOMER via surrogate_key (incluindo birth_date e uf) ===
pix_transacoes = pd.merge(
    pix_account,
    df_customer[['surrogate_key', 'uf', 'birth_date']],  # incluído birth_date
    on='surrogate_key',
    how='left'
)

# === STATUS da transação (Sucesso/Falha) ===
pix_transacoes['status'] = pix_transacoes['surrogate_key'].apply(
    lambda x: 'Sucesso' if pd.notnull(x) else 'Falha'
)

# === Dias entre entrada da conta e transação ===
# Garantir que 'entry_date' exista em df_account e adicionar
if 'entry_date' in df_account.columns:
    pix_transacoes = pd.merge(
        pix_transacoes,
        df_account[['id_transaction', 'entry_date']],
        on='id_transaction',
        how='left'
    )
    pix_transacoes['entry_date'] = pd.to_datetime(pix_transacoes['entry_date'], errors='coerce')
else:
    pix_transacoes['entry_date'] = pd.NaT

pix_transacoes['dt_transaction'] = pd.to_datetime(pix_transacoes['dt_transaction'], errors='coerce')
pix_transacoes['dias_entre_entrada_e_pix'] = (
    pix_transacoes['dt_transaction'] - pix_transacoes['entry_date']
).dt.days

# === Marcar transações suspeitas (valor muito alto) ===
valor_mediano = pix_transacoes['vl_transaction'].median()
pix_transacoes['transacao_suspeita'] = pix_transacoes['vl_transaction'] > (3 * valor_mediano)

# === Adiciona coluna de ingestão ===
pix_transacoes['dt_ingestion'] = datetime.today().strftime('%Y-%m-%d')

# === Salva resultado enriquecido na camada Silver ===
pix_transacoes.to_csv(silver_path + 'silver_pix_transacoes.csv', index=False)

print("Arquivo 'silver_pix_transacoes.csv' enriquecido e salvo com sucesso!")
