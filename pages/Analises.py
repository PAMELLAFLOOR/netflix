import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px

# Carregar os dados
@st.cache_data
def load_data():
    data = pd.read_csv('netflix.csv', sep=';')
    return data

# Lê os dados
data = load_data()

# Título do Dashboard
st.title('Dashboard do Netflix - Análise Estatística')

# Sidebar com opções
st.sidebar.title('Opções')
menu = st.sidebar.selectbox('Selecione uma opção:', ('Visão Geral','Análise por Ano de Lançamento', 'Análise por Duração','Comparação da classificação etária','Top 10 Melhores Filmes','Análise por Type e IMDB Votes','Informações do Filme','Correlação entre Variáveis'))

# Visão Geral dos Dados
if menu == 'Visão Geral':
    st.header('Visão Geral das Pontuações IMDB para Séries, Filmes e Shows da Netflix')
    st.write(data.head())

    st.subheader('Informações Gerais')
    descricao_estatisticas = data.describe().rename(index={
        'count': 'Contagem',
        'mean': 'Média',
        'std': 'Desvio Padrão',
        'min': 'Mínimo',
        '25%': '25º Percentil',
        '50%': 'Mediana',
        '75%': '75º Percentil',
        'max': 'Máximo'
    })

    st.write("A tabela abaixo apresenta estatísticas descritivas.")
    st.write(descricao_estatisticas)

# Análise por Ano de Lançamento
elif menu == 'Análise por Ano de Lançamento':
    st.header('Análise por Ano de Lançamento')

    # Verificar se as colunas existem no conjunto de dados
    if 'type' in data.columns and 'release_year' in data.columns and 'age_certification' in data.columns:
        # Filtros interativos
        selected_type = st.selectbox('Selecione o Tipo:', data['type'].unique())
        selected_release_year = st.selectbox('Selecione o Ano de Lançamento:', data['release_year'].unique())
        selected_age_certification = st.selectbox('Selecione a Certificação de Idade:', data['age_certification'].unique())

        # Filtrar os dados com base nos filtros selecionados
        filtered_data = data[(data['type'] == selected_type) & (data['release_year'] == selected_release_year) & (data['age_certification'] == selected_age_certification)]

        # Exibir tabela com os resultados do filtro
        st.subheader('Resultados do Filtro')
        st.write(filtered_data)

    else:
        st.warning("As colunas necessárias não estão presentes no conjunto de dados.")

# Análise por Duração
elif menu == 'Análise por Duração':
    st.header('Análise por Duração')

    # Adicionar filtro de duração
    selected_duration = st.selectbox('Selecione a Duração do Filme:', ['Curto (<60 minutos)', 'Comum (60-120 minutos)', 'Longo (>120 minutos)'])

    if selected_duration == 'Curto (<60 minutos)':
        filtered_data = data[data['runtime'] < 60]
    elif selected_duration == 'Comum (60-120 minutos)':
        filtered_data = data[(data['runtime'] >= 60) & (data['runtime'] <= 120)]
    else:
        filtered_data = data[data['runtime'] > 120]

    # Exibir tabela com os resultados do filtro de duração
    st.subheader('Resultados do Filtro de Duração')
    st.write(filtered_data)

# Comparação Age Certification
elif menu == 'Comparação da classificação etária':
    st.header('Comparação da classificação etária com Média de IMDB Score')

    # Tratar a coluna imdb_score como numérica
    data['imdb_score'] = pd.to_numeric(data['imdb_score'], errors='coerce')

    # Calcular a média do imdb_score para cada categoria de age_certification
    avg_score_by_certification = data.groupby('age_certification')['imdb_score'].mean().reset_index()

    # Criar gráfico de barras
    fig_bar_chart = px.bar(avg_score_by_certification, x='age_certification', y='imdb_score', title='Média de IMDB Score por Age Certification', labels={'x': 'Age Certification', 'y': 'Média de IMDB Score'})
    st.plotly_chart(fig_bar_chart)

# Top 10 Melhores Filmes
elif menu == 'Top 10 Melhores Filmes':
    st.header('Top 10 Melhores Filmes por IMDB Score e IMDB Votes')

    # Tratar a coluna imdb_score como numérica
    data['imdb_score'] = pd.to_numeric(data['imdb_score'], errors='coerce')

    # Filtrar os top 10 melhores filmes
    top_movies = data.nlargest(10, 'imdb_score')

    # Criar gráfico de barras horizontal
    fig_bar_chart_top_movies = px.bar(top_movies, x='imdb_score', y='title', orientation='h',
                                      title='Top 10 Melhores Filmes por IMDB Score e IMDB Votes',
                                      labels={'x': 'IMDB Score', 'y': 'Título'},
                                      text='imdb_votes',  # Adicionando a quantidade de votos como texto na barra
                                      height=400)  # Ajustando a altura do gráfico

    st.plotly_chart(fig_bar_chart_top_movies)

