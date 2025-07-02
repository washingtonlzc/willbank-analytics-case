import pandas as pd

# Caminhos
silver_path = 'data/silver/'
gold_path = 'data/gold/'

# Leitura da base Silver
df = pd.read_csv(silver_path + 'silver_pix_transacoes.csv')

# Filtra valores válidos
df = df[df['vl_transaction'] > 0].copy()

# 1. Total de transações com falha por UF (excluindo NaN)
falhas_por_uf = (
    df[(df['status'] == 'Falha') & (df['uf'].notna())]
    .groupby('uf')['id_transaction']
    .count()
    .reset_index()
    .rename(columns={'id_transaction': 'total_falhas'})
)
falhas_por_uf.to_csv(gold_path + 'gold_falhas_por_uf.csv', index=False)
print(f"Total de falhas por UF:\n{falhas_por_uf}")

# Métrica extra: falhas sem UF
falhas_sem_uf = df[(df['status'] == 'Falha') & (df['uf'].isna())]
total_falhas_sem_uf = len(falhas_sem_uf)
print(f"Total de falhas sem UF: {total_falhas_sem_uf}")

# 2. Total de transações suspeitas (valores muito altos)
mediana_valor = df['vl_transaction'].median()
limite_suspeito = mediana_valor * 3
transacoes_suspeitas = df[df['vl_transaction'] > limite_suspeito]

# Estatísticas sobre suspeitas
total_suspeitas = len(transacoes_suspeitas)
media_valores_suspeitos = transacoes_suspeitas['vl_transaction'].mean()
max_valor_suspeito = transacoes_suspeitas['vl_transaction'].max()
min_valor_suspeito = transacoes_suspeitas['vl_transaction'].min()

# Exporta tabela de suspeitas e resumo
transacoes_suspeitas.to_csv(gold_path + 'gold_transacoes_suspeitas.csv', index=False)

with open(gold_path + 'gold_transacoes_suspeitas_resumo.txt', 'w') as f:
    f.write(f"Total de transações suspeitas: {total_suspeitas}\n")
    f.write(f"Média dos valores suspeitos: R$ {media_valores_suspeitos:.2f}\n")
    f.write(f"Valor máximo suspeito: R$ {max_valor_suspeito:.2f}\n")
    f.write(f"Valor mínimo suspeito: R$ {min_valor_suspeito:.2f}\n")
    f.write(f"Limite considerado suspeito: R$ {limite_suspeito:.2f}\n")
    f.write(f"Mediana original: R$ {mediana_valor:.2f}\n")

print("KPIs estratégicos gerados com sucesso!")
