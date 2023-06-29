#%%
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point, Polygon, box
import contextily as cx
import rasterio
import matplotlib.pyplot as plt
import folium
import seaborn as sns
import matplotlib.patches as mpatches
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
from sklearn.cluster import DBSCAN
from libpysal.weights import KNN
from esda.moran import Moran_Local
from matplotlib_scalebar.scalebar import ScaleBar

from mgwr.gwr import GWR, MGWR
from mgwr.sel_bw import Sel_BW
from libpysal.weights import DistanceBand, KNN


from sklearn.preprocessing import StandardScaler

import libpysal
from esda.moran import Moran_Local


#%% tratamiento fichas
#fichas=pd.read_csv(r'/home/aospinau/Documents/Unal/AnlisisGeoespacial/GitHubGDS/InspeccionesDAGRD.csv', encoding='ISO-8859-1')


# #Cambiar nombre de columna
# fichas.rename(columns={ fichas.columns[1]: "fecha" }, inplace = True)
# #definir columna de fecha como tipo datetime
# fichas['fecha']= pd.to_datetime(fichas['fecha'])

# #Crear columna de dirrección completa
# # fichas["Address"] = fichas["Dirección"] + " " + fichas["Numero"]


# #Borrar todas las fichas sin caracterizacion de evento Todos los eventos en minuscula

# fichas=fichas[fichas['Dirección'].notna()]
# fichas=fichas[fichas['Numero'].notna()]
# fichas=fichas[fichas['fecha'].notna()]
# fichas=fichas[fichas['Evento'].notna()]
# fichas['Evento']=fichas['Evento'].apply(str.lower)
# fichas['Prioridad']=fichas['Prioridad'].apply(str.lower)

# # #llenar espacios vacios de numero de evacuaciones con ceros
# # fichas['DEF'] = (pd.to_numeric(fichas['DEF'], errors='coerce').fillna(0))
# # fichas['TEM'] = (pd.to_numeric(fichas['TEM'], errors='coerce').fillna(0))


# ###Explorar Datos###

# #Número de inspecciones por meses
# #fichas['Evento'].groupby(fichas["fecha"].dt.month).count().plot(kind="bar", legend=False, ylabel='Numero de inspecciones por riesgo', xlabel='Mes')

# #Número de inspecciones por años
# #fichas['Evento'].groupby(fichas["fecha"].dt.year).count().plot(kind="bar", legend=False, ylabel='Numero de inspecciones por riesgo', xlabel='Año')



# #agrupar en unica clase inspecciones por movimientos en masa, estructural e incendio.

# fichas['Evento'] = fichas['Evento'].replace(to_replace=r'^mov.*', value='movimientos en masa', regex=True)
# fichas['Evento'] = fichas['Evento'].replace(to_replace=r'^est.*', value='estructural', regex=True)
# fichas['Evento'] = fichas['Evento'].replace(to_replace=r'^inc.*', value='incendio', regex=True)

#Para Mapgis
#Fraccionar datos de inspecciones por riesgo para 

#fichasMG= fichas[['FICHA', 'Address']].copy()

# fichas1=fichasMG.iloc[0:10000]
# fichas2=fichasMG.iloc[10000:20000]
# fichas3=fichasMG.iloc[20000:30000]
# fichas4=fichasMG.iloc[30000:40000]
# fichas5=fichasMG.iloc[40000:50000]
# fichas6=fichasMG.iloc[50000:60000]
#fichas7=fichasMG.iloc[60000:70000]
# fichas8=fichasMG.iloc[70000:80000]
# fichas9=fichasMG.iloc[80000:90000]


# fichas1.to_excel(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas1.xlsx', index = None, header=True)
# fichas2.to_excel(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas2.xlsx', index = None, header=True)
# fichas3.to_excel(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas3.xlsx', index = None, header=True)
# fichas4.to_excel(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas4.xlsx', index = None, header=True)
# fichas5.to_excel(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas5.xlsx', index = None, header=True)
# fichas6.to_excel(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas6.xlsx', index = None, header=True)
#fichas7.to_excel('/home/aospinau/Documents/Unal/AnlisisGeoespacial/GitHubGDS/fichas7.xlsx', index = None, header=True)
# fichas8.to_excel(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas8.xlsx', index = None, header=True)
# fichas9.to_excel(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas9.xlsx', index = None, header=True)


# %%# Merge fichas codificiadas

# fichasGC1=pd.read_excel('/home/aospinau/Documents/Unal/AnlisisGeoespacial/DatosFichas/fichasGC1.xlsx')
# fichasGC2=pd.read_excel('/home/aospinau/Documents/Unal/AnlisisGeoespacial/DatosFichas/fichasGC2.xlsx')
# fichasGC3=pd.read_excel('/home/aospinau/Documents/Unal/AnlisisGeoespacial/DatosFichas/fichasGC3.xlsx')
# fichasGC4=pd.read_excel('/home/aospinau/Documents/Unal/AnlisisGeoespacial/DatosFichas/fichasGC4.xlsx')
# fichasGC5=pd.read_excel('/home/aospinau/Documents/Unal/AnlisisGeoespacial/DatosFichas/fichasGC5.xlsx')
# fichasGC6=pd.read_excel('/home/aospinau/Documents/Unal/AnlisisGeoespacial/DatosFichas/fichasGC6.xlsx')
# fichasGC7=pd.read_excel('/home/aospinau/Documents/Unal/AnlisisGeoespacial/DatosFichas/fichasGC7.xlsx')
# fichasGC8=pd.read_excel('/home/aospinau/Documents/Unal/AnlisisGeoespacial/DatosFichas/fichasGC8.xlsx')
# fichasGC9=pd.read_excel('/home/aospinau/Documents/Unal/AnlisisGeoespacial/DatosFichas/fichasGC9.xlsx')

# #Agregar geometría
# fichasG=pd.concat([fichasGC1, fichasGC2, fichasGC3, fichasGC4, fichasGC7,  fichasGC5,  fichasGC6,  fichasGC8,  fichasGC9])

# fichasG['FICHA'] = fichasG['FICHA'].astype(str)
# fichas['FICHA'] = fichas['FICHA'].astype(str)
# #%%
# fichas=fichas.drop_duplicates(subset='FICHA', keep=False)
# fichasG=fichasG.drop_duplicates(subset='FICHA', keep=False)
# #%%
# fichasGC=pd.merge(fichas, fichasG, how='left', on='FICHA')

#%% #eliminar nan
#pd.set_option("display.max_rows", 10)

#fichasGC[fichasGC['Tipo'].notna()]
#fichasGC[fichasGC['Tipo'].str.startswith('MALLA VIAL APROXIMADA :CR 112 F  34CC ')]

#fichasGC.set_index('FICHA')
# %%Guardar como csv
#fichasGC.to_csv('/home/aospinau/Documents/Unal/AnlisisGeoespacial/GitHubGDS/InspeccionesGeocodificadas.csv')

#%% geolocalización fichas

#fichasGC=pd.read_csv('/home/aospinau/Documents/Unal/AnlisisGeoespacial/GitHubGDS/InspeccionesGeocodificadas.csv')


# #Definir coordenadas
# fichasGC['Coordenadas']  = list(zip(fichasGC.Longitud, fichasGC.Latitud))

# fichasGC['Coordenadas'] = fichasGC['Coordenadas'].apply(Point)

# gdf = gpd.GeoDataFrame(fichasGC, geometry='Coordenadas')

# gdf = gdf.set_crs(epsg=4326)

# # Eliminar filas correspondientes a geometrías vacías
# empty_geom = gdf.geometry.is_empty
# gdf = gdf[~empty_geom]

# #Guardar

# gdf.to_file('/home/aospinau/Documents/Unal/AnlisisGeoespacial/GitHubGDS/FichasRiesgos2.geojson', driver='GeoJSON')




#%%  #Mapa

# fig, ax = plt.subplots(figsize=(10,10))
# #gdf.plot(ax=ax, alpha=0.3, edgecolor="black", facecolor="white")
# gdf.plot(ax=ax, alpha = 0.2, color="red", marker='o');
# cx.add_basemap(ax, crs=gdf.crs, source=cx.providers.OpenStreetMap.Mapnik)
#%% #Mapa de bin
# Set up figure and axis
# f, ax = plt.subplots(1, figsize=(12, 9))
# # Generate and add hexbin with 50 hexagons in each dimension, no borderlines, half transparency, and the reverse viridis colormap
# hb = ax.hexbin(
#     gdf.Coordenadas.x, 
#     gdf.Coordenadas.y,
#     gridsize=50, 
#     linewidths=0,
#     alpha=0.5, 
#     cmap='Purples'
# )
# # Add basemap
# cx.add_basemap(
#     ax, 
#     source=cx.providers.CartoDB.Positron
# )
# # Add colorbar
# plt.colorbar(hb)
# # Remove axes
# ax.set_axis_off()
#%% PLUVIOMETROS

# pluviometros=pd.read_csv(r'/home/aospinau/Documents/Unal/AnlisisGeoespacial/PluviometrosMedellinDiario.csv')
# pluviometrosEPM=pd.read_csv(r'/home/aospinau/Documents/Unal/AnlisisGeoespacial/pluviosEPM.csv')
# #%%
# pluviometrosEPM = pluviometrosEPM[pluviometrosEPM['acumulado'] != -999]
# #%%
# pluviometrosEPM['fecha'] = pd.to_datetime(pluviometrosEPM['fecha'])
# pluviometros['fecha']= pd.to_datetime(pluviometros['fecha'])

# #Precipitacion no está en milimetros, para pasarlos se debe dividir por 1000
# pluviometros['P1']=pluviometros['P1']/1000
# pluviometros['P2']=pluviometros['P2']/1000



# pluviometrosLoc=pd.read_csv(r'/home/aospinau/Documents/Unal/AnlisisGeoespacial/GitHubGDS/ubicacionPluviometros.csv')
# pluviometrosLocEPM=pd.read_csv(r'/home/aospinau/Documents/Unal/AnlisisGeoespacial/ubicacionpluviosepm.csv')
# #%%
# # pluviometrosLoc=pluviometrosLoc.rename(columns={"Codigo": "codigo"})
# pluviometrosEPM=pluviometrosEPM.rename(columns={"idestacion": "codigo"})
# pluviometrosEPM=pluviometrosEPM.rename(columns={"acumulado": "P1"})
# pluviometrosLocEPM=pluviometrosLocEPM.rename(columns={"idestacion": "codigo"})
# pluviometrosLocEPM=pluviometrosLocEPM.rename(columns={"latitud": "Latitude"})
# pluviometrosLocEPM=pluviometrosLocEPM.rename(columns={"longitud": "Longitude"})

# #%%

# pluviometrosEPM = pluviometrosEPM.merge(pluviometrosLocEPM, on='codigo')
# pluviometros = pluviometros.merge(pluviometrosLoc, on='codigo')

# #%% aplicar geomtetría pluviometros

