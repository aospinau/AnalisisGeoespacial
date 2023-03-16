#%%
import pandas as pd
import numpy as np
# %%
#Importar datos en formato csv y crear df
fichas=pd.read_csv(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\InspeccionesDAGRD.csv', encoding='ISO-8859-1')

#%%
#Cambiar nombre de columna
fichas.rename(columns={ fichas.columns[1]: "fecha" }, inplace = True)
#definir columna de fecha como tipo datetime
fichas['fecha']= pd.to_datetime(fichas['fecha'])

#%%

#Crear columna de dirrección completa
fichas["Address"] = fichas["Dirección"] + " " + fichas["Numero"]
#%%

#Borrar todas las fichas sin caracterizacion de evento Todos los eventos en minuscula

fichas=fichas[fichas['Dirección'].notna()]
fichas=fichas[fichas['Numero'].notna()]
fichas=fichas[fichas['fecha'].notna()]
fichas=fichas[fichas['Evento'].notna()]
fichas['Evento']=fichas['Evento'].apply(str.lower)
fichas['Prioridad']=fichas['Prioridad'].apply(str.lower)

#llenar espacios vacios de numero de evacuaciones con ceros
fichas['DEF'] = (pd.to_numeric(fichas['DEF'], errors='coerce').fillna(0))
fichas['TEM'] = (pd.to_numeric(fichas['TEM'], errors='coerce').fillna(0))


#%%
###Explorar Datos###

#Número de inspecciones por meses
fichas['Evento'].groupby(fichas["fecha"].dt.month).count().plot(kind="bar", legend=False, ylabel='Numero de inspecciones por riesgo', xlabel='Mes')

#Número de inspecciones por años
fichas['Evento'].groupby(fichas["fecha"].dt.year).count().plot(kind="bar", legend=False, ylabel='Numero de inspecciones por riesgo', xlabel='Año')



#%%
#agrupar en unica clase inspecciones por movimientos en masa, estructural e incendio.
fichas[fichas['Evento'].str.match('mov')]='movimientos en masa'
fichas[fichas['Evento'].str.match('est')]='estructural'
fichas[fichas['Evento'].str.match('inc')]='incendio'


# %%

#Para Mapgis
#Fraccionar datos de inspecciones por riesgo para 

fichasMG= fichas[['FICHA', 'Address']].copy()

fichas1=fichasMG.iloc[0:10000]
fichas2=fichasMG.iloc[10000:20000]
fichas3=fichasMG.iloc[20000:30000]
fichas4=fichasMG.iloc[30000:40000]
fichas5=fichasMG.iloc[40000:50000]
fichas6=fichasMG.iloc[50000:60000]
fichas7=fichasMG.iloc[60000:70000]
fichas8=fichasMG.iloc[70000:80000]
fichas9=fichasMG.iloc[80000:90000]

fichas1.to_csv(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas1.csv', index=False)
fichas2.to_csv(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas2.csv', index=False)
fichas3.to_csv(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas3.csv', index=False)
fichas4.to_csv(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas4.csv', index=False)
fichas5.to_csv(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas5.csv', index=False)
fichas6.to_csv(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas6.csv', index=False)
fichas7.to_csv(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas7.csv', index=False)
fichas8.to_csv(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas8.csv', index=False)
fichas9.to_csv(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas9.csv', index=False)

# %%
