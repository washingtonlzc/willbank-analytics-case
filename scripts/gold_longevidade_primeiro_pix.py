import pandas as pd

# Carregar bases
df_pix = pd.read_csv('data/bronze/bronze_core_pix.csv', parse_dates=['dt_transaction'])
df_account = pd.read_csv('data/bronze/bronze_core_account.csv', parse_dates=['dt_transaction'])
df_customers = pd.read_csv('data/bronze/bronze_customer.csv', parse_dates=['entry_date'])

# Join PIX → Account para trazer o surrogate_key do cliente
df_pix_account = pd.merge(df_pix, df_account[['cd_seqlan', 'surrogate_key', 'dt_transaction']], on='cd_seqlan', how='left', suffixes=('_pix', '_account'))

# Pega a PRIMEIRA transação PIX de cada cliente (surrogate_key)
pix_primeiro = (
    df_pix_account.sort_values('dt_transaction_pix')
    .groupby('surrogate_key', as_index=False)
    .first()
)

# Join com cadastro do cliente
df = pd.merge(pix_primeiro, df_customers, left_on='surrogate_key', right_on='surrogate_key', how='left')

# Calcula diferença em dias
df['dias_ate_primeiro_pix'] = (df['dt_transaction_pix'] - df['entry_date']).dt.days

# Salva resultado
df[['surrogate_key', 'full_name', 'entry_date', 'dt_transaction_pix', 'dias_ate_primeiro_pix']].to_csv(
    'data/gold/gold_longevidade_primeiro_pix.csv', index=False
)

# Estatísticas resumo
desc = df['dias_ate_primeiro_pix'].describe()
print("Resumo estatístico:")
print(desc)

with open('data/gold/gold_longevidade_primeiro_pix_resumo.txt', 'w') as f:
    f.write(str(desc))
