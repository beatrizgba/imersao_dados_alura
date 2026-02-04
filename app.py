import streamlit as st
import pandas as pd
import plotly.express as px

# Configuracoes da pagina
# Titulo, Icone, layout (wide = ocupa a largura inteira)
st.set_page_config(
    page_title='Dashboard de Salarios na Area de Dados',
    page_icon='📊',
    layout='wide'
)

df = pd.read_csv("C:\\Users\\beatr\\OneDrive\\Documentos\\Projeto Dados Alura\\dados_imersao_alura_limpo.csv")

# -- Barra lateral
st.sidebar.header('🔍 Filtros')

# .unique = valores unicos
# st.sidebar.multiselect = campo de seleção múltipla
# (titulo, lista de opcoes, opcoes ja selecionados por padrao) """

# Filtro de ano
anos_disponiveis = sorted(df['ano'].unique())
anos_selecionados = st.sidebar.multiselect('Ano', anos_disponiveis, default=anos_disponiveis)

# Filtro Senioridade
serioridades_disponiveis = sorted(df['senioridade'].unique())
serioridades_selecionados = st.sidebar.multiselect('Senioridade', serioridades_disponiveis, default=serioridades_disponiveis)

# Filtro tipo de contrato
contratos_disponiveis = sorted(df['contrato'].unique())
contratos_selecionados = st.sidebar.multiselect('Tipo de Contrato', contratos_disponiveis, default=contratos_disponiveis)

# Filtro tamanho da empresa
tamanhos_disponiveis = sorted(df['empresa'].unique())
tamanhos_selecionados = st.sidebar.multiselect('Tamanho da Empresa', tamanhos_disponiveis, default=tamanhos_disponiveis)

# Filtragem para garantir que o dataframe so contenha os valores selecionados nos filtros
df_filtrado = df[
    (df['ano'].isin(anos_selecionados)) &
    (df['senioridade'].isin(serioridades_selecionados)) &
    (df['contrato'].isin(contratos_selecionados)) &
    (df['empresa'].isin(tamanhos_selecionados))
]

# -- Conteúdo Principal
st.title('📊 Dashboard de Salarios na Area de Dados')
st.markdown('Explore os dados salariais na area de dados com filtros interativos!')
# markdown = para escrever texto, mas posso alterar a aparência.

# -- Métricas Principais (KPIs)
st.subheader('Métricas gerais (Sálario anual em USD)')
# "h2"

if not df_filtrado.empty:
    salario_medio = df_filtrado['usd'].mean()
    salario_maximo = df_filtrado['usd'].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado['cargo'].mode()[0]

# mode() = valor mais frequente
 
else:
    salario_medio, salario_maximo, total_registros, cargo_mais_frequente = 0,0,0, ""

# Solicitando para que o streamlit crie 4 colunas para exibir as métricas
col1, col2, col3, col4 = st.columns(4)

# Definindo as colunas
col1.metric('Salário Médio', f'${salario_medio:,.2f}')
col2.metric('Salário Máximo', f'${salario_maximo:,.2f}')
col3.metric('Total de Registros', f'{total_registros}')
col4.metric('Cargo mais Frequente', cargo_mais_frequente)

st.markdown('---')
# Barra cinza para separar as seções

# -- Gráficos
st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

# With = tudo que estiver indentado abaixo sera parte dessa coluna
with col_graf1:
    if not df_filtrado.empty:
        # groupby = agrupa as linhas que possuem o mesmo cargo
        # ['usd'] = seleciona a coluna usd
        # .mean() = calcula a media dos valores agrupados
        # nlargest(10) = seleciona os 10 maiores valores
        # sort_values(ascending=True) = ordena os valores em ordem crescente
        top_cargos = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()

        graficos_cargos = px.bar(
            top_cargos, # os dados para o grafico
            x='usd', # o valor que sera exibido no eixo x
            y='cargo', # o valor que sera exibido no eixo y
            orientation='h', # orientacao horizontal
            title='Top 10 Cargos com Maior Salário Médio', # titulo do grafico
            labels={'usd': 'Salário Médio (USD)', 'cargo': 'Cargo'} # rótulos dos eixos
            )
        
        graficos_cargos.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        # title_x=0.1 = para o titulo ficar alinhado a esquerda
        # update_layout = para atualizar o layout do grafico
        # yaxis = para configurar o eixo y
        # categoryorder = ordem das categorias
        # total ascending = ordem crescente com base no total
        st.plotly_chart(graficos_cargos, use_container_width=True)
        # plotly_chart = para exibir o grafico
        # use_container_width=True = para o grafico ocupar toda a largura da coluna
    
    else:
        st.warning('Nenhum dado para exibir no gráfico de cargos.')

with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x='usd',  
            nbins=30, # numero de barras do histograma
            title='Distribuição Salarial',
            labels={'usd': 'Faixa Salarial (USD)', 'count': ''}
            )
        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist, use_container_width=True)

    else:
        st.warning('Nenhum dado para exibir no gráfico de evolução anual.')


col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
        grafico_remoto = px.pie(
            remoto_contagem,
            names='tipo_trabalho',# categorias que serao exibidas no grafico
            values='quantidade', # valores que serao exibidos no grafico
            title='Proporção dos Tipos de Trabalho',
            hole=0.5 # para fazer o grafico de rosca

        )
        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning('Nenhum dado para exibir no gráfico de tipos de trabalho.')

with col_graf4:
    if not df_filtrado.empty:
        df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
        media_ds_pais = df_ds.groupby('residencia_iso3')["usd"].mean().reset_index()
        grafico_paises = px.choropleth(
            media_ds_pais,
            locations='residencia_iso3',
            color='usd',
            color_continuous_scale='rdylgn',
            labels={'usd': 'Salário Médio (USD)', 'residencia_iso3': 'País'},
            title='Salário Médio de Data Scientists por País'
            )
        grafico_paises.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning('Nenhum dado para exibir no gráfico de salários por país.')

# mostrar a tabela com os dados filtrados
st.subheader('Dados Detalhados')
st.dataframe(df_filtrado)