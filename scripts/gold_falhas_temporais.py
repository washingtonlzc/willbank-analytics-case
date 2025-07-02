import pandas as pd
import matplotlib.pyplot as plt

# 1. Carregar as falhas
df = pd.read_csv('data/silver/silver_pix_falhou_registro.csv', parse_dates=['dt_transaction'])

# 2. Extrair hora e dia da semana
df['hora'] = pd.to_datetime(df['dt_transaction']).dt.hour
df['dia_semana'] = pd.to_datetime(df['dt_transaction']).dt.day_name()

# 3. Agrupar por hora
falhas_por_hora = df.groupby('hora').size().reset_index(name='qtd_falhas')
falhas_por_hora.to_csv('data/gold/gold_falhas_por_hora.csv', index=False)

# 4. Agrupar por dia da semana
falhas_por_dia = df.groupby('dia_semana').size().reset_index(name='qtd_falhas')

# Ordenar dias na ordem certa (segunda a domingo)
dias_ordem = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
falhas_por_dia['dia_semana'] = pd.Categorical(falhas_por_dia['dia_semana'], categories=dias_ordem, ordered=True)
falhas_por_dia = falhas_por_dia.sort_values('dia_semana')

falhas_por_dia.to_csv('data/gold/gold_falhas_por_dia.csv', index=False)

# 5. Gerar gráfico por hora
plt.figure(figsize=(10,5))
plt.plot(falhas_por_hora['hora'], falhas_por_hora['qtd_falhas'], marker='o')
plt.title('Falhas PIX por Hora do Dia')
plt.xlabel('Hora do Dia')
plt.ylabel('Quantidade de Falhas')
plt.grid(True)
plt.savefig('deliverables/output/falhas_por_hora.png')
plt.show()

# 6. Gerar gráfico por dia da semana
plt.figure(figsize=(8,5))
plt.bar(falhas_por_dia['dia_semana'], falhas_por_dia['qtd_falhas'])
plt.title('Falhas PIX por Dia da Semana')
plt.xlabel('Dia da Semana')
plt.ylabel('Quantidade de Falhas')
plt.grid(axis='y')
plt.savefig('deliverables/output/falhas_por_dia.png')
plt.show()