# pluviometrosEPM['geometry']  = list(zip(pluviometrosEPM.Longitude, pluviometrosEPM.Latitude))

# pluviometrosEPM['geometry'] = pluviometrosEPM['geometry'].apply(Point)

# pluviometrosEPM = gpd.GeoDataFrame(pluviometrosEPM, geometry='geometry')

# pluviometrosEPM = pluviometrosEPM.set_crs(epsg=4326)

# pluviometros['Coordenadas']  = list(zip(pluviometros.Longitude, pluviometros.Latitude))

# pluviometros['Coordenadas'] = pluviometros['Coordenadas'].apply(Point)

# pluviometros = gpd.GeoDataFrame(pluviometros, geometry='Coordenadas')

# pluviometros = gdf.set_crs(epsg=4326)


# #%% ventanas moviles de precipitación antecedente

# pluviometrosEPM = pluviometrosEPM.sort_values(by=['codigo', 'fecha'])

# pluviometrosEPM['acumulado_3_dias'] = pluviometrosEPM.groupby('codigo')['P1'].rolling(window=3).sum().reset_index(0, drop=True)
# pluviometrosEPM['acumulado_7_dias'] = pluviometrosEPM.groupby('codigo')['P1'].rolling(window=7).sum().reset_index(0, drop=True)
# pluviometrosEPM['acumulado_15_dias'] = pluviometrosEPM.groupby('codigo')['P1'].rolling(window=15).sum().reset_index(0, drop=True)
# pluviometrosEPM['acumulado_30_dias'] = pluviometrosEPM.groupby('codigo')['P1'].rolling(window=30).sum().reset_index(0, drop=True)
# pluviometrosEPM['acumulado_90_dias'] = pluviometrosEPM.groupby('codigo')['P1'].rolling(window=90).sum().reset_index(0, drop=True)
# pluviometrosEPM = pluviometrosEPM.sort_values(by=['codigo', 'fecha'])


# pluviometros = pluviometros.sort_values(by=['codigo', 'fecha'])

# pluviometros['acumulado_3_dias'] = pluviometros.groupby('codigo')['P1'].rolling(window=3).sum().reset_index(0, drop=True)
# pluviometros['acumulado_7_dias'] = pluviometros.groupby('codigo')['P1'].rolling(window=7).sum().reset_index(0, drop=True)
# pluviometros['acumulado_15_dias'] = pluviometros.groupby('codigo')['P1'].rolling(window=15).sum().reset_index(0, drop=True)
# pluviometros['acumulado_30_dias'] = pluviometros.groupby('codigo')['P1'].rolling(window=30).sum().reset_index(0, drop=True)
# pluviometros['acumulado_90_dias'] = pluviometros.groupby('codigo')['P1'].rolling(window=90).sum().reset_index(0, drop=True)

##%%
#eliminar datos anteriores a 2017 por dudosa calidad
#filtro = pluviometrosEPM['fecha'] <= '2017-01-01'

# Aplicar el filtro al Geodataframe
#pluviometrosEPM = pluviometrosEPM[filtro]

##%%
#pluviometros= pd.concat([pluviometros, pluviometrosEPM], ignore_index=True)

##%%

# #%% graficar series de tiempo pluviometro

# # Filtrar el DataFrame para un pluviómetro en particular
# pluv = 619  # reemplaza con el código del pluviómetro que te interese
# df_pluv = pluviometros[pluviometros['codigo'] == pluv]


# # Graficar los acumulados históricos
# plt.plot(df_pluv['fecha'], df_pluv['acumulado_7_dias'])
# plt.title(f'Acumulados históricos para pluviómetro {pluv}')
# plt.xlabel('Fecha')
# plt.ylabel('Acumulado 7 días')
# plt.show()

#pluviometros = pluviometros.drop('iddata', axis=1)
#pluviometros = pluviometros.sort_values(by='fecha')
#pluviometros=pluviometros.reset_index()
#pluviometros = pluviometros.drop('level_0', axis=1)

#pluviometros.to_file('/home/aospinau/Documents/Unal/AnlisisGeoespacial/GitHubGDS/PluvioSIATA_EPM_Diario.geojson', driver='GeoJSON')


# %%
#llamadas = gpd.read_file('FichasRiesgos2.geojson')

#gdf=llamadas
#%% depuracion de datos desconfiables
# gdf=llamadas

# #Elimina ubicaciones repetinas n veces
# gdf['geom_str'] = gdf.geometry.apply(lambda x: str(x))
# counts = gdf.groupby('geom_str').size().reset_index(name='count')
# n = 50
# unique_gdf = gdf.loc[gdf['geom_str'].isin(counts.loc[counts['count'] < n, 'geom_str'])]
# gdf = unique_gdf

# #Elimina fichas clasificadas como no ubicadas

# gdf = gdf.drop(gdf[gdf['Tipo'].str.contains('NO UBICADA')].index)

#%%Asociar cada evento con el publiometro más cercano y tomar la lluvia antecedente.

# gdf = llamadas

# gdf['fecha'] = pd.to_datetime(gdf['fecha'])

#Evitar pluviometros sin acumuladosantecedentes de 90 días.
# pluviometros= pluviometros[pluviometros['acumulado_90_dias'].notna()]

# resultados = []
# for i, evento in gdf.iterrows():
#     fecha_puntual = gdf.iloc[i]
#     eventos_seleccionados = pluviometros[pluviometros['fecha'] == fecha_puntual.fecha]

#     if len(eventos_seleccionados) == 0:
#         continue
#     # Calcular la distancia entre el evento y cada punto de referencia en pluviometros
#     distancias = []
#     for j, punto_referencia in eventos_seleccionados.iterrows():
#         distancia = evento.geometry.distance(punto_referencia.geometry)
#         distancias.append(distancia)

#     indice_punto_cercano = distancias.index(min(distancias))
#     punto_cercano = eventos_seleccionados.iloc[indice_punto_cercano]

#     resultados.append({'FICHA': evento.FICHA, 'PluvioAsociado': punto_cercano.codigo, 
#     "Acum_diario": punto_cercano.P1, "Acum_3dias": punto_cercano.acumulado_3_dias, 
#     "Acum_7dias": punto_cercano.acumulado_7_dias, "Acum_15dias": punto_cercano.acumulado_15_dias, 
#     "Acum_30dias": punto_cercano.acumulado_30_dias, "Acum_90dias": punto_cercano.acumulado_90_dias})
# resultados_df = pd.DataFrame(resultados)

# gdf= gdf.merge(resultados_df, on='FICHA')
# gdf=gdf.drop('Unnamed: 0', axis=1)

#%% Graficas choropleth
# gdf = gpd.sjoin(gdf, barrios, op='within')
# barrios_shapefile = barrios
# barrios_geojson = barrios


# # crear nuevo geodataframe con el número de eventos 'movimientos en masa' por barrio
# eventos_por_barrio = gdf[gdf['Evento'] == 'movimientos en masa'].groupby('NOMBRE').count()['Evento'].reset_index(name='NumEventos')


# # unir información de número de eventos con los límites de los barrios
# barrios_con_eventos = barrios_shapefile.merge(eventos_por_barrio, on='NOMBRE')

# barrios_con_eventos['popup_info'] = 'Barrio: ' + barrios_con_eventos['NOMBRE'] + '<br>' + 'Eventos de movimientos en masa: ' + barrios_con_eventos['NumEventos'].astype(str)

# def popup_content(row):
#     return row['popup_info']

# m = folium.Map(location=[6.25, -75.57], zoom_start=12)

# folium.GeoJson(
#     barrios_geojson,
#     name='Movimientos en masa',
#     style_function=lambda feature: {
#         'fillColor': 'YlOrRd',
#         'fillOpacity': 0.7,
#         'color': 'black',
#         'weight': 0.5,
#     },
#     tooltip=folium.GeoJsonTooltip(fields=['NOMBRE', 'NumEventos'], aliases=['Barrio', 'Eventos de movimientos en masa']),
#     popup=folium.GeoJsonPopup(fields=['popup_info'], aliases=['Información']),
#     highlight_function=lambda x: {'weight':3, 'color':'red', 'fillOpacity':0.5},
# ).add_to(m)


# # crear mapa choropleth con folium

# folium.Choropleth(
#     geo_data=barrios_geojson,
#     name='Movimientos en masa',
#     data=barrios_con_eventos,
#     columns=['NOMBRE', 'NumEventos'],
#     key_on='feature.properties.NOMBRE',
#     fill_color='YlOrRd',
#     fill_opacity=0.7,
#     line_opacity=0.2,
#     legend_name='Eventos de movimientos en masa por barrio'
# ).add_to(m)

# eventos_por_barrio_colapso = gdf[gdf['Evento'] == 'estructural'].groupby('NOMBRE').count()['Evento'].reset_index(name='NumEventos_colapso')

# # unir información de número de eventos con los límites de los barrios
# barrios_con_eventos_colapso = barrios_shapefile.merge(eventos_por_barrio_colapso, on='NOMBRE')

# # crear segundo choropleth map
# folium.Choropleth(
#     geo_data=barrios_geojson,
#     name='choropleth2',
#     data=barrios_con_eventos_colapso,
#     columns=['NOMBRE', 'NumEventos_colapso'],
#     key_on='feature.properties.NOMBRE',
#     fill_color='Greys',
#     fill_opacity=0.7,
#     line_opacity=0.2,
#     legend_name='Eventos de colapso estructural por barrio'
# ).add_to(m)

# eventos_por_barrio_inundacion = gdf[gdf['Evento'] == 'inundación'].groupby('NOMBRE').count()['Evento'].reset_index(name='NumEventos_inundacion')

# # unir información de número de eventos con los límites de los barrios
# barrios_con_eventos_inundacion = barrios_shapefile.merge(eventos_por_barrio_inundacion, on='NOMBRE')

# # crear segundo choropleth map
# folium.Choropleth(
#     geo_data=barrios_geojson,
#     name='Inundación',
#     data=barrios_con_eventos_inundacion,
#     columns=['NOMBRE', 'NumEventos_inundacion'],
#     key_on='feature.properties.NOMBRE',
#     fill_color='YlGnBu',
#     fill_opacity=0.7,
#     line_opacity=0.2,
#     legend_name='Eventos de inundación por barrio'
# ).add_to(m)

# # agregar control de capas para ambos choropleth maps
# folium.LayerControl().add_to(m)

# m

# %% choropleth interactivo


# cargar datos de eventos y barrios

barrios_shapefile = barrios

# convertir shapefile de barrios a formato geojson para usar con folium
barrios_geojson = barrios_shapefile.to_crs(epsg='4326').to_json()

# obtener número de eventos de cada tipo por barrio
eventos_por_barrio_mov = gdf[gdf['Evento'] == 'movimientos en masa'].groupby('NOMBRE').count()['Evento'].reset_index(name='NumEventos_mov')
eventos_por_barrio_col = gdf[gdf['Evento'] == 'estructural'].groupby('NOMBRE').count()['Evento'].reset_index(name='NumEventos_colapso')
eventos_por_barrio_inu = gdf[gdf['Evento'] == 'inundación'].groupby('NOMBRE').count()['Evento'].reset_index(name='NumEventos_inundacion')

