#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import numpy as np
import folium
import pygeohash as gh
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from colour import Color


# In[2]:


df = pd.read_excel(r"ruta",sheet_name="BD")
df.dropna(subset=['Lat'], inplace= True)


# In[3]:


WIDETECH = df[['PLACA','Lat','Long']]


# In[4]:


ITURAN = pd.read_excel(r"ruta",sheet_name="BD_GENERAL")


# In[5]:


## FILTRAR, QUITAR PLACAS CON REPORTE RECIENTE.
ITURAN = ITURAN[ITURAN['DT__TRIP_START_DATETIME']<='2023-07-15']


# In[6]:


ITURAN = ITURAN[['V_DESCRIPTION','G_LATITUDE','G_LONGITUDE']]


# In[7]:


ITURAN.columns = ['PLACA','Lat','Long']


# In[8]:


def format_number(num):
    num_str = str(num)  # Convertir el valor a cadena de texto
    if num_str.startswith('1'):
        return f'{num_str[:2]}.{num_str[2:]}'
    else:
        return f'{num_str[:1]}.{num_str[1:]}'


# In[9]:


ITURAN['Lat'] = ITURAN['Lat'].apply(format_number)


# In[10]:


def format(num):
    num_str= str(num)
    return f'{num_str[:3]}.{num_str[3:]}'


# In[11]:


ITURAN['Long'] = ITURAN['Long'].apply(lambda x:format(x))


# In[12]:


# unir dataframes para consolidar datos
data = pd.concat([WIDETECH,ITURAN], ignore_index=True)


# In[13]:


data['Lat'] = data['Lat'].astype('float')


# In[14]:


data['Long'] = data['Long'].astype('float')


# In[15]:


data['geohash']=data.apply(lambda x: gh.encode(x.Lat, x.Long, precision=6), axis=1)


# ## ahora calculamos los geohash, para las sedes. y así quitarlas del estudio. 

# In[ ]:


# Carga el archivo de sedes
SEDES = pd.read_excel(r"C:\Users\jramos\Renting Colombia S.A\Gerencia de Estructuración Logística Tempo - Documentos Guia\TIL\Johao Ramos\Proyecto_localiza\Localiza - Renting Colombia - SEDES.xlsx",sheet_name ="Sede")


# In[ ]:


# Crea una nueva columna para almacenar los Geohash
SEDES['geohash'] = SEDES.apply(lambda x: gh.encode(x.Lat, x.Long, precision=6), axis=1)


# In[ ]:


## quitamos los geohash de las sedes
data = data[~data['geohash'].isin(SEDES['geohash'])]


# In[ ]:


# cargamos data de los geohash del estudio que se tendrán en cuenta. 


# In[ ]:


zonas_rojas = pd.read_excel(r"ruta",sheet_name ="Heohash_estudio")


# In[ ]:


data = data[data['geohash'].isin(zonas_rojas['geohash'])]


# In[ ]:


col = gpd.read_file(r"ruta")


# In[ ]:


mapa = folium.Map(location=[data['Lat'].mean(), data['Long'].mean()], zoom_start=5.5)


# In[ ]:


folium.GeoJson(col).add_to(mapa)


# In[ ]:


grouped_data = data.groupby('geohash').size().reset_index(name='count')

# Obtener el mínimo y máximo de la cantidad de puntos para normalizar la escala de colores
min_count = grouped_data['count'].min()
max_count = grouped_data['count'].max()

# Definir la escala de colores personalizada desde verde hasta rojo
color_map = mcolors.LinearSegmentedColormap.from_list('custom_colormap', [(0, 'green'), (0.5, 'yellow'), (1, 'red')])

for index, row in grouped_data.iterrows():
    geohash_code = row['geohash']
    count = row['count']
    subset = data[data['geohash'] == geohash_code]
    min_lat, max_lat = subset['Lat'].min(), subset['Lat'].max()
    min_lon, max_lon = subset['Long'].min(), subset['Long'].max()
    bounds = [(min_lat, min_lon), (max_lat, max_lon)]
    normalized_count = (count - min_count) / (max_count - min_count)
    # Obtener el color correspondiente en la escala personalizada
    color = mcolors.to_hex(color_map(normalized_count))
    folium.vector_layers.Rectangle(
        bounds=bounds,
        color=color,
        fill_color=color,
        fill_opacity=0.4,
        weight=1,
        tooltip=f'Geohash: {geohash_code}\nCantidad: {count}').add_to(mapa)


# In[ ]:


from geopy.adapters import AioHTTPAdapter
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="my_request")


# In[ ]:


# Crea una lista para almacenar las ciudades correspondientes a los geohashes
ciudades = []

# Itera sobre los geohashes en el DataFrame
for geohash_code in grouped_data['geohash']:
    # Decodifica el geohash para obtener las coordenadas de latitud y longitud
    lat, lon = gh.decode(geohash_code)
    # Realiza la geocodificación inversa para obtener la información de ubicación
    location = geolocator.reverse((lat, lon), exactly_one=True)
    if location:
        # Obtiene el nombre de la ciudad desde la información de ubicación
        ciudad = location.raw.get('address').get('city')
    else:
        ciudad = 'Desconocido'
    # Agrega la ciudad a la lista
    ciudades.append(ciudad)

# Agrega la lista de ciudades al DataFrame como una nueva columna
grouped_data['ciudad'] = ciudades


# In[ ]:


#grouped_data.to_excel("direcciones.xlsx",index=False)


# In[ ]:


mapa


# In[ ]:


grouped_data = data.groupby(['geohash','']).size().reset_index(name='count')


# In[ ]:


mapa.save(r"ruta")


# In[ ]:


import pandas as pd
from docx import Document
from docx.shared import Pt
from docx.enum.table import WD_ALIGN_VERTICAL

# Supongamos que tienes el DataFrame grouped_data con las columnas 'geohash', 'otra_columna' y 'count'

# Crear un nuevo documento de Word
doc = Document()

# Crear una tabla con el DataFrame grouped_data
filas = len(top10) + 1
columnas = len(top10.columns)

tabla = doc.add_table(rows=filas, cols=columnas)

# Establecer el estilo de la tabla
tabla.style = 'Table Grid'

# Rellenar la primera fila con los nombres de las columnas
for i, columna in enumerate(top10.columns):
    tabla.cell(0, i).text = columna
    # Alinea el contenido verticalmente al centro
    tabla.cell(0, i).vertical_alignment = WD_ALIGN_VERTICAL.CENTER

# Rellenar las filas de la tabla con los datos del DataFrame grouped_data
for i, fila in enumerate(top10.itertuples(), 1):
    for j, valor in enumerate(fila[1:], 0):
        tabla.cell(i, j).text = str(valor)
        # Alinea el contenido verticalmente al centro
        tabla.cell(i, j).vertical_alignment = WD_ALIGN_VERTICAL.CENTER

# Guardar el documento
doc.save("tabla_grouped_data.docx")


# In[ ]:




