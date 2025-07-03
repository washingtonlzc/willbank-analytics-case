import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Paleta Will Bank
WILL_ROXO = "#8E4FE0"
WILL_AMARELO = "#FED300"
WILL_AZUL = "#6DD3FA"
WILL_CINZA = "#F4F5FE"

# Função utilitária para formatar valores em R$ no padrão brasileiro
def formatar_brl(valor):
    if valor is None:
        return ""
    if isinstance(valor, int):
        valor = float(valor)
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


st.set_page_config(page_title="Will Bank – Painel Gerencial", layout="wide")

# Cabeçalho estilizado Will Bank (fundo amarelo, nome preto)
st.markdown(
    """
    <div style="background-color:#FED300;padding:24px 0 12px 0;border-radius:16px;margin-bottom:32px;">
        <h1 style="color:#111;text-align:center;margin-bottom:0;font-size:2.3rem;font-family:Arial,sans-serif;font-weight:700;letter-spacing:-1px;">
            Painel Gerencial Will Bank
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>
    /* Borda preta da bolinha (sempre) */
    div[role="radiogroup"] > label > div:first-child {
        border: 3px solid #111 !important;
        width: 22px !important;
        height: 22px !important;
        margin-right: 10px;
        background: #FFF !important;
        display: flex; align-items: center; justify-content: center;
    }
    /* Centro AMARELO quando ativo - cobre diferentes seletores internos */
    div[role="radiogroup"] > label[aria-checked="true"] > div:first-child > div,
    div[role="radiogroup"] > label[aria-checked="true"] > div:first-child > svg {
        background: #FED300 !important;
        box-shadow: 0 0 0 1px #111;
        border-radius: 50%;
        width: 12px !important;
        height: 12px !important;
        margin: 0 auto;
        /* remove SVG fill se houver */
        fill: #FED300 !important;
    }
    /* Garante também cor de fill caso seja SVG */
    div[role="radiogroup"] > label[aria-checked="true"] svg > circle {
        fill: #FED300 !important;
    }
    /* Centro BRANCO quando inativo */
    div[role="radiogroup"] > label[aria-checked="false"] > div:first-child > div,
    div[role="radiogroup"] > label[aria-checked="false"] > div:first-child > svg {
        background: #FFF !important;
        box-shadow: 0 0 0 1px #111;
        border-radius: 50%;
        width: 12px !important;
        height: 12px !important;
        margin: 0 auto;
        fill: #FFF !important;
    }
    div[role="radiogroup"] > label[aria-checked="false"] svg > circle {
        fill: #FFF !important;
    }
    </style>
""", unsafe_allow_html=True)


# Função utilitária para carregar CSV (trata caminho relativo)
def load_csv(path):
    return pd.read_csv(Path(path))


# Importações já existentes
import streamlit as st
from pathlib import Path

# Caminho da logo
logo_path = Path("assets/will-bank.svg")

st.sidebar.image(str(logo_path), width=150)

