# Will Bank – Case Técnico: Senior Analytics Engineer

**Autor:** Washington Campos

## Sumário

- [Objetivo do Case](#objetivo-do-case)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Arquitetura do Pipeline](#arquitetura-da-pipeline)
- [Como Executar o Projeto](#como-executar-o-projeto)
- [Principais Métricas e KPIs](#principais-métricas-kpis)
- [Exemplo de Análise Exploratória (EDA)](#exemplo-de-análise-exploratória-eda)
- [Plano de Integração de Dados Externos (NPS)](#plano-de-integracao-de-dados-externos-nps)
- [Sugestões de Governança e Melhoria](#sugestoes-tecnicas-e-de-governanca)
- [Status do Projeto](#status-do-projeto)

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
├── assets/will-bank.svg                            # Logo em svg do will para o (figma e dashboard)
├── data/
│   ├── raw/                                        # Dados originais fornecidos (core_account, core_pix, customer)
│   │   ├── core_account.csv
│   │   ├── core_pix.csv
│   │   └── customer.csv
│   ├── bronze/                                     # Dados tratados e padronizados
│   │   ├── bronze_core_account.csv
│   │   ├── bronze_core_pix.csv
│   │   └── bronze_customer.csv
│   ├── silver/                                     # Dados enriquecidos, cruzamentos e análises intermediárias
│   │   ├── silver_inconsistencias.csv
│   │   ├── silver_pix_falhou_registro.csv
│   │   ├── silver_pix_falhou_registro_com_uf.csv
│   │   └── silver_pix_transacoes.csv 
│   └── gold/                                       # Dados agregados e KPIs finais (camada Gold do pipeline)
│       ├── gold_clientes_por_uf.csv                # Quantidade de clientes por estado (UF)
│       ├── gold_estatisticas_idade.csv             # Estatísticas descritivas da idade dos clientes (média, mediana, quartis)
│       ├── gold_falhas_por_dia.csv                 # Volume de falhas em transações PIX por dia da semana
│       ├── gold_falhas_por_hora.csv                # Volume de falhas em transações PIX por hora do dia
│       ├── gold_falhas_por_uf.csv                  # Total de falhas em transações PIX por estado (UF)
│       ├── gold_longevidade_primeiro_pix.csv       # Tempo (em dias) entre a abertura da conta e o primeiro PIX de cada cliente
│       ├── gold_longevidade_primeiro_pix_resumo.txt # Estatísticas-resumo sobre a longevidade até o primeiro PIX
│       ├── gold_ranking_falhas_por_uf.csv          # Ranking dos estados (UF) com mais falhas em transações PIX
│       ├── gold_taxa_sucesso_pix_percentual.csv    # Percentual de sucesso/falha nas transações PIX
│       ├── gold_taxa_sucesso_pix_quantidade.csv    # Quantidade absoluta de transações PIX por status (sucesso/falha)
│       ├── gold_total_pix_por_tipo.csv             # Volume de transações PIX por tipo de chave (CPF, e-mail, celular, aleatória)
│       ├── gold_total_pix_por_uf.csv               # Total de transações PIX por estado (UF)
│       ├── gold_transacoes_suspeitas.csv           # Lista detalhada das transações PIX suspeitas (outliers)
│       ├── gold_transacoes_suspeitas_resumo.txt    # Resumo estatístico das transações suspeitas (outliers)
│       ├── gold_valor_medio_pix_mensal.csv         # Valor médio mensal das transações PIX
│
├── deliverables/                                   # Resultados finais e artefatos para apresentação
│   ├── dashboard/                                  # Imagens e links de dashboards
│   │   ├── link_para_o_dashboard_online.md         # Links do prototipo de dashboard no Looker
│   │   └── figma_link.md                           # Links do prototipo de dashboard no Figma
│   ├── docs/                                       # Documentos auxiliares e suporte
│   └── output/                                     # Gráficos, relatórios e imagens exportadas
│       ├── falhas_por_dia.png
│       └── ranking_falhas_por_uf.png
│
├── scripts/                                     # Scripts organizados por camada do pipeline
│   ├── validation/                              # Scripts auxiliares para validação e testes dos dados
│   │   ├── testa_falhas_por_uf.py               # Gera o total de falhas PIX por UF (estado) a partir da silver, salvando para a gold (gold_falhas_por_uf.csv)
│   │   ├── verifica_surrogate_key_cliente.py    # Valida se todos os surrogate_key presentes nas falhas existem na base de clientes (bronze_customer.csv)
│   │   ├── verifica_surrogate_key_falhas.py     # Mostra quantos surrogate_key estão ausentes ou presentes nas falhas (silver_pix_falhou_registro.csv)
│   │   ├── verifica_uf_falhas.py                # Checa a presença de valores nulos e não nulos na coluna 'uf' das falhas de PIX (silver)
│   │   └── verifica_uf_nos_bronze.py            # Mostra e examina a presença da coluna 'uf' e exemplos nos arquivos bronze (account, pix, customer)
│   │
│   ├── bronze_transform.py                      # Tratamento inicial e padronização (Bronze)
│   ├── silver_transform.py                      # Enriquecimento e união de dados (Silver)
│   ├── silver_inconsistencias.py                # Detecção de inconsistências na camada Silver
│   ├── silver_pix_falhou_registro.py            # Identificação de falhas em registros PIX (Silver)
│   ├── gold_kpis.py                             # Geração dos principais KPIs (Gold)
│   ├── gold_kpis_demografia.py                  # KPIs demográficos (idade, UF) (Gold)
│   ├── gold_kpis_estrategicos.py                # KPIs estratégicos (falhas, suspeitas) (Gold)
│   ├── gold_falhas_temporais.py                 # Análise temporal de falhas (Gold)
│   ├── gold_ranking_falhas_por_uf.py            # Ranking de falhas por UF (Gold)
│   └── run_pipeline.py                          # Scripts que executa de uma só vez toda pipeline
│
├── requirements.txt                             # Dependências Python do projeto
├── README.md                                    # Documentação principal do projeto
└── .gitignore                                   # Configurações para Git

````

-----

## Arquitetura do Pipeline

O pipeline foi construído em Python, com análise e documentação em Jupyter Notebook, visualização dos dados em Streamlit e um protótipo básico de dashboard no Figma, para ilustrar a visão final do produto. Todos os scripts foram separados por camadas (Bronze, Silver, Gold), seguindo a metodologia **Medallion Architecture** e boas praticas de engenharia de dados para garantir qualidade e governança.

### Notas sobre a Implementação e SQL

Como os dados disponibilizados para o case estão em formato CSV e não em um banco de dados real, optei por utilizar o Pandas para realizar as transformações e análises localmente. O Pandas permite simular praticamente todos os comandos SQL clássicos, como SELECT, JOIN e GROUP BY, então consigo aplicar as regras do pipeline sem perder nenhuma funcionalidade.

Para garantir o que foi solicitado, incluí exemplos de como cada etapa poderia ser feita em SQL, seja nos comentários dos scripts ou no README do projeto, deixando claro que todo o processo pode ser facilmente adaptado para qualquer engine SQL em um ambiente de Data Lake real.

## Exemplo de Transformação Silver

```sql
-- Exemplo conceitual da transformação Silver: Unificando PIX, Account e Customer
-- Equivalente à lógica do silver_transform.py

SELECT
    p.id_end_to_end,
    p.dt_transaction,
    p.vl_transaction,
    p.ds_transaction_type AS pix_transaction_type,
    ca.cd_account_customer,
    c.full_name,
    c.birth_date,
    c.uf,
    CASE
        WHEN c.surrogate_key IS NOT NULL THEN 'Sucesso'
        ELSE 'Falha'
    END AS status_transacao,
    -- Outras colunas e cálculos, como idade e transacao_suspeita,
    -- seriam adicionados aqui ou em etapas posteriores.
    CURRENT_DATE AS dt_ingestion -- Data de ingestão para rastreabilidade
FROM
    bronze_core_pix p
LEFT JOIN
    bronze_core_account ca ON p.cd_seqlan = ca.cd_seqlan
LEFT JOIN
    bronze_customer c ON ca.surrogate_key = c.surrogate_key;
```

### Detecção de Inconsistência

* **Contexto:** PIX em Account que falhou no Core PIX
* **Equivalente à lógica do:** `silver_pix_falhou_registro.py`

```sql
-- Exemplo conceitual da detecção de inconsistência: PIX em Account que falhou no Core PIX
-- Equivalente à lógica do silver_pix_falhou_registro.py

SELECT
    a.id_transaction,
    a.dt_transaction,
    a.cd_account_customer,
    a.vl_transaction
FROM
    bronze_core_account a
WHERE
    a.ds_transaction_type = 'PIX'
    AND NOT EXISTS (
        SELECT 1
        FROM bronze_core_pix p
        WHERE p.cd_seqlan = a.cd_seqlan
    );
```


### Camadas da PipeLine
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

## 📊 Dashboard Gerencial (Streamlit & Figma)

O projeto conta com um dashboard interativo desenvolvido em Streamlit (**veja instruções abaixo para rodar localmente**) e um protótipo visual de dashboard criado no Figma para ilustrar como seria a entrega final para o negócio.

- [Link para o protótipo no Figma](https://www.figma.com/design/kCj4qhSlHDMhnOVmoZo7Un/Willbank-Dashboard-Case?node-id=0-1&t=J9Df221xte2GYwCR-1) 

**Principais características:**
- Visualização dinâmica dos KPIs PIX (taxa de sucesso/falha, volume por status)
- Análise temporal de falhas (por dia da semana e ranking de UFs)
- Distribuição demográfica dos clientes (UF e idade)
- Detecção de outliers (transações suspeitas)
- Propostas de evolução e governança, integradas à visão estratégica do case
- **Cores e layout seguem a identidade visual do Will Bank (amarelo, preto, branco)**

**Como executar:**

```bash
pip install streamlit plotly pandas
streamlit run scripts/dashboard.py
```
-----


### Principais Métricas e Insights Gerados

A partir do pipeline estruturado até a camada Gold, foram extraídas as seguintes métricas e análises, proporcionando uma visão abrangente do negócio e subsidiando a tomada de decisão. Além disso, foram geradas propostas de valor e melhoria contínua:

* **KPIs de Desempenho e Qualidade do PIX:**
    * 📈 **Taxa de Sucesso das Transações PIX:** Percentual e volume absoluto de transações bem-sucedidas.
    * ❌ **Taxa de Falha/Inconsistência PIX:** Quantificação de transações que falharam no registro ou apresentaram inconsistências.
    * 🕵️ **Transações Suspeitas (Outliers):** Identificação de anomalias com base em valores monetários.
    * 💰 **Valor Médio Mensal das Transações PIX.**
    * **Proposta de Alerta Automático:** Implementação de alertas para queda da taxa de sucesso abaixo de um limiar crítico (ex: 98%).

* **Insights Demográficos e Geográficos:**
    * 🌎 **Distribuição de Clientes por UF:** Visualização da base de clientes por estado.
    * 👵 **Distribuição Etária dos Clientes:** Estatísticas descritivas (média, mediana, quartis) da idade dos clientes.
    * 🏆 **Ranking de UFs com Mais Erros:** Identificação dos estados com maior taxa de falhas em transações PIX.
    * **Longevidade até o Primeiro PIX:** Tempo médio entre abertura da conta e primeira transação PIX, com análise de engajamento inicial.

* **Análises Comportamentais e Temporais:**
    * **Volume de Transações PIX por Tipo de Chave:** Análise da distribuição por CPF, e-mail, celular e aleatória.
    * ⏰ **Falhas por Dia/Hora:** Estudo do padrão de falhas ao longo do tempo (por dia da semana e hora do dia) para identificar gargalos.

* **Visualização e Consumo:**
    * **Dashboards Interativos:** Desenvolvimento de protótipos de dashboards em Figma e Streamlit para acompanhamento contínuo dos KPIs pela área de negócio.
    * **Enriquecimento Demográfico:** Cruzamento de dados transacionais com idade e estado (UF) para análises comportamentais detalhadas.

*Detalhes completos de algumas métricas e análises estão disponíveis em:*
`data/gold/gold_longevidade_primeiro_pix.csv`
`data/gold/gold_longevidade_primeiro_pix_resumo.txt`
`data/gold/gold_taxa_sucesso_pix_percentual.csv`
`data/gold/gold_taxa_sucesso_pix_quantidade.csv`
... (e adicione outros relevantes)


## Longevidade até o Primeiro PIX

Foi calculado o tempo (em dias) entre a data de abertura da conta e a data da primeira transação PIX de cada cliente.  
Esse indicador mede o engajamento inicial do cliente com o PIX e pode indicar oportunidades para campanhas de ativação, educação ou melhorias no onboarding.

- **Média de dias até o 1º PIX:** 27 dias  
- **Mediana:** 36 dias  
- **Quartis:** 25% (-21), 75% (86)  
- **Mínimo:** -207 dias (possível erro de cadastro ou retroalimentação do sistema)  
- **Máximo:** 177 dias

> Valores negativos sugerem inconsistências cadastrais ou processos retroativos de registro, recomendando revisão nos sistemas de origem.

*Detalhes completos disponíveis em:*  
`data/gold/gold_longevidade_primeiro_pix.csv`  
`data/gold/gold_longevidade_primeiro_pix_resumo.txt`
...


## Taxa de Sucesso nas Transações PIX

Para melhor compreensão e análise do desempenho das transações PIX, foram gerados dois arquivos distintos contendo informações complementares sobre o status das transações:

- **`gold_taxa_sucesso_pix_percentual.csv`**  
  Contém a distribuição percentual das transações categorizadas por status (por exemplo, "Sucesso" e "Falha").  
  Este arquivo ajuda a entender a proporção relativa de transações bem-sucedidas versus as que apresentaram falhas, facilitando a análise do desempenho global do sistema.

- **`gold_taxa_sucesso_pix_quantidade.csv`**  
  Apresenta o número absoluto de transações para cada categoria de status.  
  Esta informação é crucial para contextualizar o percentual, pois revela o volume real de transações em cada categoria, permitindo avaliar a significância estatística das métricas apresentadas.


Esses insights permitem à equipe técnica priorizar esforços e prever janelas de maior risco, reforçando a robustez do pipeline implementado.

## Exemplo de Análise Exploratória (EDA)

Antes do desenvolvimento completo do pipeline, foi realizada uma análise exploratória dos dados (EDA) para identificar padrões, avaliar a qualidade e levantar possíveis inconsistências.  
O notebook completo da EDA, com gráficos e insights, pode ser consultado em [`scripts/eda_willbank.ipynb`](scripts/eda_willbank.ipynb).

-----

## Sugestões de Governança e Melhoria

Para garantir a evolução e a sustentabilidade da solução, as seguintes melhorias são propostas:

### 1. Plano de Integração de Dados Externos (NPS)

Para integrar os dados da pesquisa de satisfação do cliente (NPS) fornecidos via API externa, conforme solicitado, propõe-se o seguinte plano de ação detalhado em tópicos, alinhado à arquitetura Medallion:

* **1.1. Origem e Frequência:**
    * **Origem:** Dados de NPS disponibilizados mensalmente por um fornecedor externo via API.
    * **Frequência:** Ingestão agendada para ocorrer uma vez ao mês, após a disponibilização dos dados pela API.

* **1.2. Camada Bronze (Ingestão e Armazenamento Bruto):**
    * **Mecanismo de Ingestão:** Desenvolvimento de um script Python dedicado (e.g., `scripts/nps_ingest.py`) que se conectaria à API externa. Este script seria responsável por:
        * Gerenciar a autenticação e autorização junto à API (ex: uso de chaves API ou tokens).
        * Realizar requisições HTTP para coletar os dados da pesquisa.
        * Implementar mecanismos de re-tentativa e tratamento de erros de conexão/resposta da API.
    * **Formato de Armazenamento:** Os dados brutos da API (provavelmente em JSON) seriam salvos "as-is" (como recebidos) em formato Parquet ou CSV na pasta `data/bronze/nps/`.
    * **Metadados e Rastreabilidade:** Adicionar colunas de metadados como `dt_ingestion` (data da coleta), `api_version` (se aplicável), e `process_id` para garantir a auditabilidade e reprocessamento, se necessário.

* **1.3. Camada Silver (Tratamento e Enriquecimento):**
    * **Mecanismo de Transformação:** Um script Python (e.g., `scripts/silver_nps_transform.py`) seria desenvolvido para:
        * **Normalização:** Padronizar nomes de colunas, ajustar tipos de dados (e.g., datas, scores numéricos) e garantir a consistência dos valores.
        * **Tratamento de Qualidade:** Lidar com valores nulos ou inconsistentes (ex: preenchimento, remoção ou sinalização).
        * **Deduplicação:** Garantir a unicidade dos registros de NPS para evitar contagens duplas em análises.
        * **Enriquecimento:** Realizar um `JOIN` com os dados de `customer` (da `bronze_customer.csv` ou `silver_customer.csv` se já existisse uma específica) utilizando o `surrogate_key` do cliente. Isso agregaria informações demográficas (idade, UF, etc.) às respostas de NPS, permitindo análises contextuais.
    * **Saída:** A tabela `silver_nps_data.csv` (ou Parquet) seria salva na pasta `data/silver/nps/`, contendo os dados de NPS limpos e enriquecidos.

* **1.4. Camada Gold (Consumo e KPIs):**
    * **Mecanismo de Agregação:** Scripts Python (e.g., `scripts/gold_nps_kpis.py`) seriam criados para gerar métricas e cubos de negócio a partir da `silver_nps_data.csv`.
    * **Exemplos de KPIs e Análises:**
        * NPS médio por mês, por região (UF) e por faixa etária.
        * Correlação entre o NPS e a taxa de sucesso de transações PIX (cruzando com `gold_taxa_sucesso_pix.csv`).
        * Identificação de segmentos de clientes com baixo NPS para ações de melhoria.
        * Visualização das tendências de NPS ao longo do tempo.
    * **Saída:** Arquivos sumarizados (e.g., `gold_nps_mensal.csv`, `gold_nps_por_uf.csv`) seriam salvos na pasta `data/gold/`.

* **1.5. Considerações Adicionais para Robustez:**
    * **Idempotência:** Projetar o processo para que múltiplas execuções do script de ingestão (dentro de um mesmo período mensal) não resultem em duplicação de dados, seja por verificação de chaves ou estratégia de "upsert".
    * **Observabilidade:** Implementar logging detalhado para monitorar a execução, erros da API e volumes de dados.
    * **Alertas:** Configurar alertas (e.g., via e-mail ou Slack) para falhas na ingestão ou anomalias nos dados de NPS (ex: queda abrupta do score).
    * **Versionamento:** Garantir que o código da ingestão e as definições das tabelas sejam versionados no Git, e considerar o uso de ferramentas como DVC para versionar os próprios datasets de NPS.

---

## Status do Projeto

✅ **Pipeline Implementado:** As camadas Raw → Bronze → Silver → Gold estão completas.
✅ **Análises Estratégicas:** KPIs e análises de negócio foram desenvolvidos.
✅ **Pronto para Expansão:** Projeto estruturado para futuras integrações via API e visualização em ferramentas de BI.

---

## Como Executar o Projeto

1.  **Pré-requisitos:** Certifique-se de ter o Python (versão 3.x) e o `pip` instalados em sua máquina.

2.  **Instalar Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Executar o Pipeline completo:**
    ```bash
    python scripts/run_pipeline.py
    ```
    Esse script executa automaticamente todos os passos das camadas Bronze, Silver e Gold na ordem correta, gerando todos os arquivos processados.

4.  **(Opcional) Executar o Pipeline por Etapa:**
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
        python scripts/gold_falhas_temporais.py
        python scripts/gold_ranking_falhas_por_uf.py
        python scripts/gold_longevidade_primeiro_pix.py
        ```
 5. **(Opcional) Rodar o Dashboard:**
        Para visualizar os principais KPIs e análises do projeto, execute:
        ```bash
        streamlit run scripts/dashboard.py
        ```

    Após a execução, os resultados e as saídas processadas estarão disponíveis nas respectivas pastas (`data/bronze`, `data/silver`, `data/gold`, e `deliverables/output`).
---
## Observações Finais
* O projeto busca refletir práticas reais de engenharia de dados em larga escala.
* Foi construído para ser simples de testar, manter e escalar.
* Todos os scripts estão separados por camada e responsabilidade.
* Aberto a sugestões e discussões para evoluir a solução e contribuir com o time Will Bank!
