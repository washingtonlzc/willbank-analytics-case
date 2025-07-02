import pandas as pd

# Carregar os dados
df_falhas = pd.read_csv('data/silver/silver_pix_falhou_registro.csv')
df_customer = pd.read_csv('data/bronze/bronze_customer.csv')

# Pega os surrogate_key das falhas
surrogate_keys_falhas = df_falhas['surrogate_key'].unique()

# Pega os surrogate_key dos clientes
surrogate_keys_clientes = df_customer['surrogate_key'].unique()

# Quantos surrogate_key das falhas existem na base de clientes?
existem = [key for key in surrogate_keys_falhas if key in surrogate_keys_clientes]
nao_existem = [key for key in surrogate_keys_falhas if key not in surrogate_keys_clientes]

print(f"Total de surrogate_key nas falhas: {len(surrogate_keys_falhas)}")
print(f"Quantos surrogate_key das falhas existem no cliente: {len(existem)}")
print(f"Quantos surrogate_key das falhas NÃO existem no cliente: {len(nao_existem)}")
print(f"Exemplos que NÃO existem no cliente (até 10): {nao_existem[:10]}")
