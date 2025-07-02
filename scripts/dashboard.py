import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Paleta Will Bank
WILL_ROXO = "#8E4FE0"
WILL_AMARELO = "#FFB800"
WILL_AZUL = "#6DD3FA"
WILL_CINZA = "#F5F5F7"

st.set_page_config(page_title="Will Bank – Painel Gerencial", layout="wide")

# Cabeçalho estilizado Will Bank
st.markdown(
    f"""
    <div style="background:linear-gradient(90deg,{WILL_ROXO} 0%,{WILL_AMARELO} 100%);padding:16px 0 6px 0;border-radius:10px;margin-bottom:20px;">
        <h1 style="color:white;text-align:center;margin-bottom:0;font-family:Arial,sans-serif;">
            Painel Gerencial Will Bank
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Função utilitária para carregar CSV (trata caminho relativo)
def load_csv(path):
    return pd.read_csv(Path(path))

# Sidebar – Seleção rápida
st.sidebar.title("Will Bank – Analytics Case")
st.sidebar.markdown("Desenvolvido por Kim")

menu = st.sidebar.radio("Navegue pelo dashboard", [
    "Visão Geral",
    "KPIs PIX",
    "Falhas e Inconsistências",
    "Demografia dos Clientes",
    "Transações Suspeitas",
    "Propostas & Governança"
])

# --- 1. Visão Geral (Resumo)
if menu == "Visão Geral":
    st.title("📊 Painel Gerencial Will Bank")
    st.markdown("### Pipeline de Dados – Estrutura em Camadas")
    st.image("deliverables/output/falhas_por_dia.png", caption="Exemplo de insight temporal (Falhas PIX por dia)")
    st.info("""
    Este painel resume os principais KPIs extraídos do pipeline e os insights estratégicos para o negócio Will Bank.
    """)

# --- 2. KPIs PIX (Taxa de sucesso/falha)
elif menu == "KPIs PIX":
    st.header("📈 KPIs das Transações PIX")
    taxa_sucesso = load_csv("data/gold/gold_taxa_sucesso_pix_percentual.csv")
    taxa_quantidade = load_csv("data/gold/gold_taxa_sucesso_pix_quantidade.csv")

    st.subheader("Taxa de Sucesso (%)")
    fig = px.pie(
        taxa_sucesso,
        names='status',
        values='percentual',
        hole=0.55,
        color='status',
        color_discrete_map={'Sucesso': WILL_ROXO, 'Falha': WILL_AMARELO}
    )
    fig.update_traces(textinfo='percent+label', pull=[0.01, 0.1], textfont_size=16)
    fig.update_layout(template='simple_white')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Volume de Transações por Status")
    fig2 = px.bar(
        taxa_quantidade,
        x='status', y='quantidade', color='status', text='quantidade',
        color_discrete_map={'Sucesso': WILL_ROXO, 'Falha': WILL_AMARELO}
    )
    fig2.update_traces(marker_line_width=0, textposition='outside')
    fig2.update_layout(template='simple_white', showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

    st.warning("🔔 Proposta: Implementar alerta automático caso a taxa de sucesso caia abaixo de 98%.")

# --- 3. Falhas e Inconsistências
elif menu == "Falhas e Inconsistências":
    st.header("❌ Análise de Falhas e Inconsistências")
    falhas_dia = load_csv("data/gold/gold_falhas_por_dia.csv")
    ranking_uf = load_csv("data/gold/gold_ranking_falhas_por_uf.csv")

    st.subheader("Falhas por Dia da Semana")
    fig = px.bar(
        falhas_dia,
        x='dia_semana', y='qtd_falhas', text='qtd_falhas',
        color_discrete_sequence=[WILL_AMARELO]
    )
    fig.update_traces(marker_line_width=0, textposition='outside')
    fig.update_layout(template='simple_white', showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Ranking de UFs com Mais Falhas")
    fig2 = px.bar(
        ranking_uf,
        x='uf', y='total_falhas', text='total_falhas',
        color_discrete_sequence=[WILL_ROXO]
    )
    fig2.update_traces(marker_line_width=0, textposition='outside')
    fig2.update_layout(template='simple_white', showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

    st.caption("Dica: Investigue segunda/quarta-feira e UFs no topo do ranking para priorização de esforços.")

# --- 4. Demografia dos Clientes
elif menu == "Demografia dos Clientes":
    st.header("🌎 Demografia dos Clientes Will Bank")
    clientes_uf = load_csv("data/gold/gold_clientes_por_uf.csv")
    estat_idade = load_csv("data/gold/gold_estatisticas_idade.csv")
    st.subheader("Distribuição de Clientes por Estado")
    fig = px.bar(
        clientes_uf, x='uf', y='total_clientes', text='total_clientes',
        color_discrete_sequence=[WILL_ROXO]
    )
    fig.update_traces(marker_line_width=0, textposition='outside')
    fig.update_layout(template='simple_white', showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Estatísticas de Idade dos Clientes")
    st.dataframe(estat_idade)
    # Busca os valores pela label do describe
    media = estat_idade.loc[estat_idade['Unnamed: 0'] == 'mean', 'valor'].values[0]
    mediana = estat_idade.loc[estat_idade['Unnamed: 0'] == '50%', 'valor'].values[0]
    q1 = estat_idade.loc[estat_idade['Unnamed: 0'] == '25%', 'valor'].values[0]
    q3 = estat_idade.loc[estat_idade['Unnamed: 0'] == '75%', 'valor'].values[0]

    st.markdown(f"""
    <div style="background-color:{WILL_CINZA};padding:12px 20px;border-radius:8px;margin:12px 0;">
    <b>Média de idade:</b> {media}<br>
    <b>Mediana:</b> {mediana}<br>
    <b>Quartis:</b> {q1} / {q3}
    </div>
    """, unsafe_allow_html=True)

# --- 5. Transações Suspeitas (Outliers)
elif menu == "Transações Suspeitas":
    st.header("🕵️ Transações Suspeitas (Outliers)")
    trans_suspeitas = load_csv("data/gold/gold_transacoes_suspeitas.csv")
    resumo = Path("data/gold/gold_transacoes_suspeitas_resumo.txt")
    st.subheader("Resumo Estatístico dos Outliers")
    if resumo.exists():
        st.text(resumo.read_text())
    st.subheader("Tabela de Transações Suspeitas")
    st.dataframe(trans_suspeitas.head(20))  # Mostra só os 20 primeiros
    st.caption("Outliers identificados automaticamente por análise estatística dos valores.")

# --- 6. Propostas & Governança
elif menu == "Propostas & Governança":
    st.header("🛡️ Propostas Técnicas e de Governança")
    st.markdown(f"""
    - Integração de dados de pesquisa (NPS) via API, enriquecendo o pipeline.<br>
    - Versionamento de dados, testes automatizados e score de confiabilidade.<br>
    - Estimar impacto financeiro das falhas e simular dashboards executivos (ex: Looker, PowerBI).<br>
    - <span style="color:{WILL_ROXO}">(Espaço reservado para evolução futura e feedback do time)</span>
    """, unsafe_allow_html=True)

# --- Footer
st.markdown("---")
st.caption("Projeto Will Bank – Senior Analytics Engineer • Kim (Washington) – 2025")