# unir información de número de eventos con los límites de los barrios
barrios_con_eventos_mov = barrios_shapefile.merge(eventos_por_barrio_mov, on='NOMBRE')
barrios_con_eventos_col = barrios_shapefile.merge(eventos_por_barrio_col, on='NOMBRE')
barrios_con_eventos_inu = barrios_shapefile.merge(eventos_por_barrio_inu, on='NOMBRE')

#columna pop-up
barrios_con_eventos_mov['popup_info'] = 'Barrio: ' + barrios_con_eventos['NOMBRE'] + '<br>' + 'Eventos de movimientos en masa: ' + barrios_con_eventos['NumEventos'].astype(str)


# crear mapa base con folium
m = folium.Map(location=[6.25, -75.57], zoom_start=12)

# crear primer choropleth map
folium.Choropleth(
    geo_data=barrios_geojson,
    name='Movimientos en masa',
    data=barrios_con_eventos_mov,
    columns=['NOMBRE', 'NumEventos_mov'],
    key_on='feature.properties.NOMBRE',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Eventos de movimientos en masa por barrio'
).add_to(m)

def create_popup(barrio, num_eventos):
    popup_html = f'<b>Barrio:</b> {barrio}<br><b>Eventos:</b> {num_eventos}'
    return folium.Popup(popup_html, max_width=200)

# agregar pop-ups para cada barrio en el primer choropleth map
for _, row in barrios_con_eventos.iterrows():
    barrio = row['NOMBRE']
    num_eventos = row['NumEventos']
    popup = create_popup(barrio, num_eventos)
    folium.GeoJson(
        barrios_geojson['features'][barrios_geojson['features'].index
                                    (next(filter(lambda x: x['properties']['NOMBRE'] == barrio, barrios_geojson['features'])))]
        , tooltip=row['NOMBRE']
        , popup=popup
        , style_function=lambda x: {
            'fillColor': 'YlOrRd',
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.7
        }).add_to(m)
    


folium.LayerControl().add_to(m)

m




# %%
llamadas = gpd.read_file('/home/aospinau/Documents/Unal/AnlisisGeoespacial/GitHubGDS/fichasPrecicpitacionAcumulada3.geojson')
#%%
gdf=llamadas
#%%
gdf=gdf.to_crs(epsg='32619')
#%%
#pluviometros =gpd.read_file('PluvioSIATA_EPM_Diario.geojson')
#%%
barrios = gpd.read_file('/home/aospinau/Documents/Unal/AnlisisGeoespacial/GitHubGDS/planeacion_gdb.geojson')

#%%

quebradas = gpd.read_file('/home/aospinau/Documents/Unal/AnlisisGeoespacial/GitHubGDS/RedHidricaMedellin.geojson')

#%% Elimina ubicaciones repetinas n veces
# gdf['geom_str'] = gdf.geometry.apply(lambda x: str(x))
# counts = gdf.groupby('geom_str').size().reset_index(name='count')
# n = 50
# unique_gdf = gdf.loc[gdf['geom_str'].isin(counts.loc[counts['count'] < n, 'geom_str'])]
# gdf = unique_gdf

#Elimina fichas clasificadas como no ubicadas

#gdf = gdf.drop(gdf[gdf['Tipo'].str.contains('NO UBICADA')].index)

#%% Todas las fichas caracterizadas en alto, medio bajo o emergencia
# gdf['Prioridad'] = gdf['Prioridad'].replace(to_replace=r'^baj.*', value='baja', regex=True)
# gdf['Prioridad'] = gdf['Prioridad'].replace(to_replace=r'^med.*', value='media', regex=True)
# gdf['Prioridad'] = gdf['Prioridad'].replace(to_replace=r'^alt.*', value='alta', regex=True)
# gdf['Prioridad'] = gdf['Prioridad'].replace(to_replace=r'^emer.*', value='emergencia', regex=True)


# gdf['TipoEvento'] = gdf['Evento']

# gdf['TipoEvento'] = gdf['TipoEvento'].replace(to_replace=r'^alte.*', value='otros eventos', regex=True)
# gdf['TipoEvento'] = gdf['TipoEvento'].replace(to_replace=r'^tecno.*', value='otros eventos', regex=True)
# gdf['TipoEvento'] = gdf['TipoEvento'].replace(to_replace=r'^epid.*', value='otros eventos', regex=True)
# gdf['TipoEvento'] = gdf['TipoEvento'].replace(to_replace=r'^natur.*', value='otros eventos', regex=True)
# gdf['TipoEvento'] = gdf['TipoEvento'].replace(to_replace=r'^explo.*', value='otros eventos', regex=True)


# gdf['año'] = gdf['fecha'].dt.year
# gdf['mes'] = gdf['fecha'].dt.month
#


#%% Mapa presentación de datos
fig, ax = plt.subplots(1, figsize=(9, 9))

# Plot de los eventos
gdf.plot(column="TipoEvento",
         legend=True,
         alpha=0.7,
         ax=ax
        )

# Agregar capa de polígonos de barrios
barrios.plot(ax=ax, facecolor="none", edgecolor="black", alpha=0.5)

# Agregar mapa base
cx.add_basemap(ax,
               crs=gdf.crs.to_string(),
               source=cx.providers.Stamen.TerrainBackground,
               alpha=0.8
              )

ax.set_title("Mapa de eventos de riesgo reportados")

# Agregar barra de escala manualmente
scale = 1000  # Longitud en metros
scalebar_length = 0.1  # Longitud en la figura

xmin, xmax, ymin, ymax = ax.axis()
ax_length = xmax - xmin
ax_height = ymax - ymin

scalebar_x = xmax - scalebar_length * ax_length
scalebar_y = ymin + 0.05 * ax_height

ax.plot([scalebar_x, xmax], [scalebar_y, scalebar_y], color='k', linewidth=3)
ax.text((scalebar_x + xmax) / 2, scalebar_y - 0.03 * ax_height, f"{scale} m", ha='center')

north_arrow = cx.add_basemap(ax,
                             zoom=13,
                             crs=gdf.crs.to_string(),
                             source=cx.providers.Stamen.TerrainBackground,
                             alpha=0.8
                            )

plt.show()

# %% Lluvia para histogramas

Pluviometros=pluviometros
Pluviometros['mes'] = Pluviometros['fecha'].dt.month
Pluviometros['año'] = Pluviometros['fecha'].dt.year
Pluviometros = Pluviometros[Pluviometros['año'] >= Pluviometros['año'].max() - 20]

lluviaMensual = Pluviometros.groupby(['mes', 'año', 'codigo']).sum()
promedio_mensual = lluviaMensual.groupby('mes')['P1'].mean()
prom_mensual=pd.DataFrame(promedio_mensual)
data = {'mes': prom_mensual.index.to_list(),
        'P1': prom_mensual.P1.to_list()}

prom = pd.DataFrame(data)

lluviaanual = Pluviometros.groupby(['año', 'codigo']).sum()

prom_anual=lluviaanual.groupby('año')['P1'].mean()

prom_anual=pd.DataFrame(prom_anual)
dataA = {'año': prom_anual.index.to_list(),
        'P1': prom_anual.P1.to_list()}

promA = pd.DataFrame(dataA)

promA = promA.drop(promA.index[0])

promA=promA.reset_index()

# %% Histograma mensual
eventos_por_mes = gdf.groupby(['mes', 'TipoEvento']).size().reset_index(name='count')


fig, ax1 = plt.subplots(figsize=(10,5))

eventos_por_mes.pivot(index='mes', columns='TipoEvento', values='count').plot(kind='bar', stacked=True, ax=ax1)

ax2=plt.twinx()
ax2.plot(prom['P1'], label=u'Lluvia', lw=2, ls='--', color='yellow')


#prom.plot(kind='line', x='mes', y='P1', color='green', ax=ax2)

ax1.set_xlabel('Mes')
ax1.set_ylabel('Número de Eventos')
ax2.set_ylabel('Lluvia (mm)')

ax1.set_title('Histograma de Eventos por Mes y Lluvia Media en Medellín')

ax1.legend(title='Tipo de Evento', bbox_to_anchor=(1.05, 1.05))
ax2.legend(['Lluvia'])

plt.show()

# %% Histograma anual

# Agrupar los eventos por año y tipo de evento
eventos_por_año = gdf.groupby(['año', 'TipoEvento']).size().reset_index(name='count')


# Crear el histograma
fig, ax1 = plt.subplots(figsize=(10,5))
eventos_por_año.pivot(index='año', columns='TipoEvento', values='count').plot(kind='bar', stacked=True, ax=ax1)

ax2=plt.twinx()
ax2.plot(promA['P1'], label=u'Lluvia', lw=2, ls='--', color='yellow')


ax1.set_xlabel('Año')
ax1.set_ylabel('Número de Eventos')
ax2.set_ylabel('Lluvia (mm)')

ax1.set_title('Histograma de Eventos por Año y Lluvia Media en Medellín')

ax1.legend(title='Tipo de Evento', bbox_to_anchor=(1.35, 1.05))
ax2.legend(['Lluvia'])#bbox_to_anchor=(1.37, 0.7))

plt.show()

#%% Mapa de histogramas laterales
joint_axes = sns.jointplot(x='Longitud', y='Latitud', data=gdf, s=0.5)
# Add dark basemap
cx.add_basemap(
    joint_axes.ax_joint,
    crs="EPSG:4326",
    source=cx.providers.Stamen.TonerLite
);
# %% Mapa de pluviometros asociados
#pluviometros usados
pluvio=pluviometros.drop_duplicates(subset='codigo', keep='first')
pluvio['codigo'] = pluvio['codigo'].astype(str)


# Crear una lista de valores
valores_a_mantener = ['2701045', '2701481', '2701485', '2701517', '2701046', '2701038',
       '2701093', '2701114', '2701035', '2701115', '2308023', '7', '27',
       '49', '48', '17', '16', '1', '53', '8', '28', '46', '39', '12',
       '44', '22', '40', '55', '14', '54', '35', '24', '56', '9', '41',
       '23', '26', '42', '15', '3', '45', '18', '5', '60', '11', '71',
       '211', '29', '81', '4', '2', '89', '129', '20', '184', '242',
       '274', '241', '189', '289', '10', '21', '311', '352', '353', '376',
       '378', '356', '393', '394', '429', '418', '456', '434', '445',
       '447', '446', '320', '499', '551', '558', '575', '578', '612',
       '601', '25']

# Filtrar el DataFrame
pluvio = pluvio[pluvio['codigo'].isin(valores_a_mantener)]


gdf['PluvioAsociado'] = gdf['PluvioAsociado'].astype(str)


fig, ax = plt.subplots(1, figsize=(9, 9))

