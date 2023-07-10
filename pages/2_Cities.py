#libraries
import pandas as pd
import inflection
import numpy as np
import folium 
import streamlit as st
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import plotly.express as px
from PIL import Image
st.set_page_config(page_title='Cities', page_icon=':city_sunrise:', layout='wide')

#--------------------------------------------------------------
#---------------------------Funções----------------------------
#--------------------------------------------------------------
def grafico_cuisines_cidade(df1):
    """
    Função para montar um gráfico com a quantidade de tipos de cuisines por cidade e algumas personalizações de visualização
    Input: Daframe
    Output: Gráfico
    """
    df_aux = df1.loc[:, ['city','cuisines','restaurant_id','country_code']].groupby(['country_code','city','cuisines']).count().reset_index()
    df_aux = df_aux.loc[:,['city','cuisines','country_code']].groupby(['country_code','city']).count().reset_index()
    df_aux = df_aux.sort_values('cuisines', ascending=False)
    df_limitado = df_aux.head(10)
    grafico1 = px.bar(df_limitado, x='city', y='cuisines', color='country_code', color_discrete_sequence=['blue', 'green', 'red', 'orange','yellow','purple', 'pink', 'black'])
    grafico1.update_layout(xaxis_title='Cidades', yaxis_title='Quantidade Tipos de culinária distintos')
    return grafico1

def grafico_media2_cidade(df1):
    """
    Função para montar um gráfico com a quantidade de restaurantes com média de avaliação abaixo de 2,5, separado por cidade e algumas    personalizações de visualização
    Input: Daframe
    Output: Gráfico
    """
    selecao = df1['aggregate_rating'] < 2.5
    df_aux = df1.loc[selecao, :]
    df_aux = df_aux.loc[:, ['city','aggregate_rating','country_code']].groupby(['country_code','city']).count().reset_index()
    df_aux = df_aux.sort_values('aggregate_rating', ascending=False)
    df_limitado = df_aux.head(7)
    grafico1 = px.bar(df_limitado, x='city', y='aggregate_rating', color='country_code', color_discrete_sequence=['blue', 'green', 'red', 'orange','yellow','purple', 'pink', 'black'])
    grafico1.update_layout(xaxis_title='Cidades', yaxis_title='Quantidade restaurantes')
    return grafico1

def grafico_media4_cidade(df1):
    """
    Função para montar um gráfico com a quantidade de restaurantes com média de avaliação acima de 4, separado por cidade e algumas    personalizações de visualização
    Input: Daframe
    Output: Gráfico
    """
    selecao = df1['aggregate_rating'] >= 4
    df_aux = df1.loc[selecao, :]
    df_aux = df_aux.loc[:, ['city','aggregate_rating', 'country_code']].groupby(['country_code','city']).count().reset_index()
    df_aux = df_aux.sort_values('aggregate_rating', ascending=False)
    df_limitado = df_aux.head(7)
    grafico1 = px.bar(df_limitado, x='city', y='aggregate_rating', color='country_code', color_discrete_sequence=['blue', 'green', 'red', 'orange','yellow','purple', 'pink', 'black'])
    grafico1.update_layout(xaxis_title='Cidades', yaxis_title='Quantidade restaurantes')
    return grafico1

def grafico_restaurantes_cidade(df1):
    """
    Função para montar um gráfico com a quantidade de restaurantes por cidade e algumas personalizações de visualização
    Input: Daframe
    Output: Gráfico
    """
    df_aux = df1.loc[:,['restaurant_id','city','country_code'] ].groupby(['country_code','city']).count().reset_index()
    df_aux = df_aux.sort_values('restaurant_id', ascending=False)
    df_limitado = df_aux.head(10)
    grafico1 = px.bar(df_limitado, x='city', y='restaurant_id', color='country_code', color_discrete_sequence=['blue', 'green', 'red', 'orange','yellow','purple', 'pink', 'black'])
    grafico1.update_layout(xaxis_title='Cidades', yaxis_title='Quantidade restaurantes')
    return grafico1
    