# Sidebar – Seleção rápida
st.sidebar.title("Analytics Case")
st.sidebar.markdown("Desenvolvido por Washington")

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
    st.title("Painel Gerencial Will Bank")

    st.markdown("### Pipeline de Dados – Estrutura em Camadas")
    
    st.markdown("""
        <div style="display:flex;justify-content:center;gap:38px;margin-bottom:38px;">
        <div style="background:#000;border-radius:16px;padding:12px 40px 10px 40px;box-shadow:0 1px 6px #0001;text-align:center;min-width:220px;max-width:260px;">
            <div style="font-weight:800;font-size:1.10em;color:#fff;">RAW</div>
            <div style="color:#fff;font-size:0.96em;margin-top:3px;">Dados Brutos</div>
        </div>
        <div style="align-self:center;font-size:2.5em;">→</div>
        <div style="background:#6E4D25;border-radius:16px;padding:12px 40px 10px 40px;box-shadow:0 1px 6px #0001;text-align:center;min-width:220px;max-width:260px;">
            <div style="font-weight:800;font-size:1.10em;color:#fff;">BRONZE</div>
            <div style="color:#fff;font-size:0.96em;margin-top:3px;">Dados Ingeridos e Validados</div>
        </div>
        <div style="align-self:center;font-size:2.5em;">→</div>
        <div style="background:#F0F2F6;border-radius:16px;padding:12px 40px 10px 40px;box-shadow:0 1px 6px #0001;text-align:center;min-width:220px;max-width:260px;">
            <div style="font-weight:800;font-size:1.10em;color:#111;">SILVER</div>
            <div style="color:#000;font-size:0.96em;margin-top:3px;">Dados Integrados e Tratados</div>
        </div>
        <div style="align-self:center;font-size:2.5em;">→</div>
        <div style="background:#FED300;border-radius:16px;padding:12px 40px 10px 40px;box-shadow:0 1px 6px #0001;text-align:center;min-width:220px;max-width:260px;">
            <div style="font-weight:800;font-size:1.10em;color:#000;">GOLD</div>
            <div style="color:#000;font-size:0.96em;margin-top:3px;">Métricas, KPIs e Relatórios</div>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### Resumo de Metricas")
    
    # Cards KPI - EXEMPLO DE VALORES (troque pelos seus dados reais)
    total_pix = 1250000
    taxa_sucesso = 97.8
    clientes_unicos = 95000
    valor_total = 258000000.00

    st.markdown(f"""
    <div style="display:flex;justify-content:center;gap:24px;margin-bottom:30px;">
        <div style="background:#fff;color:#000;padding:24px 40px;border-radius:15px;min-width:180px;max-width:220px;box-shadow:0 1px 6px #0001;text-align:center;">
            <div style="font-weight:700;font-size:1.6em;">{total_pix:,}</div>
            <div style="font-size:1.05em;margin-top:6px;">Transações PIX Processadas</div>
        </div>
        <div style="background:#fff;color:#000;padding:24px 40px;border-radius:15px;min-width:180px;max-width:220px;box-shadow:0 1px 6px #0001;text-align:center;">
            <div style="font-weight:700;font-size:1.6em;">{taxa_sucesso:.1f}%</div>
            <div style="font-size:1.05em;margin-top:6px;">Taxa de Sucesso das Transações PIX</div>
        </div>
        <div style="background:#fff;color:#000;padding:24px 40px;border-radius:15px;min-width:180px;max-width:220px;box-shadow:0 1px 6px #0001;text-align:center;">
            <div style="font-weight:700;font-size:1.6em;">{clientes_unicos:,}</div>
            <div style="font-size:1.05em;margin-top:6px;">Clientes Únicos com Transações PIX</div>
        </div>
        <div style="background:#fff;color:#000;padding:24px 40px;border-radius:15px;min-width:180px;max-width:220px;box-shadow:0 1px 6px #0001;text-align:center;">
            <div style="font-weight:700;font-size:1.6em;">{formatar_brl(valor_total)}</div>
            <div style="font-size:1.05em;margin-top:6px;">Valor Total Movimentado via PIX</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="text-align:center; font-size:1.05em; color:#333; max-width:720px; margin-left:auto; margin-right:auto;">
    Este painel apresenta um resumo dos dados PIX processados pelo Will Bank, exibindo os principais indicadores operacionais e financeiros do período analisado.  
    As métricas selecionadas refletem a performance e a abrangência do uso do PIX, facilitando o acompanhamento estratégico e a tomada de decisão.
    </p>
    """, unsafe_allow_html=True)



# --- 2. KPIs PIX (Taxa de sucesso/falha)
elif menu == "KPIs PIX":
    st.header("📈 KPIs das Transações PIX")
    
    st.markdown("""
    <div style="margin-bottom:14px;font-size:1.07em;color:#444;">
    <b>Sobre os KPIs:</b>  
    Os gráficos abaixo apresentam a taxa de sucesso e o volume de transações PIX processadas pelo Will Bank no período analisado, permitindo monitorar rapidamente a performance operacional e identificar possíveis gargalos.
    </div>
    """, unsafe_allow_html=True)

    taxa_sucesso = load_csv("data/gold/gold_taxa_sucesso_pix_percentual.csv")
    taxa_quantidade = load_csv("data/gold/gold_taxa_sucesso_pix_quantidade.csv")

    st.subheader("Taxa de Sucesso (%)")
    st.markdown("""
    <div style="margin-bottom:12px;font-size:1.05em;color:#444;">
    <b>Legenda:</b><br>
    <span style="color:#FED300;font-weight:600;">■</span> <b>Sucesso</b>: Transações PIX concluídas com êxito.<br>
    <span style="color:#000;font-weight:600;">■</span> <b>Falha</b>: Transações PIX que apresentaram erro ou não foram processadas.
    </div>
    """, unsafe_allow_html=True)
    fig = px.pie(
        taxa_sucesso,
        names='status',
        values='percentual',
        hole=0.55,
        color='status',
        color_discrete_map={
            'Sucesso': '#FED300',   # Amarelo Will
            'Falha': '#000'         # Preto Will (ou outro tom leve)
        }
    )
    fig.update_traces(textinfo='percent+label', pull=[0.01, 0.1], textfont_size=16)
    fig.update_layout(template='simple_white', plot_bgcolor='#FFF', paper_bgcolor='#FFF', legend=dict(font=dict(color="#222")))
    st.plotly_chart(fig, use_container_width=True)
    

    st.subheader("Volume de Transações por Status")
    st.markdown("""
    <div style="margin-bottom:12px;font-size:1.05em;color:#444;">
    <b>Descrição:</b><br>
    O gráfico abaixo exibe o volume total de transações PIX processadas pelo Will Bank, categorizando-as conforme o status da operação (sucesso ou falha). As cores evidenciam rapidamente a predominância de transações bem-sucedidas.<br>
    Cada barra representa um status diferente, permitindo visualizar rapidamente o volume total de operações que foram bem-sucedidas ou falharam.<br>
    As cores seguem o padrão visual do painel:<br>
    <span style="color:#FED300;font-weight:600;">■</span> <b>Sucesso</b> &nbsp;&nbsp;
    <span style="color:#FFA600;font-weight:600;">■</span> <b>Falha</b> &nbsp;&nbsp;
    </div>
    """, unsafe_allow_html=True)

    STATUS_COLORS = {
        'Sucesso': '#FED300',     # Amarelo Will
        'Falha':   '#FFA600',     # Laranja Will
    }
    taxa_quantidade['cor'] = taxa_quantidade['status'].map(STATUS_COLORS).fillna('#222222')

    fig2 = px.bar(
        taxa_quantidade,
        x='status', y='quantidade', color='cor', text='quantidade',
        color_discrete_map='identity'
    )
    fig2.update_traces(marker_line_width=0, textposition='outside')
    fig2.update_layout(
        template='simple_white',
        plot_bgcolor='#FFF',
        paper_bgcolor='#FFF',
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.warning("🔔 Proposta: Implementar alerta automático caso a taxa de sucesso caia abaixo de 98%.")


# --- 3. Falhas e Inconsistências
elif menu == "Falhas e Inconsistências":
    st.header("❌ Análise de Falhas e Inconsistências")
    falhas_dia = load_csv("data/gold/gold_falhas_por_dia.csv")
    ranking_uf = load_csv("data/gold/gold_ranking_falhas_por_uf.csv")
    
    # Tradução dos dias da semana para português
    dias_traducao = {
        'Monday': 'Segunda-feira',
        'Tuesday': 'Terça-feira',
        'Wednesday': 'Quarta-feira',
        'Thursday': 'Quinta-feira',
        'Friday': 'Sexta-feira',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }
    falhas_dia['dia_semana'] = falhas_dia['dia_semana'].map(dias_traducao)

    dias_ordem = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
    falhas_dia['dia_semana'] = pd.Categorical(falhas_dia['dia_semana'], categories=dias_ordem, ordered=True)
    falhas_dia = falhas_dia.sort_values('dia_semana')

    # Garante todos os dias presentes e zera as ausências
    falhas_dia = falhas_dia.set_index('dia_semana').reindex(dias_ordem).reset_index()
    falhas_dia['qtd_falhas'] = falhas_dia['qtd_falhas'].fillna(0)

    # Cores para cada barra
    CORES_PADRAO = ['#FED300', '#FFA600', '#6DD3FA', '#222222']
    COR_VAZIA = '#D3D3D3'

    def cor_barras(row, idx):
        if row['qtd_falhas'] == 0:
            return COR_VAZIA
        else:
            return CORES_PADRAO[idx % len(CORES_PADRAO)]
    falhas_dia['cor'] = [cor_barras(row, i) for i, row in falhas_dia.iterrows()]

    # A PARTIR DAQUI segue normal pro gráfico, sem set_index/reindex novamente!




    st.subheader("Falhas por Dia da Semana")
    st.markdown("""
    <div style="margin-bottom:10px;font-size:1.05em;color:#444;">
    <b>Descrição:</b><br>
    O gráfico abaixo exibe a quantidade de transações PIX que apresentaram falha, agrupadas por dia da semana.  
    Essa visualização ajuda a identificar padrões temporais e possíveis gargalos operacionais em determinados dias, facilitando o direcionamento de ações para mitigar falhas em períodos críticos.
    </div>
    """, unsafe_allow_html=True)
    

    
    # Lista de cores (gira, se tiver mais de 4 dias, repete a ordem)
    CORES_PADRAO = ['#FED300', '#FFA600', '#6DD3FA', '#222222']
    COR_VAZIA = '#D3D3D3'  # cinza claro (vazio)

    def cor_barras(row, idx):
        if pd.isna(row['qtd_falhas']) or row['qtd_falhas'] == 0:
            return COR_VAZIA
        else:
            return CORES_PADRAO[idx % len(CORES_PADRAO)]

    falhas_dia['cor'] = [cor_barras(row, i) for i, row in falhas_dia.iterrows()]

    
    fig = px.bar(
    falhas_dia,
    x='dia_semana', y='qtd_falhas', text='qtd_falhas',
    color='cor', color_discrete_map='identity', category_orders={'dia_semana': dias_ordem}
    )
    fig.update_traces(marker_line_width=0, textposition='outside')
    fig.update_layout(template='simple_white', plot_bgcolor='#FFF', paper_bgcolor='#FFF', showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div style="font-size:1.03em;">
    <b>Legenda das cores:</b><br>
    <span style="color:#FED300;font-weight:600;">&#9632;</span> Maior quantidade<br>
    <span style="color:#6DD3FA;font-weight:600;">&#9632;</span> menor<br>
    <span style="color:#D3D3D3;font-weight:600;">&#9632;</span> Nenhuma falha.
    </div>
    """, unsafe_allow_html=True)


    st.subheader("Ranking de UFs com Mais Falhas")
    st.markdown("""
    <div style="margin-bottom:10px;font-size:1.05em;color:#444;">
    <b>Descrição:</b><br>
    O gráfico apresenta o ranking dos estados brasileiros (UFs) com maior número de transações PIX falhas no período analisado.  
    Essa análise permite priorizar esforços em regiões com maiores índices de inconsistências, contribuindo para a melhoria da experiência do cliente e a estabilidade dos serviços.
    </div>
    """, unsafe_allow_html=True)

    # Top 1 UF = amarelo, Top 2 = laranja, Top 3 = azul, demais = preto
    ranking_uf = ranking_uf.sort_values('total_falhas', ascending=False).reset_index(drop=True)
    top1_uf = ranking_uf.iloc[0]['uf']
    top2_uf = ranking_uf.iloc[1]['uf'] if len(ranking_uf) > 1 else None
    top3_uf = ranking_uf.iloc[2]['uf'] if len(ranking_uf) > 2 else None
    def cor_ranking(uf):
        if uf == top1_uf:
            return '#FED300'
        elif uf == top2_uf:
            return '#FFA600'
        elif top3_uf and uf == top3_uf:
            return '#6DD3FA'
        else:
            return '#222222'
    ranking_uf['cor'] = ranking_uf['uf'].apply(cor_ranking)
    fig2 = px.bar(
        ranking_uf,
        x='uf', y='total_falhas', text='total_falhas',
        color='cor', color_discrete_map='identity'
    )
    fig2.update_traces(marker_line_width=0, textposition='outside')
    fig2.update_layout(template='simple_white', plot_bgcolor='#FFF', paper_bgcolor='#FFF', showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

    st.caption("Dica: Investigue segunda/quarta-feira e UFs no topo do ranking para priorização de esforços.")



# --- 4. Demografia dos Clientes
elif menu == "Demografia dos Clientes":
    st.header("🌎 Demografia dos Clientes Will Bank")
    clientes_uf = load_csv("data/gold/gold_clientes_por_uf.csv")
    estat_idade = load_csv("data/gold/gold_estatisticas_idade.csv")
    st.subheader("Distribuição de Clientes por Estado")
    
    st.markdown("""
    <div style="margin-bottom:10px;font-size:1.05em;color:#444;">
    <b>Descrição:</b><br>
    O gráfico abaixo apresenta a distribuição dos clientes do Will Bank por estado (UF), considerando apenas aqueles que realizaram transações PIX no período analisado.<br>
    Essa visualização permite identificar rapidamente as regiões com maior concentração de clientes ativos no PIX, facilitando o direcionamento de estratégias comerciais e a identificação de oportunidades ou desequilíbrios regionais.
    </div>
    """, unsafe_allow_html=True)

    # Ordena ranking real
    clientes_uf = clientes_uf.sort_values('total_clientes', ascending=False).reset_index(drop=True)
    top1_uf = clientes_uf.iloc[0]['uf']
    top2_uf = clientes_uf.iloc[1]['uf']
    top3_uf = clientes_uf.iloc[2]['uf'] if len(clientes_uf) > 2 else None

    def cor_uf(uf):
        if uf == top1_uf:
            return '#FED300'   # Top 1 amarelo
        elif uf == top2_uf:
            return '#FFA600'   # Top 2 laranja
        elif top3_uf is not None and uf == top3_uf:
            return '#6DD3FA'   # Top 3 azul
        else:
            return '#222222'   # Preto

    clientes_uf['cor'] = clientes_uf['uf'].apply(cor_uf)

    fig = px.bar(
        clientes_uf,
        x='uf',
        y='total_clientes',
        text='total_clientes',
        color='cor',
        color_discrete_map='identity'
    )
    fig.update_traces(marker_line_width=0, textposition='outside')
    fig.update_layout(template='simple_white', plot_bgcolor='#FFF', paper_bgcolor='#FFF', showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # Legenda dinâmica: mostra azul só se houver top 3
    if top3_uf is not None:
        st.markdown(
            """
            <div style="font-size:1.03em;">
            <b>Legenda das cores:</b><br>
            <span style="color:#FED300;font-weight:600;">&#9632;</span> Estado com mais clientes (Top 1)<br>
            <span style="color:#FFA600;font-weight:600;">&#9632;</span> Segundo estado com mais clientes (Top 2)<br>
            <span style="color:#6DD3FA;font-weight:600;">&#9632;</span> Terceiro estado com mais clientes (Top 3)<br>
            <span style="color:#222;font-weight:600;">&#9632;</span> Demais estados
            </div>
            """, unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="font-size:1.03em;">
            <b>Legenda das cores:</b><br>
            <span style="color:#FED300;font-weight:600;">&#9632;</span> Estado com mais clientes (Top 1)<br>
            <span style="color:#FFA600;font-weight:600;">&#9632;</span> Segundo estado com mais clientes (Top 2)<br>
            <span style="color:#222;font-weight:600;">&#9632;</span> Demais estados
            </div>
            """, unsafe_allow_html=True
        )

    # Estatísticas de Idade dos Clientes (mantém igual)
    st.subheader("Estatísticas de Idade dos Clientes")
    st.markdown("""
    <div style="margin-bottom:10px;font-size:1.05em;color:#444;">
    <b>Descrição:</b><br>
    Os indicadores abaixo apresentam estatísticas descritivas do perfil etário dos clientes Will Bank que realizaram ao menos uma transação PIX no período analisado.<br>
    São exibidos a média, mediana, quartis e os valores mínimo e máximo das idades, permitindo entender a distribuição e a concentração etária dos clientes ativos no PIX.<br>
    Essas informações são úteis para direcionar campanhas, identificar públicos predominantes e detectar eventuais oportunidades de atuação em faixas etárias sub-representadas.
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(estat_idade)
    media = estat_idade.loc[estat_idade['Unnamed: 0'] == 'mean', 'valor'].values[0]
    mediana = estat_idade.loc[estat_idade['Unnamed: 0'] == '50%', 'valor'].values[0]
    q1 = estat_idade.loc[estat_idade['Unnamed: 0'] == '25%', 'valor'].values[0]
    q3 = estat_idade.loc[estat_idade['Unnamed: 0'] == '75%', 'valor'].values[0]

    # Se não tiver a série idade pronta, crie:
    # idades = clientes['age']    # <-- Troque 'clientes' pelo seu dataframe real de clientes

    # MAS no seu fluxo, você só tem o arquivo estat_idade, então faça assim:
    media = estat_idade.loc[estat_idade['Unnamed: 0'] == 'mean', 'valor'].values[0]
    mediana = estat_idade.loc[estat_idade['Unnamed: 0'] == '50%', 'valor'].values[0]
    q1 = estat_idade.loc[estat_idade['Unnamed: 0'] == '25%', 'valor'].values[0]
    q3 = estat_idade.loc[estat_idade['Unnamed: 0'] == '75%', 'valor'].values[0]
    minimo = estat_idade.loc[estat_idade['Unnamed: 0'] == 'min', 'valor'].values[0]
    maximo = estat_idade.loc[estat_idade['Unnamed: 0'] == 'max', 'valor'].values[0]

    # 1. Cards Will dos indicadores
    st.markdown(
        f"""
        <div style="display:flex;gap:18px;margin-bottom:14px;">
            <div style="background:#FFF;padding:20px 30px 14px 30px;border-radius:15px;box-shadow:0 1px 6px #0001;text-align:center;">
                <div style="font-size:1.35em;font-weight:800;color:#FED300">{media:.1f}</div>
                <div style="font-size:0.99em;color:#444;margin-top:-6px;">Média</div>
            </div>
            <div style="background:#FFF;padding:20px 30px 14px 30px;border-radius:15px;box-shadow:0 1px 6px #0001;text-align:center;">
                <div style="font-size:1.35em;font-weight:800;color:#8E4FE0">{mediana:.1f}</div>
                <div style="font-size:0.99em;color:#444;margin-top:-6px;">Mediana</div>
            </div>
            <div style="background:#FFF;padding:20px 30px 14px 30px;border-radius:15px;box-shadow:0 1px 6px #0001;text-align:center;">
                <div style="font-size:1.35em;font-weight:800;color:#6DD3FA">{q1:.1f} / {q3:.1f}</div>
                <div style="font-size:0.99em;color:#444;margin-top:-6px;">Quartis</div>
            </div>
            <div style="background:#FFF;padding:20px 30px 14px 30px;border-radius:15px;box-shadow:0 1px 6px #0001;text-align:center;">
                <div style="font-size:1.35em;font-weight:800;color:#FFA600">{minimo:.0f} - {maximo:.0f}</div>
                <div style="font-size:0.99em;color:#444;margin-top:-6px;">Mín / Máx</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- 5. Transações Suspeitas (Outliers)
elif menu == "Transações Suspeitas":
    st.header("🕵️ Transações Suspeitas (Outliers)")
    trans_suspeitas = load_csv("data/gold/gold_transacoes_suspeitas.csv")
    resumo = Path("data/gold/gold_transacoes_suspeitas_resumo.txt")

    st.subheader("Resumo Estatístico dos Outliers")
    
    st.markdown("""
    <div style="margin-bottom:30px;font-size:1.05em;color:#444;">
    <b>Descrição:</b><br>
    O painel abaixo apresenta um resumo estatístico das transações PIX identificadas como suspeitas, com base em um critério automático de valor acima do limite.  
    Cada card exibe um indicador relevante: quantidade total de transações suspeitas, média dos valores, valores máximo e mínimo, limite de corte e a mediana do conjunto original.<br>
    
    </div>
    """, unsafe_allow_html=True)


    # Lê e extrai os indicadores do TXT, se existir
    indicadores = {
        "Total de Suspeitas": None,
        "Média dos Valores": None,
        "Máximo": None,
        "Mínimo": None,
        "Limite Suspeito": None,
        "Mediana Original": None
    }
    if resumo.exists():
        txt = resumo.read_text()
        for line in txt.splitlines():
            if "Total de transações suspeitas" in line:
                indicadores["Total de Suspeitas"] = int(line.split(":")[1].strip())
            elif "Média dos valores suspeitos" in line:
                indicadores["Média dos Valores"] = float(line.split(":")[1].strip().replace("R$", "").replace(",", "."))
            elif "Valor máximo suspeito" in line:
                indicadores["Máximo"] = float(line.split(":")[1].strip().replace("R$", "").replace(",", "."))
            elif "Valor mínimo suspeito" in line:
                indicadores["Mínimo"] = float(line.split(":")[1].strip().replace("R$", "").replace(",", "."))
            elif "Limite considerado suspeito" in line:
                indicadores["Limite Suspeito"] = float(line.split(":")[1].strip().replace("R$", "").replace(",", "."))
            elif "Mediana original" in line:
                indicadores["Mediana Original"] = float(line.split(":")[1].strip().replace("R$", "").replace(",", "."))

        # Cards Will para os principais indicadores
        st.markdown(
        f"""
        <div style="display:flex;gap:18px;margin-bottom:14px;">
            <div style="background:#FED300;padding:18px 28px 12px 28px;border-radius:15px;box-shadow:0 1px 6px #0001;text-align:center;min-width:160px;">
                <div style="font-size:1.18em;font-weight:800;color:#000000">{indicadores['Total de Suspeitas']:,}</div>
                <div style="font-size:0.99em;color:#000;margin-top:-6px;">Total Suspeitas</div>
            </div>
            <div style="background:#FFF;padding:18px 28px 12px 28px;border-radius:15px;box-shadow:0 1px 6px #0001;text-align:center;min-width:160px;">
                <div style="font-size:1.18em;font-weight:800;color:#000000">{formatar_brl(indicadores['Média dos Valores'])}</div>
                <div style="font-size:0.99em;color:#444;margin-top:-6px;">Média dos Valores</div>
            </div>
            <div style="background:#FFF;padding:18px 28px 12px 28px;border-radius:15px;box-shadow:0 1px 6px #0001;text-align:center;min-width:160px;">
                <div style="font-size:1.18em;font-weight:800;color:#000000">{formatar_brl(indicadores['Máximo'])}</div>
                <div style="font-size:0.99em;color:#444;margin-top:-6px;">Valor Máximo</div>
            </div>
            <div style="background:#FFF;padding:18px 28px 12px 28px;border-radius:15px;box-shadow:0 1px 6px #0001;text-align:center;min-width:160px;">
                <div style="font-size:1.18em;font-weight:800;color:#000000">{formatar_brl(indicadores['Mínimo'])}</div>
                <div style="font-size:0.99em;color:#444;margin-top:-6px;">Valor Mínimo</div>
            </div>
            <div style="background:#FFF;padding:18px 28px 12px 28px;border-radius:15px;box-shadow:0 1px 6px #0001;text-align:center;min-width:160px;">
                <div style="font-size:1.18em;font-weight:800;color:#222">{formatar_brl(indicadores['Limite Suspeito'])}</div>
                <div style="font-size:0.99em;color:#444;margin-top:-6px;">Limite Suspeito</div>
            </div>
            <div style="background:#FFF;padding:18px 28px 12px 28px;border-radius:15px;box-shadow:0 1px 6px #0001;text-align:center;min-width:160px;">
                <div style="font-size:1.18em;font-weight:800;color:#444">{formatar_brl(indicadores['Mediana Original'])}</div>
                <div style="font-size:0.99em;color:#444;margin-top:-6px;">Mediana Original</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


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