# Plot de los eventos
gdf.plot(column="PluvioAsociado",
         legend=False,
         alpha=0.4,
         cmap='Paired',
         ax=ax
        )

# Agregar capa de polígonos de barrios
barrios.plot(ax=ax, facecolor="none", edgecolor="black", alpha=0.5)

pluvio.plot(ax=ax, color='yellow', markersize=20, edgecolor="black", label='Pluviómetros')

ax.legend(loc='upper right')

ax.set_title("Mapa de pluviómetros asociados a eventos")
             
# Agregar mapa base
cx.add_basemap(ax,
               crs=gdf.crs.to_string(),
               source=cx.providers.Stamen.TerrainBackground,
               alpha=0.8
              )

# for i, row in pluvio.iterrows():
#     bbox_props = dict(boxstyle="square", facecolor="white", edgecolor="none", alpha=0.4)
#     ax.text(row['geometry'].x, row['geometry'].y, row['codigo'], color='black', bbox=bbox_props, fontsize=8)

# Agregar barra de escala manualmente
scale = 1000  # Longitud en metros
scalebar_length = 0.1  # Longitud en la figura

xmin, xmax, ymin, ymax = ax.axis()
ax_length = xmax - xmin
ax_height = ymax - ymin

scalebar_x = xmax - scalebar_length * ax_length
scalebar_y = ymin + 0.05 * ax_height

ax.plot([scalebar_x, xmax], [scalebar_y, scalebar_y], color='k', linewidth=3)
ax.text((scalebar_x + xmax) / 2, scalebar_y - 0.03 * ax_height, f"{scale} m", ha='center')

plt.show()


#%% Choropleths interactivos
# Carga el GeoDataFrame de eventos
gdf_eventos = gdf

# Carga el GeoDataFrame de polígonos de barrios
gdf_barrios = barrios

# Realiza la unión espacial entre eventos y barrios
eventos_barrios_gdf = gpd.sjoin(gdf_eventos, gdf_barrios, op='within')

# Agrupa los eventos por barrio y tipo de evento, y cuenta el número de eventos por tipo en cada barrio
eventos_por_barrio = eventos_barrios_gdf.groupby(['NOMBRE', 'TipoEvento']).size().unstack(fill_value=0).reset_index()

# Fusiona el GeoDataFrame de barrios con los datos del número de eventos por tipo y barrio
barrios_con_eventos = gdf_barrios.merge(eventos_por_barrio, on='NOMBRE', how='left')


#%%
# Crea el mapa centrado en Medellín
mapa = folium.Map(location=[6.244203, -75.581211], zoom_start=12)

# Función para generar el contenido del cuadro emergente
def popup_content(row):
    content = "<strong>Barrio:</strong> " + row['NOMBRE'] + "<br>"
    content += "<strong>Eventos estructurales:</strong> " + str(row['estructural']) + "<br>"
    content += "<strong>Eventos movimientos en masa:</strong> " + str(row['movimientos en masa']) + "<br>"
    content += "<strong>Eventos inundación:</strong> " + str(row['inundación']) + "<br>"
    content += "<strong>Eventos incendio:</strong> " + str(row['incendio']) + "<br>"
    content += "<strong>Eventos humedad:</strong> " + str(row['humedades']) + "<br>"
    content += "<strong>Otros eventos:</strong> " + str(row['otros eventos']) + "<br>"
    return content


    
# Capa de eventos estructurales
barrios_con_eventos_estructurales = barrios_con_eventos[['NOMBRE', 'estructural', 'geometry']]
choropleth_estructurales = folium.Choropleth(
    geo_data=barrios_con_eventos_estructurales,
    data=barrios_con_eventos_estructurales,
    columns=['NOMBRE', 'estructural'],
    key_on='feature.properties.NOMBRE',
    fill_color='Greens',
    fill_opacity=0.9,
    line_opacity=0.2,
    legend_name='Número de eventos estructurales por barrio',
    name='Eventos estructurales'
).add_to(mapa)

# Capa de eventos de movimientos en masa
barrios_con_eventos_movimientos = barrios_con_eventos[['NOMBRE', 'movimientos en masa', 'geometry']]
choropleth_movimientos = folium.Choropleth(
    geo_data=barrios_con_eventos_movimientos,
    data=barrios_con_eventos_movimientos,
    columns=['NOMBRE', 'movimientos en masa'],
    key_on='feature.properties.NOMBRE',
    fill_color='Oranges',
    fill_opacity=0.9,
    line_opacity=0.2,
    legend_name='Número de eventos de movimientos en masa por barrio',
    name='Eventos de movimientos en masa'
).add_to(mapa)

# Capa de eventos de movimientos en masa
barrios_con_eventos_movimientos = barrios_con_eventos[['NOMBRE', 'inundación', 'geometry']]
choropleth_movimientos = folium.Choropleth(
    geo_data=barrios_con_eventos_movimientos,
    data=barrios_con_eventos_movimientos,
    columns=['NOMBRE', 'inundación'],
    key_on='feature.properties.NOMBRE',
    fill_color='Blues',
    fill_opacity=0.9,
    line_opacity=0.2,
    legend_name='Número de eventos de inundación',
    name='Eventos de inunadción'
).add_to(mapa)

barrios_con_eventos_movimientos = barrios_con_eventos[['NOMBRE', 'otros eventos', 'geometry']]
choropleth_movimientos = folium.Choropleth(
    geo_data=barrios_con_eventos_movimientos,
    data=barrios_con_eventos_movimientos,
    columns=['NOMBRE', 'otros eventos'],
    key_on='feature.properties.NOMBRE',
    fill_color='Greys',
    fill_opacity=0.9,
    line_opacity=0.2,
    legend_name='Número de otros eventos',
    name='Otros eventos'
).add_to(mapa)

barrios_con_eventos_movimientos = barrios_con_eventos[['NOMBRE', 'incendio', 'geometry']]
choropleth_movimientos = folium.Choropleth(
    geo_data=barrios_con_eventos_movimientos,
    data=barrios_con_eventos_movimientos,
    columns=['NOMBRE', 'incendio'],
    key_on='feature.properties.NOMBRE',
    fill_color='Purples',
    fill_opacity=0.9,
    line_opacity=0.2,
    legend_name='Número de eventos incendio',
    name='Eventos de incendio'
).add_to(mapa)

barrios_con_eventos_movimientos = barrios_con_eventos[['NOMBRE', 'humedades', 'geometry']]
choropleth_movimientos = folium.Choropleth(
    geo_data=barrios_con_eventos_movimientos,
    data=barrios_con_eventos_movimientos,
    columns=['NOMBRE', 'humedades'],
    key_on='feature.properties.NOMBRE',
    fill_color='OrRd',
    fill_opacity=0.9,
    line_opacity=0.2,
    legend_name='Número de eventos por humedades',
    name='Eventos de humedades'
).add_to(mapa)

for _, row in barrios_con_eventos.iterrows():
    folium.GeoJson(
        row['geometry'],
        style_function=lambda x: {'fillColor': '#YlOrRd', 'fillOpacity': 0.1, 'color': '#000000', 'line_opacity': 0.01, 'line_weight': 0.5},
        tooltip=row['NOMBRE'],
        popup=folium.Popup(popup_content(row), max_width=300)
    ).add_to(mapa)



# Agrega los polígonos de barrios con el número de eventos como datos


# Control de capas
folium.LayerControl().add_to(mapa)


# Guarda el mapa como un archivo HTML
mapa.save('mapa_interactivo_con_control_de_capas.html')

# %% Amenaza alta

gdf_alta=gdf[(gdf['Prioridad'] == 'alta') | (gdf['Prioridad'] == 'emergencia')]
df_MM = gdf_alta[gdf_alta['TipoEvento'] == 'movimientos en masa']
df_Est = gdf_alta[gdf_alta['TipoEvento'] == 'estructural']
df_Inun = gdf_alta[gdf_alta['TipoEvento'] == 'inundación']

#%% Mapas de densidad de kernel
barrios= barrios #capa de poligonos que quieres agregar al mapa
df_MM2 = gdf[gdf['TipoEvento'] == 'movimientos en masa'] #capa de puntos (geodataframe)

# Create a figure and axes object
fig, ax = plt.subplots(ncols=1, figsize=(10, 8))

levels = [0.1,0.3,0.5,0.7,0.9,1]

# Plot df_MM2 on the second axes object
kde = sns.kdeplot(
    ax=ax[0],
    x=df_MM2['geometry'].x,
    y= df_MM2['geometry'].y,
    levels = levels,
    shade=True,
    cmap='Reds',
    alpha=0.8,
    cbar=True
)

df_MM2.plot(ax=ax[0], color='black', markersize=1, alpha=0.03)
barrios.plot(ax=ax[0], edgecolor='black', facecolor='none')
cx.add_basemap(ax=ax[0],crs = df_MM.crs.to_string(), source=cx.providers.CartoDB.Positron)  #mapa base de contextily
ax[0].set_axis_off()

ax[0].set_title('Densidad de Kernel para eventos de movimientos en masa')

# Plot df_MM on the first axes object
kde = sns.kdeplot(
    ax=ax[1],
    x=df_MM['geometry'].x,
    y= df_MM['geometry'].y,
    levels = levels,
    shade=True,
    cmap='Reds',
    alpha=0.8,
    cbar=True
)

# Add a basemap
df_MM.plot(ax=ax[1], color='black', markersize=2, alpha=1)
barrios.plot(ax=ax[1], edgecolor='black', facecolor='none', alpha=0.5)
cx.add_basemap(ax=ax[1],crs = df_MM.crs.to_string(), source=cx.providers.CartoDB.Positron)
ax[1].set_axis_off()

ax[1].set_title('Densidad de Kernel para eventos de movimientos en masa con prioridad alta o emergencia')

ax[0].set_xlim(ax[1].get_xlim())
ax[0].set_ylim(ax[1].get_ylim())

# # Tighten the layout
plt.tight_layout()

# # Show the plot
# plt.show()

# #%%

df_Est = df_Est
df_Est2 = gdf[gdf['TipoEvento'] == 'estructural']

fig, ax = plt.subplots(ncols=2, figsize=(20, 8))



# Plot df_MM2 on the second axes object
kde = sns.kdeplot(
    ax=ax[0],
    x=df_Est2['geometry'].x,
    y= df_Est2['geometry'].y,
    levels = levels,
    shade=True,
    cmap='Greens',
    alpha=0.8,
    cbar=True
)
ax[0].set_title('Densidad de Kernel para eventos estructurales')
# Add a basemap
df_Est2.plot(ax=ax[0], color='black', markersize=1, alpha=0.03)

barrios.plot(ax=ax[0], edgecolor='black', facecolor='none', alpha=0.5)
cx.add_basemap(ax=ax[0],crs = df_MM.crs.to_string(), source=cx.providers.CartoDB.Positron)
ax[0].set_axis_off()

# Plot df_MM on the first axes object
kde = sns.kdeplot(
    ax=ax[1],
    x=df_Est['geometry'].x,
    y= df_Est['geometry'].y,
    levels = levels,
    shade=True,
    cmap='Greens',
    alpha=0.8,
    cbar=True
)

