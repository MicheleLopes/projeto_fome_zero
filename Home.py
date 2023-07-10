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
st.set_page_config(page_title='Main Page', page_icon=':bar_chart:')

#--------------------------------------------------------------
#---------------------------Funções----------------------------
#--------------------------------------------------------------
def mapa(df1):
        """ 
        Função para montar um mapa com marcadores de todos os restaurantes da plataforma e personalizar a visualição de algumas informações
        Input: DataFrame
        Output: o mapa é exibido no streamlit
        """
        mapa = folium.Map()
        marker_cluster = MarkerCluster().add_to(mapa)
        for index, location in df1.iterrows():
            rating_color = location['rating_color']
            conteudo_popup = f""" 
                        <h4 style="font-weight: bold;">{location['restaurant_name']}</h4>
                        <p>Type: {location['cuisines']}</p>
                        <p>Price for two: {location['average_cost_for_two']} {location['currency']}</p>
                        <p>Aggregate Rating: {location['aggregate_rating']}</p>
        """
            folium.Marker([location['latitude'], 
                           location['longitude']],    popup=folium.Popup(conteudo_popup, max_width=300), icon=folium.Icon(color=rating_color, icon='home', prefix='fa')).add_to(marker_cluster)
    
        folium_static(mapa, width=800, height=600)
        return None

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
st.markdown( '# Fome zero!')
st.markdown('## O Melhor lugar para encontrar seu mais novo restaurante favorito!')
st.markdown('### Temos as seguintes marcas dentro da nossa plataforma:')
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
    col1, col2, col3 = st.columns(3)
    with col1:
        rest = len(df1['restaurant_id'].unique())
        col1.metric( 'Restaurantes cadastrados', rest ) 
    with col2:
        paises = len(df1['country_code'].unique())
        col2.metric( 'Restaurantes cadastrados', paises ) 
    with col3:
        cidades = len(df1['city'].unique())
        col3.metric( 'cidades cadastradas', cidades ) 
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        avaliacoes = df1['votes'].sum()
        col1.metric( 'Avaliações na plataforma', avaliacoes ) 
    with col2:
        cuisines = len(df1['cuisines'].unique())
        col2.metric( 'Tipos de culinária', cuisines )   
with st.container():
    mapa(df1)
