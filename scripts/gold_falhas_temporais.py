import pandas as pd
import matplotlib.pyplot as plt

# Caminhos
silver_path = 'data/silver/'
gold_path = 'data/gold/'
output_path = 'deliverables/output/'

# Ler arquivo com UF agregado
df = pd.read_csv(silver_path + 'silver_pix_falhou_registro_com_uf.csv', parse_dates=['dt_transaction'])

# Filtrar falhas que possuem UF
df = df[df['uf'].notna()]

# Extrair dia da semana
df['dia_semana'] = df['dt_transaction'].dt.day_name()

# Agrupar por dia da semana
dias_ordem = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
falhas_por_dia = df.groupby('dia_semana').size().reindex(dias_ordem).reset_index(name='qtd_falhas')
falhas_por_dia.to_csv(gold_path + 'gold_falhas_por_dia.csv', index=False)

# Plotar gráfico falhas por dia
plt.figure(figsize=(8,5))
plt.bar(falhas_por_dia['dia_semana'], falhas_por_dia['qtd_falhas'])
plt.title('Falhas PIX por Dia da Semana')
plt.xlabel('Dia da Semana')
plt.ylabel('Quantidade de Falhas')
plt.grid(axis='y')

# Adiciona valores acima das barras
for i, valor in enumerate(falhas_por_dia['qtd_falhas']):
    plt.text(i, valor + 5, str(valor), ha='center', va='bottom')

plt.savefig(output_path + 'falhas_por_dia.png')
plt.show()

print("KPIs temporais gerados e gráfico de falhas por dia da semana criados com sucesso!")
