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
st.set_page_config(page_title='Cuisines', page_icon=':knife_fork_plate:', layout='wide')

#--------------------------------------------------------------
#---------------------------Funções----------------------------
#--------------------------------------------------------------
def grafico_top_restaurantes(df1, asc):
    """
    Essa função faz um gráfico dos melhores ou piores tipos de cuisine
    Inputs:
        df1: Dataframe com os dados necessários para o cáculo
        asc: True = irá trazer os piores tipos de cuisine False = irá trazer os melhores tipos de cuisine
    Output: Coluna no streamlit
    """
    df_aux = df1.loc[:, ['cuisines','aggregate_rating']].groupby(['cuisines']).mean().reset_index()
    df_aux = df_aux.sort_values('aggregate_rating', ascending=asc)
    df_limitado = df_aux.head(qt_restaurante)
    grafico1 = px.bar(df_limitado, x='cuisines', y='aggregate_rating')
    grafico1.update_layout(xaxis_title='Tipo de culinária', yaxis_title='Média de avaliação média')
    return grafico1
def melhores_restaurantes(df1):
    """
    Essa função trás uma tabela com os melhores restaurantes, organizados por aggregate_rating e restaurant_id, respectivamente.
    Input: Dataframe
    Output: Dataframe
    """
    df_aux = df1.loc[:, ['restaurant_id','restaurant_name','country_code','city','cuisines',
                         'average_cost_for_two','aggregate_rating','votes']]
    df_aux = df_aux.sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True])
    df_limitado = df_aux.head(qt_restaurante)
    return df_limitado

def top_cuisines(df1, index, col_name, asc):
    """
    Essa função trás a visualização no streamlit do melhor ou pior restaurante do tipo de cuisine de acordo com alguns parâmetros
    Inputs:
        df1: Dataframe com os dados necessários para o cáculo
        index: Qual a posição do restaurante que deseja retornar as informações. Se 0, a função retornará o primeiro restaurante, se 1 retornará o segundo
        col_name: O nome da coluna do streamlit onde irá aparecer as informações do restaurante
        asc: True = irá ordenar da pior nota para a melhor False = irá ordenar da melhor nota para a pior
    Output: Coluna no streamlit
    """
    df_aux = df1.loc[df1['cuisines'] == type_cuisine, :]
    df_aux = df_aux.sort_values(['aggregate_rating','restaurant_id'], ascending=[asc, True]).reset_index()
    restaurante = df_aux.loc[index,'restaurant_name']
    nota = df_aux.loc[index,'aggregate_rating' ]
    pais = df_aux.loc[index,'country_code']
    cidade = df_aux.loc[index,'city']
    prato2 = df_aux.loc[index,'average_cost_for_two']
    help_text = f'Pais: {pais}    Cidade: {cidade}    Média prato para dois: {prato2}'
    col_name.metric( f'{type_cuisine}: {restaurante}', f'{nota}/5.0', help=help_text)
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

st.markdown( '# :knife_fork_plate: Visão Tipos culinários')
col1, col2 = st.sidebar.columns(2)
with col1:
    image = Image.open('imagem.png')
    st.image(image, width=40)
with col2:
    st.markdown('# Fome Zero')
st.sidebar.markdown('### Filtros')