# Add a basemap

df_Est.plot(ax=ax[1], color='black', markersize=2, alpha=1)

barrios.plot(ax=ax[1], edgecolor='black', facecolor='none')
cx.add_basemap(ax=ax[1],crs = df_MM.crs.to_string(), source=cx.providers.CartoDB.Positron)
ax[1].set_axis_off()

ax[1].set_title('Densidad de Kernel para eventos estructurales de alta prioridad o emergencia')


ax[0].set_xlim(ax[1].get_xlim())
ax[0].set_ylim(ax[1].get_ylim())


plt.tight_layout()

df_Inun = df_Inun
df_Inun2 = gdf[gdf['TipoEvento'] == 'inundación']

fig, ax = plt.subplots(ncols=2, figsize=(20, 8))



# Plot df_MM2 on the second axes object
kde = sns.kdeplot(
    ax=ax[0],
    x=df_Inun2['geometry'].x,
    y= df_Inun2['geometry'].y,
    levels = levels,
    shade=True,
    cmap='Blues',
    alpha=0.8,
    cbar=True
)
ax[0].set_title('Densidad de Kernel para eventos de inundación')
# Add a basemap

df_Inun2.plot(ax=ax[0], color='black', markersize=2, alpha=0.5)

barrios.plot(ax=ax[0], edgecolor='black', facecolor='none')
cx.add_basemap(ax=ax[0],crs = df_MM.crs.to_string(), source=cx.providers.CartoDB.Positron)
ax[0].set_axis_off()

# Plot df_MM on the first axes object
kde = sns.kdeplot(
    ax=ax[1],
    x=df_Inun['geometry'].x,
    y= df_Inun['geometry'].y,
    levels = levels,
    shade=True,
    cmap='Blues',
    alpha=0.8,
    cbar=True
)

# Add a basemap

df_Inun.plot(ax=ax[1], color='black', markersize=4, alpha=1)


barrios.plot(ax=ax[1], edgecolor='black', facecolor='none')
cx.add_basemap(ax=ax[1],crs = df_MM.crs.to_string(), source=cx.providers.CartoDB.Positron)
ax[1].set_axis_off()

ax[1].set_title('Densidad de Kernel para eventos de inundación de alta prioridad o emergencia')


ax[0].set_xlim(ax[1].get_xlim())
ax[0].set_ylim(ax[1].get_ylim())


# Tighten the layout
plt.tight_layout()


# %% indice de moran 1

import geopandas as gpd
import libpysal
from esda.moran import Moran_Local
from pysal.explore import esda

from pysal.viz import splot
from splot.esda import plot_moran

df2=gdf[gdf['TipoEvento'] == 'movimientos en masa']
# Cargar el GeoDataFrame desde tu archivo o fuente de datos
gdf2 = df2[(df2['Prioridad'] == 'alta') | (df2['Prioridad'] == 'emergencia')]

# Crear un objeto de pesos espaciales utilizando el método de vecinos más cercanos
w = libpysal.weights.KNN.from_dataframe(gdf2, k=1)

mi = esda.Moran(gdf2['Acum_30dias'], w)
plot_moran(mi);


mi.I
# %% indice Moran



import geopandas as gpd
import libpysal
from esda.moran import Moran_Local
from pysal.explore import esda

from pysal.viz import splot
from splot.esda import plot_moran

#crea una columna  si es movimiento en masa y otra si es estructural
gdf['EsMM'] = gdf.apply(lambda row: 1 if row['TipoEvento'] == 'movimientos en masa' else 0, axis=1)
gdf['EsEstructural'] = gdf.apply(lambda row: 1 if row['TipoEvento'] == 'estructural' else 0, axis=1)

gdf['DEF_N'] = gdf['DEF'].apply(lambda x: 0 if x == 0 else 1)


df_MM2 = gdf[gdf['TipoEvento'] == 'movimientos en masa']
df_Est2 = gdf[gdf['TipoEvento'] == 'estructural']


gdf_alta=gdf[(gdf['Prioridad'] == 'alta') | (gdf['Prioridad'] == 'emergencia')]
df_MM = gdf_alta[gdf_alta['TipoEvento'] == 'movimientos en masa']
df_Est = gdf_alta[gdf_alta['TipoEvento'] == 'estructural']
df_Inun = gdf_alta[gdf_alta['TipoEvento'] == 'inundación']

# Cargar el GeoDataFrame desde tu archivo o fuente de datos
df = df_MM.to_crs(epsg='32619') # Puntos

# Crear un objeto de pesos espaciales utilizando el método de vecinos más cercanos
w = libpysal.weights.KNN.from_dataframe(df, k=5)  # Ajusta el valor de "k" según tus necesidades

capa = 'Acum_3dias'

# Extraer los valores de interés para el análisis (por ejemplo, una columna de datos numéricos)
your_data = df[capa]

# Crear un objeto de análisis del Índice de Moran local
moran_loc = Moran_Local(your_data, w)

# Acceder a los resultados del análisis
local_moran_values = moran_loc.Is
p_values = moran_loc.p_sim

# Agregar los resultados al GeoDataFrame
df[f'Local Moran Index {capa}'] = local_moran_values
df[f'P-value {capa}'] = p_values


# Imprimir los resultados
print(df[[f'Local Moran Index {capa}', f'P-value {capa}']])

ax = df.plot(column=f'Local Moran Index {capa}', cmap='seismic', legend=True, alpha=0.4, vmin=-10, vmax=10)

# Agregar un mapa base
cx.add_basemap(ax,crs=df.crs.to_string(), source=cx.providers.CartoDB.Positron)

# Agregar una barra de escala
scale_bar = AnchoredSizeBar(ax.transData, 10000, '10 km', loc='lower right')
ax.add_artist(scale_bar)

# Muestra el gráfico
plt.show()

w = libpysal.weights.KNN.from_dataframe(df, k=10)

mi = esda.Moran(df[capa], w)
plot_moran(mi)

gdf_moran = df[df[f'Local Moran Index {capa}'] > 1.5]

print(f'{capa}')



# %% Caracterizar por prioridad y evento
gdf_alta=gdf[(gdf['Prioridad'] == 'alta') | (gdf['Prioridad'] == 'emergencia')]
df_MM = gdf_alta[gdf_alta['Evento'] == 'movimientos en masa']
df_Est = gdf_alta[gdf_alta['Evento'] == 'estructural']
df_Inun = gdf_alta[gdf_alta['Evento'] == 'inundación']

#%% #Cluster MM


gdf_Alto= df_MM
gdf_Alto=gdf_Alto.to_crs(epsg='32619')
# Assuming you have a GeoDataFrame called 'gdf' with a 'geometry' column containing the point geometries

# Extract the coordinates from the GeoDataFrame
coords = gdf_Alto['geometry'].apply(lambda geom: (geom.x, geom.y)).tolist()

# Define the parameters for DBSCAN
eps = 500  # Neighborhood radius
min_samples = 10  # Minimum number of points to form a cluster

# Apply DBSCAN
dbscan = DBSCAN(eps=eps, min_samples=min_samples)
clusters = dbscan.fit_predict(coords)

# Add the clustering results as a new column to the GeoDataFrame
gdf_Alto['cluster'] = clusters
barrios2=barrios.to_crs(epsg='32619')
# Assuming you have a GeoDataFrame called 'gdf_Alto' with a 'cluster' column

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

barrios2.plot(ax=ax, edgecolor='black', facecolor='none', alpha=0.3)
# Plot the clusters
gdf_Alto.plot(ax=ax, column='cluster', cmap='Paired', markersize=20, legend=True)


# Add a scale bar
scale_bar = AnchoredSizeBar(ax.transData, 10000, '10 km', loc='lower right')
ax.add_artist(scale_bar)

# Add a north arrow
ax.text(0.02, 0.98, 'N', transform=ax.transAxes, fontsize=16, ha='center', va='center')

# Add a basemap
cx.add_basemap(ax, crs=gdf_Alto.crs.to_string(), source=cx.providers.CartoDB.Positron)

# Set the axis limits
ax.set_xlim(gdf_Alto.total_bounds[0], gdf_Alto.total_bounds[2])
ax.set_ylim(gdf_Alto.total_bounds[1], gdf_Alto.total_bounds[3])

plt.title('Clusterización mediante DBScan. \n Radio=200 m, minimo 5 eventos de movimientos en masa.')
# Show the plot

plt.tight_layout()

plt.show()

#%%

# Cargar el GeoDataFrame de tus puntos
gdf_cluster=gdf_Alto[gdf_Alto['cluster']==10]

# Crear la figura y los ejes
fig, ax = plt.subplots(figsize=(10, 10))

# Plotear los puntos
gdf_cluster.plot(ax=ax, column='cluster', color='red', markersize=30, legend=True)
scale_bar = AnchoredSizeBar(ax.transData, 200, '200 m', loc='lower right')
ax.add_artist(scale_bar)

ax.set_title('Cluster caracterizado mediante DBScan. \n Cluster barrio Olaya Herrera, occidente de Medellín')

ax.annotate('N', xy=(0.1, 0.97), xycoords='axes fraction', fontsize=16,
            ha='center', va='center', annotation_clip=False,
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='black'))
# Agregar el mapa base con ortofoto
cx.add_basemap(ax, crs=gdf_cluster.crs.to_string(), source=cx.providers.Esri.WorldImagery)

# # Ajustar los límites de los ejes
# ax.set_xlim(gdf_cluster.total_bounds[0], gdf_cluster.total_bounds[2])
# ax.set_ylim(gdf_cluster.total_bounds[1], gdf_cluster.total_bounds[3])

# Mostrar el gráfico

plt.tight_layout()

plt.show()

# %% Cluster Estructural

gdf_Alto= df_Est
gdf_Alto=gdf_Alto.to_crs(epsg='32619')
# Assuming you have a GeoDataFrame called 'gdf' with a 'geometry' column containing the point geometries

# Extract the coordinates from the GeoDataFrame
coords = gdf_Alto['geometry'].apply(lambda geom: (geom.x, geom.y)).tolist()

# Define the parameters for DBSCAN
eps = 500  # Neighborhood radius
min_samples = 10  # Minimum number of points to form a cluster

# Apply DBSCAN
dbscan = DBSCAN(eps=eps, min_samples=min_samples)
clusters = dbscan.fit_predict(coords)

# Add the clustering results as a new column to the GeoDataFrame
gdf_Alto['cluster'] = clusters


barrios2=barrios.to_crs(epsg='32619')
#quebradas2=quebradas.to_crs(epsg='32619')
# Assuming you have a GeoDataFrame called 'gdf_Alto' with a 'cluster' column

# Create the plot
fig, ax = plt.subplots(figsize=(10,6))

barrios2.plot(ax=ax, edgecolor='black', facecolor='none', alpha=0.3)
# Plot the clusters
gdf_Alto.plot(ax=ax, column='cluster', cmap='Paired', markersize=20, legend=True)


