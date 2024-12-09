import streamlit as st
from dataset import df
from utils import convert_csv, mensagem_sucesso

st.title('Dataset de Vendas')
with st.expander('Colunas'):
    colunas = st.multiselect(
        'Selecione as Colunas',
        list(df.columns),
        list(df.columns)
    )
st.sidebar.title('Filtros')
with st.sidebar.expander('Categoria do Produto'):
    categorias = st.multiselect(
        'Selecione as Categorias',
        df['Categoria do Produto'].unique(),
        df['Categoria do Produto'].unique()
    )

with st.sidebar.expander('Estado'):
    estado = st.multiselect(
        'Selecione o Estado',
        df['Local da compra'].unique(),
        df['Local da compra'].unique()
    )

with st.sidebar.expander('Vendedor'):
    vendedor = st.multiselect(
        'Selecione o Vendedor',
        df['Vendedor'].unique(),
        df['Vendedor'].unique()
    )

with st.sidebar.expander('Preço do Produto'):
    preco = st.slider(
        'Selecione o preço',
        0, 5000,
        (0, 5000)
    )

with st.sidebar.expander('Data da compra'):
    data = st.date_input(
        'Selecione a data',
        (df['Data da Compra'].min(),
        df['Data da Compra'].max())
    )

query = '''
    `Categoria do Produto` in @categorias and \
    `Local da compra` in @estado and \
    `Vendedor` in @vendedor and \
    @preco[0] <= Preço <= @preco[1] and \
    @data[0] <= `Data da Compra` <= @data[1]
'''
filtro_dados = df.query(query)
filtro_dados = filtro_dados[colunas]
st.dataframe(filtro_dados)
st.markdown(f'A tabela possui :blue [{filtro_dados.shape[0]}] linhas e :blue [{filtro_dados.shape[1]}] colunas')
st.markdown('Escreva o nome do arquivo')

col1, col2 = st.columns(2)
with col1:
    nome_arquivo = st.text_input(
        '',
        label_visibility='collapsed'
    )
    nome_arquivo += '.csv'
with col2:
    st.download_button(
        'Baixar arquivo',
        data = convert_csv(filtro_dados),
        file_name = nome_arquivo,
        mime = 'text/csv',
        on_click = mensagem_sucesso()
    )

