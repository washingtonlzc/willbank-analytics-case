# Will Bank – Case Técnico: Senior Analytics Engineer

**Candidato:** Washington (Kim)

---

## Objetivo do Case

Este projeto apresenta a solução para o case técnico da vaga de **Senior Analytics Engineer** no Will Bank. O objetivo principal foi desenvolver um **pipeline de dados robusto e escalável em múltiplas camadas** (Raw → Bronze → Silver → Gold), com foco em:

* **Detecção de Inconsistências**: Identificar falhas e inconsistências em transações PIX.
* **Enriquecimento de Dados**: Agregar valor aos dados transacionais com informações demográficas dos clientes.
* **Proposta de Evolução**: Sugerir a ingestão de dados via API externa para enriquecimento contínuo.
* **Visão Estratégica**: Apresentar sugestões técnicas e de negócio que vão além do escopo solicitado, visando a melhoria contínua dos processos de dados.

---

## Estrutura do Projeto

O repositório está organizado de forma a garantir a rastreabilidade, manutenibilidade e clareza do fluxo de dados, desde a origem até a camada de consumo.

```bash
willbank-analytics-case/
│
├── data/
│   ├── raw/                        # Dados fornecidos (core_account, core_pix, customer)
│   │   ├── core_account.csv
│   │   ├── core_pix.csv
│   │   └── customer.csv
│   ├── bronze/                     # Dados com tipos ajustados e padronização
│   │   ├── bronze_core_account.csv
│   │   ├── bronze_core_pix.csv
│   │   └── bronze_customer.csv
│   ├── silver/                     # Dados enriquecidos, cruzamentos e análises
│   │   ├── silver_pix_transacoes.csv
│   │   ├── silver_pix_falhou_registro.csv
│   │   └── silver_inconsistencias.csv
│   └── gold/                       # Dados agregados e métricas finais
│       ├── gold_clientes_por_uf.csv
│       ├── gold_estatisticas_idade.csv
│       ├── gold_falhas_por_uf.csv
│       ├── gold_taxa_sucesso_pix.csv
│       ├── gold_total_pix_por_tipo.csv
│       ├── gold_total_pix_por_uf.csv
│       ├── gold_transacoes_suspeitas.csv
│       ├── gold_transacoes_suspeitas_resumo.txt
│       └── gold_valor_medio_pix_mensal.csv
│
├── scripts/                             # Transformações por camada
│   ├── bronze_transform.py              # Geração dos arquivos Bronze (tipos, ingestão)
│   ├── silver_transform.py              # Join completo entre PIX, account e customer
│   ├── silver_inconsistencias.py        # PIX que não existem em core_account
│   ├── silver_pix_falhou_registro.py    # Transações em core_account que não estão no core_pix
│   ├── gold_kpis.py                     # Geração dos KPIs principais
│   ├── gold_kpis_demografia.py          # Distribuição por idade e por estado
│   └── gold_kpis_estrategicos.py        # Taxa de sucesso, suspeitas e valor médio
│
├── deliverables/                        # Saídas finais (dashboards, gráficos, relatórios)
│   ├── dashboard/                       # Imagens e simulações de dashboards
│   ├── docs/                            # Documentos de apoio
│   └── output/                          # Exportações para apresentação
│
├── requirements.txt                    # Dependências do projeto
└── README.md
````

-----

## Etapas do Pipeline

O pipeline foi construído seguindo a metodologia **Medallion Architecture** para garantir qualidade e governança.

### 1\. Camada Raw

  * **Origem:** `data/raw/`
  * **Descrição:** Contém os dados brutos fornecidos no formato CSV, sem nenhuma modificação.
      * `core_account.csv`
      * `core_pix.csv`
      * `customer.csv`

### 2\. Camada Bronze

  * **Origem:** `data/bronze/`
  * **Script:** `scripts/bronze_transform.py`
  * **Descrição:** Primeira etapa de tratamento e padronização. As principais transformações incluem:
      * Ajuste e conversão de tipos de dados (`datetime`, `float`, `int`).
      * Padronização de nomes de colunas.
      * Criação da coluna `dt_ingestion` para rastreabilidade.
  * **Saídas:**
      * `bronze_core_account.csv`
      * `bronze_core_pix.csv`
      * `bronze_customer.csv`

### 3\. Camada Silver

  * **Origem:** `data/silver/`
  * **Scripts:** `scripts/silver_transform.py`, `scripts/silver_inconsistencias.py`, etc.
  * **Descrição:** Camada de enriquecimento e consolidação, onde os dados são cruzados para gerar insights.
      * **Join Estratégico:** As bases são unificadas na visão PIX → Account → Customer para criar uma tabela analítica central.
      * **Análises de Inconsistência:** Scripts dedicados identificam e isolam anomalias nos dados.
  * **Saídas Principais:**
      * `silver_pix_transacoes.csv`: Tabela consolidada com todas as transações PIX, informações da conta e dados demográficos do cliente.
      * `silver_pix_falhou_registro.csv`: Transações PIX identificadas no `core_account` que não possuem registro correspondente no `core_pix`.
      * `silver_inconsistencias.csv`: Entradas no `core_pix` que não possuem uma conta correspondente em `core_account`, apontando para possíveis problemas de integridade referencial.

### 4\. Camada Gold

  * **Origem:** `data/gold/`
  * **Descrição:** Camada final, projetada para consumo por stakeholders e ferramentas de BI. Contém dados agregados, KPIs e métricas de negócio prontas para análise.
  * **Exemplos de Saídas:**
      * `gold_taxa_sucesso_pix.csv`
      * `gold_falhas_por_uf.csv`
      * `gold_valor_medio_pix_mensal.csv`
      * `gold_transacoes_suspeitas.csv`
      * `gold_estatisticas_idade.csv`
      * `gold_clientes_por_uf.csv`
      * `gold_total_pix_por_tipo.csv`
      * `gold_total_pix_por_uf.csv`
-----

## KPIs e Propostas Estratégicas

Além da construção do pipeline, foram geradas métricas e propostas de valor para o negócio.

### Métricas Implementadas

  * **Volume de Transações com Falha:** Quantificação das transações que falharam no registro.
  * **Identificação de Transações Suspeitas:** Análise de outliers com base em valores monetários (ex: transações com valor muito acima da mediana do cliente ou do sistema).
  * **Enriquecimento Demográfico:** Cruzamento de dados transacionais com idade e estado (UF) do cliente para análises comportamentais.

### Propostas de Melhoria e Análise

1.  **Taxa de Falha por Tipo de Transação:** Calcular a proporção de falhas para cada tipo de chave PIX (CPF, e-mail, celular, aleatória).
2.  **Análise Geográfica e Demográfica:**
      * Distribuição de clientes por estado (UF).
      * Distribuição etária dos clientes (idade média, quartis, histograma).
      * Ranking de UFs com maior taxa de erro em transações PIX.
3.  **Análise Temporal:** Estudo do padrão de falhas ao longo do tempo (por hora, dia da semana) para identificar possíveis gargalos em momentos de pico.
4.  **Monitoramento e Alertas:** Proposta de implementação de um alerta automático (via Slack ou e-mail) caso a taxa de sucesso das transações PIX caia abaixo de um limiar crítico (ex: 98%).
5.  **Visualização de Dados:** Simulação de um dashboard em Power BI ou Metabase para acompanhamento contínuo dos KPIs pela área de negócio (disponível em `deliverables/dashboard/`).

-----

## Sugestões Técnicas e de Governança

Para garantir a evolução e a sustentabilidade da solução, as seguintes melhorias são propostas:

1.  **Ingestão de Dados Externos (NPS):** Planejamento para ingestão de dados de satisfação do cliente (NPS) via API. Isso permitiria correlacionar a experiência do cliente com a performance de produtos como o PIX.
2.  **Governança de Dados:**
      * **Versionamento de Dados:** Implementar o versionamento dos datasets (ex: com DVC) para garantir reprodutibilidade.
      * **Testes de Integridade:** Criar um framework de testes automatizados (ex: Great Expectations) para validar a qualidade dos dados a cada execução do pipeline.
      * **Score de Confiabilidade:** Desenvolver um health score dos dados, que meça a qualidade, atualidade e completude das tabelas críticas.
3.  **Análise de Impacto Financeiro:** Estimar o impacto financeiro das falhas PIX, considerando custos operacionais de suporte e o potencial churn de clientes insatisfeitos.



---
## Status do Projeto

✅ **Pipeline Implementado:** As camadas Raw → Bronze → Silver → Gold estão completas.
✅ **Análises Estratégicas:** KPIs e análises de negócio foram desenvolvidos.
✅ **Pronto para Expansão:** Projeto estruturado para futuras integrações via API e visualização em ferramentas de BI.

---

## Como Executar o Projeto

Para replicar o ambiente e executar o pipeline, siga os passos abaixo:

1.  **Pré-requisitos:** Certifique-se de ter o Python (versão 3.x) e o `pip` instalados em sua máquina.

2.  **Instalar Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Executar o Pipeline:**
    Siga a ordem de execução das camadas para processar os dados:

    * **Camada Bronze:**
        ```bash
        python scripts/bronze_transform.py
        ```
    * **Camada Silver:**
        ```bash
        python scripts/silver_transform.py
        python scripts/silver_inconsistencias.py
        python scripts/silver_pix_falhou_registro.py
        ```
    * **Camada Gold:**
        ```bash
        python scripts/gold_kpis.py
        python scripts/gold_kpis_demografia.py
        python scripts/gold_kpis_estrategicos.py
        ```

    Após a execução, os resultados e as saídas processadas estarão disponíveis nas respectivas pastas (`data/bronze`, `data/silver`, `data/gold`, e `deliverables/output`).
<!-- end list -->

```
```
