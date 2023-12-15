import streamlit as st
# Inserir a logo do Spotify
st.image('netflix.png',  use_column_width=True)
# Título
st.title("Análise da Base de Dados de Pontuações IMDB para Programas de TV e Filmes da Netflix")

# Introdução
st.write("A base de dados em questão contém informações cruciais sobre as pontuações IMDB atribuídas a programas de TV e filmes disponíveis na plataforma Netflix. Essa análise visa proporcionar uma compreensão abrangente da estrutura e conteúdo dessa base, destacando a importância de suas colunas e fornecendo uma visão geral sobre suas dimensões.")

# Especificações das Colunas
st.subheader("Especificações das Colunas:")
st.markdown("1. **Title (Título):** Representa o nome das séries, filmes e shows presentes na plataforma Netflix.")
st.markdown("2. **Type (Tipo):** Descreve se o conteúdo é um filme ou um show.")
st.markdown("3. **Description (Descrição):** Apresenta a sinopse ou uma breve descrição do conteúdo.")
st.markdown("4. **Release_year (Ano de Lançamento):** Indica o ano em que o programa de TV ou filme foi lançado.")
st.markdown("5. **Age_certification (Certificação de Idade):** Fornece informações sobre a certificação de idade associada ao conteúdo.")
st.markdown("6. **Runtime (Tempo de Execução):** Indica a duração total do programa de TV ou filme.")
st.markdown("7. **Imdb_id (Identificação IMDB):** Um identificador único associado ao conteúdo na base de dados IMDB.")
st.markdown("8. **Imdb_Score (Pontuação IMDB):** Representa a pontuação atribuída pelo IMDB ao programa de TV ou filme.")
st.markdown("9. **Imdb_votes (Votos IMDB):** Indica a quantidade total de votos recebidos na plataforma IMDB.")