# Add a scale bar
scale_bar = AnchoredSizeBar(ax.transData, 10000, '10 km', loc='lower right')
ax.add_artist(scale_bar)

# Add a north arrow
ax.text(0.02, 0.98, 'N', transform=ax.transAxes, fontsize=16, ha='center', va='center')

# Add a basemap
cx.add_basemap(ax, crs=gdf_Alto.crs.to_string(), source=cx.providers.CartoDB.Positron)

# Set the axis limits
ax.set_xlim(gdf_Alto.total_bounds[0], gdf_Alto.total_bounds[2])
ax.set_ylim(gdf_Alto.total_bounds[1], gdf_Alto.total_bounds[3])

plt.title('Clusterización mediante DBScan. \n Radio=200 m, minimo 5 eventos estructurales.')
# Show the plot

plt.tight_layout()

plt.show()

#%%
# Cargar el GeoDataFrame de tus puntos
gdf_cluster=gdf_Alto[gdf_Alto['cluster']==16]

# Crear la figura y los ejes
fig, ax = plt.subplots(figsize=(7, 7))

# Plotear los puntos
quebradas2.plot(ax=ax, edgecolor='blue', facecolor='none', alpha=1, linewidth=2, label='Quebradas')

gdf_cluster.plot(ax=ax, column='cluster', color='red', markersize=30, legend=True, label='Eventos')
scale_bar = AnchoredSizeBar(ax.transData, 200, '200 m', loc='lower right')
ax.add_artist(scale_bar)

ax.set_title('Cluster caracterizado mediante DBScan. \n Cluster barrio Robledo Kenedy, occidente de Medellín')

ax.annotate('N', xy=(0.1, 0.97), xycoords='axes fraction', fontsize=16,
            ha='center', va='center', annotation_clip=False,
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='black'))
# Agregar el mapa base con ortofoto

# # Ajustar los límites de los ejes
ax.set_xlim(gdf_cluster.total_bounds[0], gdf_cluster.total_bounds[2])
ax.set_ylim(gdf_cluster.total_bounds[1], gdf_cluster.total_bounds[3])

ax.legend()

cx.add_basemap(ax, crs=gdf_cluster.crs.to_string(), source=cx.providers.Esri.WorldImagery)

# Mostrar el gráfico

plt.tight_layout()

plt.show()

# %% Boxplot por cluster

grouped = gdf_Alto.groupby('cluster')

# Crear una lista vacía para almacenar los datos de lluvia por cluster
rain_data = []

# Iterar sobre cada grupo y extraer los valores de lluvia
for _, group in grouped:
    rain_values = group['Acum_diario'].values
    rain_data.append(rain_values)

# Crear la figura y los ejes del boxplot
fig, ax = plt.subplots(figsize=(10, 6))

# Crear el boxplot con los datos de lluvia por cluster
ax.boxplot(rain_data)

# Configurar las etiquetas del eje x con los nombres de los clusters
cluster_labels = grouped.groups.keys()
ax.set_xticklabels(cluster_labels)

# Agregar etiquetas y título al gráfico
ax.set_xlabel('Cluster')
ax.set_ylabel('Lluvia')
ax.set_title('Boxplot de lluvia diaria por cluster')

# Mostrar el gráfico
plt.show()

fig.savefig('/home/aospinau/Documents/Unal/AnlisisGeoespacial/FigurasProyecto/Boxplot_diaria.png', dpi=300, bbox_inches='tight')


grouped = gdf_Alto.groupby('cluster')

# Crear una lista vacía para almacenar los datos de lluvia por cluster
rain_data = []

# Iterar sobre cada grupo y extraer los valores de lluvia
for _, group in grouped:
    rain_values = group['Acum_3dias'].values
    rain_data.append(rain_values)

# Crear la figura y los ejes del boxplot
fig, ax = plt.subplots(figsize=(10, 6))

# Crear el boxplot con los datos de lluvia por cluster
ax.boxplot(rain_data)

# Configurar las etiquetas del eje x con los nombres de los clusters
cluster_labels = grouped.groups.keys()
ax.set_xticklabels(cluster_labels)

# Agregar etiquetas y título al gráfico
ax.set_xlabel('Cluster')
ax.set_ylabel('Lluvia')
ax.set_title('Boxplot de lluvia de 3 días antecedentes por cluster')

# Mostrar el gráfico
plt.show()

fig.savefig('/home/aospinau/Documents/Unal/AnlisisGeoespacial/FigurasProyecto/Boxplot_3dias.png', dpi=300, bbox_inches='tight')

grouped = gdf_Alto.groupby('cluster')

# Crear una lista vacía para almacenar los datos de lluvia por cluster
rain_data = []

# Iterar sobre cada grupo y extraer los valores de lluvia
for _, group in grouped:
    rain_values = group['Acum_7dias'].values
    rain_data.append(rain_values)

# Crear la figura y los ejes del boxplot
fig, ax = plt.subplots(figsize=(10, 6))

# Crear el boxplot con los datos de lluvia por cluster
ax.boxplot(rain_data)

# Configurar las etiquetas del eje x con los nombres de los clusters
cluster_labels = grouped.groups.keys()
ax.set_xticklabels(cluster_labels)

# Agregar etiquetas y título al gráfico
ax.set_xlabel('Cluster')
ax.set_ylabel('Lluvia')
ax.set_title('Boxplot de lluvia de 7 días antecedentes por cluster')

# Mostrar el gráfico
plt.show()

fig.savefig('/home/aospinau/Documents/Unal/AnlisisGeoespacial/FigurasProyecto/Boxplot_7dias.png', dpi=300, bbox_inches='tight')

grouped = gdf_Alto.groupby('cluster')

# Crear una lista vacía para almacenar los datos de lluvia por cluster
rain_data = []

# Iterar sobre cada grupo y extraer los valores de lluvia
for _, group in grouped:
    rain_values = group['Acum_15dias'].values
    rain_data.append(rain_values)

# Crear la figura y los ejes del boxplot
fig, ax = plt.subplots(figsize=(10, 6))

# Crear el boxplot con los datos de lluvia por cluster
ax.boxplot(rain_data)

# Configurar las etiquetas del eje x con los nombres de los clusters
cluster_labels = grouped.groups.keys()
ax.set_xticklabels(cluster_labels)

# Agregar etiquetas y título al gráfico
ax.set_xlabel('Cluster')
ax.set_ylabel('Lluvia')
ax.set_title('Boxplot de lluvia de 15 días antecedentes por cluster')

# Mostrar el gráfico
plt.show()

fig.savefig('/home/aospinau/Documents/Unal/AnlisisGeoespacial/FigurasProyecto/Boxplot_15dias.png', dpi=300, bbox_inches='tight')

grouped = gdf_Alto.groupby('cluster')

# Crear una lista vacía para almacenar los datos de lluvia por cluster
rain_data = []

# Iterar sobre cada grupo y extraer los valores de lluvia
for _, group in grouped:
    rain_values = group['Acum_30dias'].values
    rain_data.append(rain_values)

# Crear la figura y los ejes del boxplot
fig, ax = plt.subplots(figsize=(10, 6))

# Crear el boxplot con los datos de lluvia por cluster
ax.boxplot(rain_data)

# Configurar las etiquetas del eje x con los nombres de los clusters
cluster_labels = grouped.groups.keys()
ax.set_xticklabels(cluster_labels)

# Agregar etiquetas y título al gráfico
ax.set_xlabel('Cluster')
ax.set_ylabel('Lluvia')
ax.set_title('Boxplot de lluvia de 30 días antecedentes por cluster')

# Mostrar el gráfico
plt.show()

fig.savefig('/home/aospinau/Documents/Unal/AnlisisGeoespacial/FigurasProyecto/Boxplot_30dias.png', dpi=300, bbox_inches='tight')

grouped = gdf_Alto.groupby('cluster')

# Crear una lista vacía para almacenar los datos de lluvia por cluster
rain_data = []

# Iterar sobre cada grupo y extraer los valores de lluvia
for _, group in grouped:
    rain_values = group['Acum_90dias'].values
    rain_data.append(rain_values)

# Crear la figura y los ejes del boxplot
fig, ax = plt.subplots(figsize=(10, 6))

# Crear el boxplot con los datos de lluvia por cluster
ax.boxplot(rain_data)

# Configurar las etiquetas del eje x con los nombres de los clusters
cluster_labels = grouped.groups.keys()
ax.set_xticklabels(cluster_labels)

# Agregar etiquetas y título al gráfico
ax.set_xlabel('Cluster')
ax.set_ylabel('Lluvia')
ax.set_title('Boxplot de lluvia de 90 días antecedentes por cluster')

# Mostrar el gráfico
plt.show()

fig.savefig('/home/aospinau/Documents/Unal/AnlisisGeoespacial/FigurasProyecto/Boxplot_90dias.png', dpi=300, bbox_inches='tight')


#%% Boxplot por cluster
grouped = gdf_Alto.groupby('cluster')

# Crear una lista vacía para almacenar los datos de lluvia por cluster
rain_data = []

# Iterar sobre cada grupo y extraer los valores de lluvia
for _, group in grouped:
    rain_values = group['Acum_15dias'].values
    rain_data.append(rain_values)

# Crear la figura y los ejes del boxplot
fig, ax = plt.subplots(figsize=(10, 6))

# Crear el boxplot con los datos de lluvia por cluster
ax.boxplot(rain_data)

# Configurar las etiquetas del eje x con los nombres de los clusters
cluster_labels = grouped.groups.keys()
ax.set_xticklabels(cluster_labels)

# Agregar etiquetas y título al gráfico
ax.set_xlabel('Cluster')
ax.set_ylabel('Lluvia')
ax.set_title('Boxplot de lluvia por cluster')

# Mostrar el gráfico
plt.show()

grouped = gdf_Alto.groupby('cluster')

# Crear una lista vacía para almacenar los datos de lluvia por cluster
rain_data = []

# Iterar sobre cada grupo y extraer los valores de lluvia
for _, group in grouped:
    rain_values = group['Acum_15dias'].values
    rain_data.append(rain_values)

# Crear la figura y los ejes del boxplot
fig, ax = plt.subplots(figsize=(10, 6))

# Crear el boxplot con los datos de lluvia por cluster
ax.boxplot(rain_data)

# Configurar las etiquetas del eje x con los nombres de los clusters
cluster_labels = grouped.groups.keys()
ax.set_xticklabels(cluster_labels)

# Agregar etiquetas y título al gráfico
ax.set_xlabel('Cluster')
ax.set_ylabel('Lluvia')
ax.set_title('Boxplot de lluvia por cluster')

# Mostrar el gráfico
plt.show()

# %% Curva de densidad

# Supongamos que tienes un DataFrame llamado 'gdf_Alto' con las columnas 'Acum_diario' y 'cluster'