type_cuisine = st.sidebar.selectbox('Qual tipo culinário você quer ver no primeiro menu?', ['Italian', 'European', 'Filipino', 'American', 'Korean', 'Pizza','Taiwanese', 'Japanese', 'Coffee', 'Chinese', 'Seafood','Singaporean', 'Vietnamese', 'Latin American', 'Healthy Food','Cafe', 'Fast Food', 'Brazilian', 'Argentine', 'Arabian', 'Bakery','Tex-Mex', 'Bar Food', 'International', 'French', 'Steak','German', 'Sushi', 'Grill', 'Peruvian', 'North Eastern','Ice Cream', 'Burger', 'Mexican', 'Vegetarian', 'Contemporary','Desserts', 'Juices', 'Beverages', 'Spanish', 'Thai', 'Indian','Mineira', 'BBQ', 'Mongolian', 'Portuguese', 'Greek', 'Asian','Author', 'Gourmet Fast Food', 'Lebanese', 'Modern Australian','African', 'Coffee and Tea', 'Australian', 'Middle Eastern','Malaysian', 'Tapas', 'New American', 'Pub Food', 'Southern','Diner', 'Donuts', 'Southwestern', 'Sandwich', 'Irish','Mediterranean', 'Cafe Food', 'Korean BBQ', 'Fusion', 'Canadian','Breakfast', 'Cajun', 'New Mexican', 'Belgian', 'Cuban', 'Taco','Caribbean', 'Polish', 'Deli', 'British', 'California', 'Others','Eastern European', 'Creole', 'Ramen', 'Ukrainian', 'Hawaiian','Patisserie', 'Yum Cha', 'Pacific Northwest', 'Tea', 'Moroccan','Burmese', 'Dim Sum', 'Crepes', 'Fish and Chips', 'Russian','Continental', 'South Indian', 'North Indian', 'Salad','Finger Food', 'Mandi', 'Turkish', 'Kerala', 'Pakistani','Biryani', 'Street Food', 'Nepalese', 'Goan', 'Iranian', 'Mughlai','Rajasthani', 'Mithai', 'Maharashtrian', 'Gujarati', 'Rolls','Momos', 'Parsi', 'Modern Indian', 'Andhra', 'Tibetan', 'Kebab','Chettinad', 'Bengali', 'Assamese', 'Naga', 'Hyderabadi', 'Awadhi','Afghan', 'Lucknowi', 'Charcoal Chicken', 'Mangalorean','Egyptian', 'Malwani', 'Armenian', 'Roast Chicken', 'Indonesian','Western', 'Dimsum', 'Sunda', 'Kiwi', 'Asian Fusion', 'Pan Asian','Balti', 'Scottish', 'Cantonese', 'Sri Lankan', 'Khaleeji','South African', 'Drinks Only', 'Durban', 'World Cuisine','Izgara', 'Home-made', 'Giblets', 'Fresh Fish', 'Restaurant Cafe','Kumpir', 'Döner', 'Turkish Pizza', 'Ottoman', 'Old Turkish Bars',
'Kokoreç'])

country_options = st.sidebar.multiselect("Escolha os países que deseja vizualizar os restaurantes:", ["India","Australia", "Brazil", "Canada", "Indonesia", "New Zeland", "Philippines", "Qatar", "Singapure", "South Africa", "Sri Lanka", "Turkey", "United Arab Emirates", "England", "United States of America"], default=["India","Australia", "Brazil", "Canada", "Indonesia", "New Zeland", "Philippines"])


qt_restaurante = st.sidebar.slider('Quantidade de restaurantes que deseja visualizar', value=10, min_value=1, max_value=20)

# Para aplicar o filtro de countries no dashboard
linhas_selecionadas = df1['country_code'].isin(country_options)
df1 = df1.loc[linhas_selecionadas, :]

# =======================================
# Layout no Streamlit
# =======================================

with st.container():
    st.markdown(f'### Top 2 Melhores e 2 piores Restaurantes do tipo Culinário {type_cuisine}')
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('##### Top 2 Melhores')
        col1, col12 = st.columns(2)
        with col1:
            top_cuisines(df1, index=0, col_name=col1, asc=False)         
        with col12:
            top_cuisines(df1, index=1, col_name=col12, asc=False)      
    with col2:
        st.markdown('##### Top 2 Piores')
        col1, col2 = st.columns(2)
        with col1:
            top_cuisines(df1, index=0, col_name=col1, asc=True)
        with col2:
            top_cuisines(df1, index=1, col_name=col2, asc=True)
with st.container():
    st.markdown(f'#### Top {qt_restaurante} restaurantes')
    df_limitado = melhores_restaurantes(df1)
    st.dataframe(df_limitado)
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'Top {qt_restaurante} Melhores tipos de culinária')
        grafico1 = grafico_top_restaurantes(df1, asc=False)
        st.plotly_chart(grafico1, use_container_width=True)
    with col2:
        st.markdown(f'Top {qt_restaurante} Piores tipos de culinária')
        grafico1 = grafico_top_restaurantes(df1, asc=True)
        st.plotly_chart(grafico1, use_container_width=True)
        