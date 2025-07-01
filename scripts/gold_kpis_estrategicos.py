import pandas as pd

# Caminhos
silver_path = 'data/silver/'
gold_path = 'data/gold/'

# Leitura da base Silver
df = pd.read_csv(silver_path + 'silver_pix_transacoes.csv')

# 1. Total de transações com falha por UF
falhas_por_uf = (
    df[df['status'] == 'Falha']
    .groupby('uf')['id_transaction']
    .count()
    .reset_index()
    .rename(columns={'id_transaction': 'total_falhas'})
)
falhas_por_uf.to_csv(gold_path + 'gold_falhas_por_uf.csv', index=False)

# 2. Total de transações suspeitas (valores muito altos)
mediana_valor = df['vl_transaction'].median()
limite_suspeito = mediana_valor * 3
transacoes_suspeitas = df[df['vl_transaction'] > limite_suspeito]

# Estatísticas sobre suspeitas
total_suspeitas = len(transacoes_suspeitas)
media_valores_suspeitos = transacoes_suspeitas['vl_transaction'].mean()

# Exporta tabela de suspeitas e resumo
transacoes_suspeitas.to_csv(gold_path + 'gold_transacoes_suspeitas.csv', index=False)

with open(gold_path + 'gold_transacoes_suspeitas_resumo.txt', 'w') as f:
    f.write(f"Total de transações suspeitas: {total_suspeitas}\n")
    f.write(f"Média dos valores suspeitos: R$ {media_valores_suspeitos:.2f}\n")
    f.write(f"Limite considerado suspeito: R$ {limite_suspeito:.2f}\n")
    f.write(f"Mediana original: R$ {mediana_valor:.2f}\n")

print("KPIs estratégicos gerados com sucesso!")