# Análise por Type e IMDB Votes
elif menu == 'Análise por Type e IMDB Votes':
    st.header('Análise por Type e IMDB Votes')

    # Verificar se as colunas existem no conjunto de dados
    if 'type' in data.columns and 'imdb_votes' in data.columns:
        # Agrupar os dados por tipo e calcular a média de votos
        avg_votes_by_type = data.groupby('type')['imdb_votes'].mean().reset_index()

        # Criar gráfico de barras
        fig_votes_by_type = px.bar(avg_votes_by_type, x='type', y='imdb_votes',
                                   title='Média de IMDB Votes por Tipo',
                                   labels={'x': 'Tipo', 'y': 'Média de IMDB Votes'},
                                   text='imdb_votes',  # Adicionando a quantidade de votos como texto na barra
                                   height=400)  # Ajustando a altura do gráfico

        st.plotly_chart(fig_votes_by_type)

    else:
        st.warning("As colunas necessárias não estão presentes no conjunto de dados.")

# Informações do Filme
elif menu == 'Informações do Filme':
    st.header('Informações do Filme')

    # Seletor de filmes
    selected_movie = st.selectbox('Selecione um Filme:', data['title'].unique())

    # Filtrar dados para o filme selecionado
    selected_movie_data = data[data['title'] == selected_movie]

    # Exibir informações do filme selecionado
    if not selected_movie_data.empty:
        st.subheader(f'Descrição: {selected_movie_data["description"].iloc[0]}')
        st.write(f'Ano de Lançamento: {selected_movie_data["release_year"].iloc[0]}')
        st.write(f'Certificação de Idade: {selected_movie_data["age_certification"].iloc[0]}')
        st.write(f'Tempo de Execução: {selected_movie_data["runtime"].iloc[0]} minutos')
        st.write(f'IMDB ID: {selected_movie_data["imdb_id"].iloc[0]}')
        st.write(f'Pontuação IMDB: {selected_movie_data["imdb_score"].iloc[0]}')
        st.write(f'Votos IMDB: {selected_movie_data["imdb_votes"].iloc[0]}')
    else:
        st.warning("Nenhum filme selecionado. Escolha um filme no seletor acima.")

# Filme Mais Votado por Ano e Categoria
elif menu == 'Filme Mais Votado por Ano e Categoria':
    st.header('Filme Mais Votado por Ano e Categoria')

    # Verificar se as colunas necessárias existem no conjunto de dados
    if 'title' in data.columns and 'type' in data.columns and 'release_year' in data.columns and 'imdb_votes' in data.columns:
        # Tratar a coluna imdb_votes como numérica
        data['imdb_votes'] = pd.to_numeric(data['imdb_votes'], errors='coerce')

        # Seletor de ano
        selected_year = st.selectbox('Selecione um Ano:', data['release_year'].unique())

        # Seletor de categoria (filme ou show)
        selected_category = st.radio('Selecione a Categoria:', ['Filme', 'Show'])

        # Filtrar os dados para o filme mais votado por ano e categoria
        most_voted_movie_by_year_category = data[(data['release_year'] == selected_year) & (data['type'] == selected_category)].nlargest(1, 'imdb_votes')

        # Exibir informações do filme mais votado por ano e categoria
        if not most_voted_movie_by_year_category.empty:
            st.subheader(f'Descrição: {most_voted_movie_by_year_category["description"].iloc[0]}')
            st.write(f'Ano de Lançamento: {most_voted_movie_by_year_category["release_year"].iloc[0]}')
            st.write(f'Tipo: {most_voted_movie_by_year_category["type"].iloc[0]}')
            st.write(f'IMDB ID: {most_voted_movie_by_year_category["imdb_id"].iloc[0]}')
            st.write(f'Pontuação IMDB: {most_voted_movie_by_year_category["imdb_score"].iloc[0]}')
            st.write(f'Votos IMDB: {most_voted_movie_by_year_category["imdb_votes"].iloc[0]}')
        else:
            st.warning(f'Nenhum filme encontrado para o ano {selected_year} e categoria {selected_category}.')

    else:
        st.warning("As colunas necessárias não estão presentes no conjunto de dados.")

# Correlação entre as Variáveis
elif menu == 'Correlação entre Variáveis':
    st.subheader('Correlação entre Variáveis')
    
    # Selecionar apenas colunas numéricas
    numeric_columns = data.select_dtypes(include='number').columns
    
    # Substituir valores não numéricos por NaN
    data_numeric = data[numeric_columns].apply(pd.to_numeric, errors='coerce')
    
    # Calcular a matriz de correlação
    corr_matrix = data_numeric.corr()
    
    # Plotar o heatmap
    fig_corr = sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    st.pyplot(fig_corr.figure)

# Créditos
st.sidebar.text("Desenvolvido por: Pamella Rocha")