# Filtrar los datos para los primeros 5 clusters
df_filtered = gdf_Alto[gdf_Alto['cluster'].isin(gdf_Alto['cluster'].unique()[:5])]

# Crear gráficos de densidad separados para cada cluster
sns.set(style="whitegrid")  # Establecer estilo de la gráfica

# Definir una paleta de colores para los clusters
palette = sns.color_palette("Set1", len(df_filtered['cluster'].unique()))

# Crear un subplot por cada cluster
fig, axes = plt.subplots(len(df_filtered['cluster'].unique()), 1, figsize=(8, 6), sharex=True)

# Iterar sobre los clusters y crear el gráfico de densidad correspondiente
for i, cluster in enumerate(df_filtered['cluster'].unique()):
    subset = df_filtered[df_filtered['cluster'] == cluster]
    ax = axes[i]

    sns.kdeplot(data=subset, x='Acum_diario', fill=True, color=palette[i], ax=ax)
    ax.set_title(f'Cluster {cluster}')
    ax.set_ylabel('Densidad')

    # Establecer el límite del eje x en 0
    ax.set_xlim(0)

# Configurar el título y el eje x compartidos
fig.suptitle('Curvas de Densidad para los Primeros 5 Clusters', fontsize=12)
axes[-1].set_xlabel('Acumulado diario')

plt.tight_layout()
plt.show()


# %%

gdf_MM= gdf[gdf['Evento'] == 'movimientos en masa']
# %% boxplot + histograma anual

# Crear el DataFrame eventos_por_año
eventos_por_año = gdf_MM.groupby(['año', 'TipoEvento']).size().reset_index(name='count')

# Crear la figura y los ejes
fig, ax = plt.subplots(figsize=(10, 8))

# Graficar el histograma de eventos por año
eventos_por_año.pivot(index='año', columns='TipoEvento', values='count').plot(kind='bar', stacked=True, ax=ax)

# Configurar etiquetas y títulos
ax.set_xlabel('Año')
ax.set_ylabel('Número de Eventos')
ax.set_title('Histograma de Eventos por Año y Lluvia Media en Medellín')

# Ajustar las leyendas
ax.legend(title='Tipo de Evento', bbox_to_anchor=(1.35, 1.05))

# Crear los ejes para el boxplot
ax2 = ax.twinx().twiny()

# Agrupar los datos y graficar el boxplot
grouped = gdf_MM.groupby('año')
rain_data = []

for _, group in grouped:
    rain_values = group['Acum_7dias'].values
    rain_data.append(rain_values)

ax2.boxplot(rain_data)

# Configurar las etiquetas del eje x con los nombres de los clusters
cluster_labels = grouped.groups.keys()
ax2.set_xticklabels(cluster_labels)

# Configurar las etiquetas y el título del boxplot
ax2.set_xlabel('Año')
ax2.set_ylabel('Lluvia')
ax2.set_title('Boxplot de lluvia de 7 días antecedentes por cluster')

# Ajustar los márgenes para mostrar los boxplot correctamente
ax2.margins(x=0.5)

# Mostrar el gráfico completo
plt.show()


# %% calcular distancia a drenaje más cercano

# Cargar el GeoDataFrame de puntos (gdf) y el GeoDataFrame de líneas (quebradas)
gdf_puntos = gdf.to_crs(epsg='32619')
gdf_quebradas = quebradas.to_crs(epsg='32619')

# Calcular la distancia al punto más cercano de cada punto a las líneas
distancias = gdf_puntos.distance(gdf_quebradas.unary_union)

# Agregar la columna de distancia al GeoDataFrame de puntos
gdf_puntos['distancia_quebrada'] = distancias

gdf=gdf_puntos

#%% agregar estraro socioeconómico

gdf_estrato = gpd.read_file('/home/aospinau/Documents/Unal/AnlisisGeoespacial/estrato_socioeconomico.geojson')

# Crear el gráfico sin bordes
fig, ax = plt.subplots(figsize=(10, 10))
gdf_estrato.plot(column='ESTRATO', cmap='viridis', edgecolor='none', legend=True, ax=ax)

# Agregar el mapa base con contextily
cx.add_basemap(ax, crs=gdf_estrato.crs.to_string(), source=cx.providers.Stamen.TonerLite)

# Mostrar el gráfico
plt.show()

#%%

gdf= gdf.to_crs(epsg='4326')

# Conservar solo la columna 'ESTRATO'
gdf_unido = gdf_estrato[['ESTRATO', 'geometry']].to_crs(epsg='4326')


gdf= gpd.sjoin(gdf, gdf_unido, how='left')

gdf=gdf.drop_duplicates(subset='FICHA')



gdf = gdf.drop(columns=['index_right'])
# %%



# %% Regresión logistica

from pysal.model import spreg
from pysal.lib import weights
from pysal.explore import esda
from scipy import stats
import statsmodels.formula.api as sm
import numpy
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn


#%%
variable_names = ['hand', 'elevacion', 'pendiente',
                  'Acum_diario', 'Acum_3dias', 
                  'Acum_15dias', 'Acum_30dias', 'Acum_90dias', 
                  'distancia_quebrada']

for columna in variable_names:
    gdf[columna] = gdf[columna].astype(float)
for columna in variable_names:
    gdf[columna] = gdf[columna].dropna()

#%%

gdf_MM= gdf[gdf['Evento'] == 'movimientos en masa']

m1 = spreg.OLS(gdf_MM[['Acum_7dias']].values, gdf_MM[variable_names].values, name_y='Acum_7dias', name_x=variable_names)

# %%

print(m1.summary)

# %% knn

knn = weights.KNN.from_dataframe(gdf_MM, k=5)
# %%
lag_residual = weights.spatial_lag.lag_spatial(knn, m1.u)

ax = seaborn.regplot(x=m1.u.flatten(), y=lag_residual.flatten(), 
                     line_kws=dict(color='orangered'),
                     ci=None)
ax.set_xlabel('Model Residuals - $u$')
ax.set_ylabel('Spatial Lag of Model Residuals - $W u$')



# %%

correlation_matrix = gdf.corr(method='pearson')

print(correlation_matrix)
# %%
# Crear un mapa de calor de la matriz de correlación
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')

# Mostrar la gráfica
plt.show()


# %% análisis de cluster

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

gdf['EsMM'] = gdf.apply(lambda row: 1 if row['TipoEvento'] == 'movimientos en masa' else 0, axis=1)
gdf['EsEstructural'] = gdf.apply(lambda row: 1 if row['TipoEvento'] == 'estructural' else 0, axis=1)

df_MM2 = gdf[gdf['TipoEvento'] == 'movimientos en masa']
df_Est2 = gdf[gdf['TipoEvento'] == 'estructural']


gdf_alta=gdf[(gdf['Prioridad'] == 'alta') | (gdf['Prioridad'] == 'emergencia')]
df_MM = gdf_alta[gdf_alta['TipoEvento'] == 'movimientos en masa']
df_Est = gdf_alta[gdf_alta['TipoEvento'] == 'estructural']
df_Inun = gdf_alta[gdf_alta['TipoEvento'] == 'inundación']

gdf_MM= df_Est2#gdf[gdf['Evento'] == 'movimientos en masa']

variable_names = ['FICHA', 'hand', 'elevacion', 'pendiente', 
                  'distancia_quebrada', 'ESTRATO']

for columna in variable_names:
    gdf_MM[columna] = pd.to_numeric(gdf_MM[columna], errors='coerce')
    gdf_MM = gdf_MM.dropna(subset=[columna])

casa=gdf_MM[variable_names]
casa['elevacion'] = casa['elevacion'].astype(float)
#casa['FICHA'] = casa['FICHA'].astype(float)
casa['pendiente'] = casa['pendiente'].astype(float)

casa['FICHA'] = pd.to_numeric(casa['FICHA'], errors='coerce')

# Elimina las filas donde 'FICHA' es NaN
casa = casa.dropna(subset=['FICHA'])

# Opcionalmente, puedes convertir los valores en la columna 'FICHA' a float
casa['FICHA'] = casa['FICHA'].astype(float)


scaler = StandardScaler()
scaled_features = scaler.fit_transform(casa)



inertia = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=0).fit(scaled_features)
    inertia.append(kmeans.inertia_)

plt.plot(range(1, 11), inertia)
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.title('Elbow Method For Optimal Number of Clusters')
plt.show()


n_clusters = 5 # reemplaza esto con el número de clusters que hayas elegido
kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(scaled_features)


casa['Cluster_Kmeans'] = kmeans.labels_


grouped = casa.groupby('Cluster_Kmeans').mean()
print(grouped)



casa=casa[['Cluster_Kmeans', 'FICHA']]



gdf['FICHA'] = pd.to_numeric(gdf['FICHA'], errors='coerce')

# Elimina las filas donde 'FICHA' es NaN
gdf = gdf.dropna(subset=['FICHA'])

gdf['FICHA'] = gdf['FICHA'].astype(float)

casa_gdf = gdf.merge(casa, on='FICHA')


# Asegurándose de que 'dataframe' es un GeoDataFrame con la columna 'Cluster'.
# Si es un DataFrame normal, necesitas convertirlo a un GeoDataFrame.

# Si 'dataframe' es un DataFrame, conviértelo a un GeoDataFrame
# Suponiendo que las columnas de latitud y longitud se llamen 'lat' y 'lon'.
# Ahora grafica el GeoDataFrame
fig, ax = plt.subplots(figsize=(10, 10))

barrios= barrios.to_crs(epsg='32619')


# Colorea los puntos según su asignación de cluster
casa_gdf.plot(column='Cluster_Kmeans', categorical=True, legend=True, markersize=10, cmap='Set1', ax=ax)

cx.add_basemap(ax=ax,crs = casa_gdf.crs.to_string(), source=cx.providers.CartoDB.Positron)  #mapa base de contextily

barrios.plot(ax=ax, edgecolor='black', facecolor='none', alpha=0.3)


scale_bar = AnchoredSizeBar(ax.transData, 10000, '10 km', loc='lower right')
ax.add_artist(scale_bar)

# Agrega títulos y etiquetas
plt.title('Visualización Espacial de Clusters')
plt.xlabel('Longitud')
plt.ylabel('Latitud')

# Muestra el mapa
plt.show()


# %%

casa=casa_gdf.to_crs(epsg='32619')
#%%
import geopandas as gpd
import libpysal as lps
import esda

# Asegurarse de que el GeoDataFrame esté en un sistema de coordenadas proyectadas
# Cambia 'EPSG:xxxx' por el EPSG adecuado para tu área de estudio
# gdf = gdf.to_crs('EPSG:xxxx')

# Corregir geometrías inválidas
casa['geometry'] = gdf.buffer(0)

# Reindexar el GeoDataFrame
casa = casa.reset_index(drop=True)

# Crear una matriz de pesos espaciales
w = lps.weights.Queen.from_dataframe(casa)

# Calcular el índice de Moran
moran = esda.Moran(casa['Cluster'], w)

