import pandas as pd

# Caminhos
silver_path = 'data/silver/'
gold_path = 'data/gold/'

# Leitura do arquivo que contém as falhas reais
df_falhas = pd.read_csv(silver_path + 'silver_pix_falhou_registro.csv')

# Filtra falhas que possuem UF
df_falhas_com_uf = df_falhas[df_falhas['uf'].notna()]

# Agrupa por UF e conta total de falhas
falhas_por_uf = (
    df_falhas_com_uf.groupby('uf')['id_transaction']
    .count()
    .reset_index()
    .rename(columns={'id_transaction': 'total_falhas'})
)
falhas_por_uf.to_csv(gold_path + 'gold_falhas_por_uf.csv', index=False)
print(f"Total de falhas por UF:\n{falhas_por_uf}")

# Métrica extra: falhas sem UF
total_falhas_sem_uf = df_falhas['uf'].isna().sum()
print(f"Total de falhas sem UF: {total_falhas_sem_uf}")

# Leitura da base completa para transações suspeitas
df = pd.read_csv(silver_path + 'silver_pix_transacoes.csv')

# Filtra transações suspeitas (valores muito altos)
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
