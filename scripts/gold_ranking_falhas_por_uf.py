import pandas as pd
import matplotlib.pyplot as plt

# Caminhos
gold_path = 'data/gold/'
output_path = 'deliverables/output/'

# Leitura do arquivo com falhas por UF
df = pd.read_csv(gold_path + 'gold_falhas_por_uf.csv')

# Ordenar decrescente pelo total de falhas
df_ranked = df.sort_values('total_falhas', ascending=False)

# Salvar ranking ordenado
df_ranked.to_csv(gold_path + 'gold_ranking_falhas_por_uf.csv', index=False)

# Gerar gráfico de barras do ranking
plt.figure(figsize=(10,6))
plt.bar(df_ranked['uf'], df_ranked['total_falhas'])
plt.title('Ranking de UFs com Mais Falhas em Transações PIX')
plt.xlabel('UF')
plt.ylabel('Total de Falhas')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f'{output_path}ranking_falhas_por_uf.png')
plt.show()

print("Ranking de falhas por UF gerado e salvo com sucesso!")