# Imprimir el índice de Moran y su p-valor
print(f"Índice de Moran: {moran.I}, p-valor: {moran.p_sim}")


#%% Geographycally Weighted Regresion (GWR)

gdf['EsMM'] = gdf.apply(lambda row: 1 if row['TipoEvento'] == 'movimientos en masa' else 0, axis=1)
gdf['EsEstructural'] = gdf.apply(lambda row: 1 if row['TipoEvento'] == 'estructural' else 0, axis=1)

df_MM2 = gdf[gdf['TipoEvento'] == 'movimientos en masa']
df_Est2 = gdf[gdf['TipoEvento'] == 'estructural']


gdf_alta=gdf[(gdf['Prioridad'] == 'alta') | (gdf['Prioridad'] == 'emergencia')]
df_MM = gdf_alta[gdf_alta['TipoEvento'] == 'movimientos en masa']
df_Est = gdf_alta[gdf_alta['TipoEvento'] == 'estructural']
df_Inun = gdf_alta[gdf_alta['TipoEvento'] == 'inundación']


# Tu DataFrame
df = df_Est

variable_names = ['elevacion', 'pendiente', 'distancia_quebrada', 'ESTRATO', 'Acum_15dias']

for columna in variable_names:
    df[columna] = pd.to_numeric(df[columna], errors='coerce')
    df = df.dropna(subset=[columna])

# Extraer las coordenadas de los puntos
coords = np.array([(geom.x, geom.y) for geom in df.geometry])

df['DEF_N'] = df['DEF'].apply(lambda x: 0 if x == 0 else 1)

# Definir la variable dependiente y las variables independientes
y = df['DEF_N'].values.reshape(-1, 1)
X = df[variable_names].values

# Estandarizar las variables independientes
scaler = StandardScaler()
X_standardized = scaler.fit_transform(X)

# Seleccionar el ancho de banda para GWR
selector = Sel_BW(coords, y, X_standardized, multi=False)
bw = selector.search()

# Ajustar el modelo GWR
gwr_model = GWR(coords, y, X_standardized, bw)
gwr_results = gwr_model.fit()

# Coeficientes locales de regresión
local_params = gwr_results.params

# Agregar resultados al GeoDataFrame
df['local_intercept'] = local_params[:, 0]
df['local_coef_variable1'] = local_params[:, 1]
df['local_coef_variable2'] = local_params[:, 2]

# Agregar todos los parámetros
for i in range(local_params.shape[1]):
    df[f'param_{i}'] = local_params[:, i]

# Crear una figura con varios subplots
fig, axs = plt.subplots(2, 3, figsize=(20, 10))

# Loop sobre los coeficientes y graficarlos
for i in range(local_params.shape[1]):
    ax = axs[i // 3, i % 3]
    df.plot(column=f'param_{i}', ax=ax, legend=True)
    ax.set_title(f'Coeficiente Local {i}')
    ax.axis('off')

# Mostrar la figura
plt.show()

# Mostrar un resumen de los resultados
gwr_results.summary()

#%%GWR lluvia

gdf['EsMM'] = gdf.apply(lambda row: 1 if row['TipoEvento'] == 'movimientos en masa' else 0, axis=1)
gdf['EsEstructural'] = gdf.apply(lambda row: 1 if row['TipoEvento'] == 'estructural' else 0, axis=1)

df_MM2 = gdf[gdf['TipoEvento'] == 'movimientos en masa']
df_Est2 = gdf[gdf['TipoEvento'] == 'estructural']


gdf_alta=gdf[(gdf['Prioridad'] == 'alta') | (gdf['Prioridad'] == 'emergencia')]
df_MM = gdf_alta[gdf_alta['TipoEvento'] == 'movimientos en masa']
df_Est = gdf_alta[gdf_alta['TipoEvento'] == 'estructural']
df_Inun = gdf_alta[gdf_alta['TipoEvento'] == 'inundación']


# Tu DataFrame
df = gdf_alta

variable_names = ['hand', 'elevacion', 'pendiente', 
                  'distancia_quebrada', 'ESTRATO']

for columna in variable_names:
    df[columna] = pd.to_numeric(df[columna], errors='coerce')
    df = df.dropna(subset=[columna])

# Extraer las coordenadas de los puntos
coords = np.array([(geom.x, geom.y) for geom in df.geometry])

df['DEF_N'] = df['DEF'].apply(lambda x: 0 if x == 0 else 1)

# Definir la variable dependiente y las variables independientes
y = df['DEF_N'].values.reshape(-1, 1)
X = df[variable_names].values

# Estandarizar las variables independientes
scaler = StandardScaler()
X_standardized = scaler.fit_transform(X)

# Seleccionar el ancho de banda para GWR
selector = Sel_BW(coords, y, X_standardized, multi=False)
bw = selector.search()

# Ajustar el modelo GWR
gwr_model = GWR(coords, y, X_standardized, bw)
gwr_results = gwr_model.fit()

# Coeficientes locales de regresión
local_params = gwr_results.params

# Agregar resultados al GeoDataFrame
df['local_intercept'] = local_params[:, 0]
df['local_coef_variable1'] = local_params[:, 1]
df['local_coef_variable2'] = local_params[:, 2]

# Agregar todos los parámetros
for i in range(local_params.shape[1]):
    df[f'param_{i}'] = local_params[:, i]

# Crear una figura con varios subplots
fig, axs = plt.subplots(2, 3, figsize=(20, 10))

# Loop sobre los coeficientes y graficarlos
for i in range(local_params.shape[1]):
    ax = axs[i // 3, i % 3]
    df.plot(column=f'param_{i}', ax=ax, legend=True)
    ax.set_title(f'Coeficiente Local {i}')
    ax.axis('off')

# Mostrar la figura
plt.show()

# Mostrar un resumen de los resultados
gwr_results.summary()

# %%

import matplotlib.pyplot as plt
import geopandas as gpd

# Extraer coeficientes locales y valores predichos
local_params = gwr_model.params
predictions = gwr_model.predy

# Agregar coeficientes y predicciones al GeoDataFrame original
# Asumiendo que 'gdf' es tu GeoDataFrame original
df['local_intercept'] = local_params[:, 0]
df['local_slope'] = local_params[:, 1]
df['predictions'] = predictions

# Crear un gráfico para visualizar los coeficientes locales y las predicciones
fig, axes = plt.subplots(1, 3, figsize=(20, 5))

# Visualizar el coeficiente de intersección local
df.plot(column='local_intercept', cmap='coolwarm', legend=True, ax=axes[0])
axes[0].set_title('Local Intercept')

# Visualizar el coeficiente de inclinación local
df.plot(column='local_slope', cmap='coolwarm', legend=True, ax=axes[1])
axes[1].set_title('Local Slope')



# %% Variograma


import skgstat as skg
from skgstat import Variogram, OrdinaryKriging
import pandas as pd

V = Variogram(df_MM[['X', 'Y']].values, df_MM.Acum_7dias.values, estimator="entropy", model="spherical", maxlag=1000, n_lags=20)
V.plot()

#%%ANN

import geopandas as gpd
import numpy as np
from scipy.spatial import KDTree

# Asumiendo que 'gdf' es tu GeoDataFrame con los puntos

# Convertir las geometrías a una matriz numpy de coordenadas (n, 2)
coords = np.array([(geom.x, geom.y) for geom in gdf.geometry])

# Usar KDTree para encontrar rápidamente los vecinos más cercanos
kdtree = KDTree(coords)

# Calcular las distancias al vecino más cercano para cada punto
# (k=2) para encontrar el primer vecino que no sea el punto en sí
distances, _ = kdtree.query(coords, k=2)
nearest_neighbor_distances = distances[:, 1]

# Calcular la media de las distancias observadas
observed_mean_distance = np.mean(nearest_neighbor_distances)

# Calcular la media de las distancias esperadas bajo CSR (Complete Spatial Randomness)
n = len(coords)
area = 1  # Asume un área de estudio de 1 (cambiar según sea necesario)
expected_mean_distance = 0.5 / np.sqrt(n / area)

# Calcular el ratio de Nearest Neighbor
nn_ratio = observed_mean_distance / expected_mean_distance

# Mostrar resultados
print(f"Distancia promedio al vecino más cercano: {observed_mean_distance}")
print(f"Valor esperado bajo CSR (Complete Spatial Randomness): {expected_mean_distance}")
print(f"Ratio de Nearest Neighbor: {nn_ratio}")

# Interpretar el resultado
if nn_ratio < 1:
    print("Los puntos están agrupados.")
elif nn_ratio > 1:
    print("Los puntos están dispersos.")
else:
    print("Los puntos tienen una distribución aleatoria.")

# %% mapas de densidad de kernel

barrios= barrios.to_crs(epsg='32619') #capa de poligonos que quieres agregar al mapa
df_MM2 = gdf[gdf['TipoEvento'] == 'movimientos en masa'] #capa de puntos (geodataframe)


fig, ax = plt.subplots(ncols=1, figsize=(12, 8))

levels = [0.1,0.3,0.5,0.7,0.9,1]

# Plot df_MM2 on the second axes object
kde = sns.kdeplot(
    ax=ax,
    x=df_MM2['geometry'].x,
    y= df_MM2['geometry'].y,
    levels = levels,
    shade=True,
    cmap='Reds',
    alpha=0.8,
    cbar=True
)

df_MM2.plot(ax=ax, color='black', markersize=1, alpha=0.03)
barrios.plot(ax=ax, edgecolor='black', facecolor='none')
cx.add_basemap(ax=ax,crs = df_MM.crs.to_string(), source=cx.providers.CartoDB.Positron)  #mapa base de contextily
#ax.set_axis_off()

from matplotlib_scalebar.scalebar import ScaleBar

# Crear una barra de escala y añadirla a la gráfica
scalebar = ScaleBar(1, location='lower right') # 1 pixel = 1 meter, in lower right corner
ax.add_artist(scalebar)

# Mostrar la gráfica



ax.set_title('Densidad de Kernel para eventos de movimientos en masa')

plt.show()


df_Est2 = gdf[gdf['TipoEvento'] == 'estructural']

fig, ax = plt.subplots(ncols=1, figsize=(12, 8))



# Plot df_MM2 on the second axes object
kde = sns.kdeplot(
    ax=ax,
    x=df_Est2['geometry'].x,
    y= df_Est2['geometry'].y,
    levels = levels,
    shade=True,
    cmap='Greens',
    alpha=0.8,
    cbar=True
)
ax.set_title('Densidad de Kernel para eventos estructurales')
# Add a basemap
df_Est2.plot(ax=ax, color='black', markersize=1, alpha=0.03)

barrios.plot(ax=ax, edgecolor='black', facecolor='none', alpha=0.5)
cx.add_basemap(ax=ax,crs = df_MM.crs.to_string(), source=cx.providers.CartoDB.Positron)
#ax.set_axis_off()

scalebar = ScaleBar(1, location='lower right') # 1 pixel = 1 meter, in lower right corner
ax.add_artist(scalebar)


# %%
