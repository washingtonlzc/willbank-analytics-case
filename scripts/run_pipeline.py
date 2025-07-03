import os

# ========================
#   Will Bank – Pipeline Automática
#   Autor: Washington (Kim)
# ========================

# ========================
# 1. CAMADA BRONZE
# ========================
print('\n[BRONZE] Iniciando processamento dos dados brutos...')
# Padroniza, limpa e prepara os CSVs originais
os.system("python scripts/bronze_transform.py")

# ========================
# 2. CAMADA SILVER
# ========================
print('\n[SILVER] Enriquecendo dados e detectando inconsistências...')

# Une tabelas bronze e cria tabela consolidada de transações PIX enriquecida com dados de cliente
os.system("python scripts/silver_transform.py")

# Detecta possíveis inconsistências entre as tabelas (integridade referencial)
os.system("python scripts/silver_inconsistencias.py")

# Identifica transações PIX no Account que não existem no Core PIX
os.system("python scripts/silver_pix_falhou_registro.py")

# ========================
# 3. CAMADA GOLD
# ========================
print('\n[GOLD] Gerando KPIs, análises avançadas e agregações...')

# Principais KPIs das transações PIX (sucesso, falha, total, etc)
os.system("python scripts/gold_kpis.py")

# KPIs demográficos: análise de idade e estado dos clientes
os.system("python scripts/gold_kpis_demografia.py")

# Métricas estratégicas, detecção de outliers e análises especiais
os.system("python scripts/gold_kpis_estrategicos.py")

# Análise temporal das falhas PIX (por dia da semana, hora, etc)
os.system("python scripts/gold_falhas_temporais.py")

# Ranking dos estados (UF) com mais falhas em transações PIX
os.system("python scripts/gold_ranking_falhas_por_uf.py")

# script avançado da primeira transação Pix do Cliente de - longevidade do primeiro PIX
os.system("python scripts/gold_longevidade_primeiro_pix.py")

print('\n--- Pipeline completa! Todas as camadas processadas com sucesso! ---\n')