def clean_code(df1):
    """ Esta função tem a responsabilidade de limpar o dataframe
    Tipo de limpeza:
    1. Preencher o nome dos países
    2. Criação do tipo de categoria de comida
    3. Rreencher o nome das cores
    4. Renomear as colunas do DataFrame
    5. Remover os valores vazios
    6. Remover a coluna switch_to_order_menu
    7. Remover linhas duplicadas

    Input: Dataframe
    Output: Dataframe
    """
    # Preenchimento do nome dos países
    COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
    }
    def country_name(country_id):
        return COUNTRIES[country_id]
    for i in range(len(df1)):
        df1.loc[i,'Country Code'] = country_name(df1.loc[i,'Country Code'])
    
    #Criação do Tipo de Categoria de Comida
    def create_price_tye(price_range):
        if price_range == 1:
            return "cheap"
        elif price_range == 2:
            return "normal"
        elif price_range == 3:
            return "expensive"
        else:
            return "gourmet"
    
    for i in range(len(df1)):
        df1.loc[i,'Price range'] = create_price_tye(df1.loc[i,'Price range'])
    
    #Criação do nome das Cores
    COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
    }
    def color_name(color_code):
        return COLORS[color_code]
    for i in range(len(df1)):
        df1.loc[i,'Rating color'] = color_name(df1.loc[i,'Rating color'])
    
    # Renomear as colunas do DataFrame
    def rename_columns(dataframe):
        df = dataframe.copy()
        title = lambda x: inflection.titleize(x)
        snakecase = lambda x: inflection.underscore(x)
        spaces = lambda x: x.replace(" ", "")
        cols_old = list(df.columns)
        cols_old = list(map(title, cols_old))
        cols_old = list(map(spaces, cols_old))
        cols_new = list(map(snakecase, cols_old))
        df.columns = cols_new
        return df
    df1 = rename_columns(df1)
    # Remover os valores vazios de cuisines
    
    df1 = df1.dropna(subset=['cuisines'])
    df1 = df1.reset_index(drop=True)
    # Categorizar restaurantes somente por um tipo de culinária
    df1["cuisines"] = df1.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])
    
    #Remover a coluna switch_to_order_menu
    df1.pop('switch_to_order_menu')
    
    #Excluindo colunas duplicadas
    df1_duplicadas = df1.duplicated()
    df1_duplicadas = df1_duplicadas.to_frame()
    
    for i in range(len(df1)):
        if df1_duplicadas.iloc[i,0] == True:
            df1 = df1.drop(i)
    df1 = df1.reset_index(drop=True)
    return df1

# --------------- Inicio da estrutura lógica do código ---------------
#---------------------------------------------------------------------
#Importar o dataset
df = pd.read_csv('zomato.csv')
#Limpar o código
df1 = clean_code(df)

##### --------------------------------------------------#####
##### Barra Lateral
##### --------------------------------------------------#####

st.markdown( '# :city_sunrise: Visão Cidades')
col1, col2 = st.sidebar.columns(2)
with col1:
    image = Image.open('imagem.png')
    st.image(image, width=40)
with col2:
    st.markdown('# Fome Zero')
st.sidebar.markdown('### Filtros')
country_options = st.sidebar.multiselect("Escolha os países que deseja vizualizar os restaurantes:", ["India","Australia", "Brazil", "Canada", "Indonesia", "New Zeland", "Philippines", "Qatar", "Singapure", "South Africa", "Sri Lanka", "Turkey", "United Arab Emirates", "England", "United States of America"], default=["India","Australia", "Brazil", "Canada", "Indonesia", "New Zeland", "Philippines"])


# Para aplicar o filtro de countries no dashboard
linhas_selecionadas = df1['country_code'].isin(country_options)
df1 = df1.loc[linhas_selecionadas, :]


# =======================================
# Layout no Streamlit
# =======================================

with st.container():
    st.markdown( '#### Top 10 cidades com mais restaurantes na base de dados')
    grafico1 = grafico_restaurantes_cidade(df1)
    st.plotly_chart(grafico1, use_container_width=True)
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown( '#### Top 7 cidades com restaurantes com média de avaliação acima de 4')
        grafico1 = grafico_media4_cidade(df1)
        st.plotly_chart(grafico1, use_container_width=True)
    with col2:
        st.markdown( '#### Top 7 cidades com restaurantes com média de avaliação abaixo de 2.5')
        grafico1 = grafico_media2_cidade(df1)
        st.plotly_chart(grafico1, use_container_width=True)
with st.container():
    st.markdown( '#### Top 10 cidades com restaurantes com mais tipos culinários distintos')
    grafico1 = grafico_cuisines_cidade(df1)
    st.plotly_chart(grafico1, use_container_width=True)