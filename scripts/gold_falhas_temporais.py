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

# --------- Falhas por Dia da Semana ---------
df['dia_semana'] = df['dt_transaction'].dt.day_name()
dias_ordem = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
falhas_por_dia = df.groupby('dia_semana').size().reindex(dias_ordem).reset_index(name='qtd_falhas')
falhas_por_dia.to_csv(gold_path + 'gold_falhas_por_dia.csv', index=False)

# Gráfico de falhas por dia da semana
plt.figure(figsize=(8,5))
plt.bar(falhas_por_dia['dia_semana'], falhas_por_dia['qtd_falhas'])
plt.title('Falhas PIX por Dia da Semana')
plt.xlabel('Dia da Semana')
plt.ylabel('Quantidade de Falhas')
plt.grid(axis='y')
for i, valor in enumerate(falhas_por_dia['qtd_falhas']):
    plt.text(i, valor + 5, str(valor), ha='center', va='bottom')
plt.savefig(output_path + 'falhas_por_dia.png')
plt.show()

# --------- Falhas por Hora do Dia ---------
df['hora'] = df['dt_transaction'].dt.hour
falhas_por_hora = df.groupby('hora').size().reindex(range(24), fill_value=0).reset_index(name='qtd_falhas')
falhas_por_hora.to_csv(gold_path + 'gold_falhas_por_hora.csv', index=False)

# Gráfico de falhas por hora do dia
plt.figure(figsize=(10,5))
plt.bar(falhas_por_hora['hora'], falhas_por_hora['qtd_falhas'])
plt.title('Falhas PIX por Hora do Dia')
plt.xlabel('Hora do Dia')
plt.ylabel('Quantidade de Falhas')
plt.xticks(range(24))
plt.grid(axis='y')
for i, valor in enumerate(falhas_por_hora['qtd_falhas']):
    plt.text(i, valor + 5, str(valor), ha='center', va='bottom', fontsize=8)
plt.savefig(output_path + 'falhas_por_hora.png')
plt.show()

print("KPIs temporais gerados: falhas por dia da semana e por hora do dia!")
