import pandas as pd

bronze_path = 'data/bronze/'

# Leitura dos arquivos bronze
df_account = pd.read_csv(bronze_path + 'bronze_core_account.csv')
df_pix = pd.read_csv(bronze_path + 'bronze_core_pix.csv')
df_customer = pd.read_csv(bronze_path + 'bronze_customer.csv')

print("Colunas bronze_core_account.csv:")
print(df_account.columns.tolist())
print("\nExemplo linhas (contas):")
cols_account = ['id_transaction', 'surrogate_key', 'uf']
cols_account = [c for c in cols_account if c in df_account.columns]
print(df_account[cols_account].head(20))

print("\nColunas bronze_core_pix.csv:")
print(df_pix.columns.tolist())
print("\nExemplo linhas (transações PIX):")
cols_pix = ['id_transaction', 'ds_transaction_type']
cols_pix = [c for c in cols_pix if c in df_pix.columns]
print(df_pix[cols_pix].head(20))

print("\nColunas bronze_customer.csv:")
print(df_customer.columns.tolist())
print("\nExemplo linhas (clientes):")
cols_customer = ['surrogate_key', 'uf']
cols_customer = [c for c in cols_customer if c in df_customer.columns]
print(df_customer[cols_customer].head(20))

# Verificando se há transações de falha no account e se uf está preenchido nelas
falhas_account = df_account[df_account['ds_transaction_type'] == 'PIX'].copy()
print(f"\nTotal de transações PIX no account: {len(falhas_account)}")

if 'uf' in falhas_account.columns:
    print("Exemplos de transações PIX no account (uf):")
    print(falhas_account[['id_transaction', 'uf']].head(20))
else:
    print("Coluna 'uf' NÃO existe no arquivo bronze_core_account.csv")

