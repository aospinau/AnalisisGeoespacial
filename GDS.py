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

fichas['Evento'] = fichas['Evento'].replace(to_replace=r'^mov.*', value='movimientos en masa', regex=True)
fichas['Evento'] = fichas['Evento'].replace(to_replace=r'^est.*', value='estructural', regex=True)
fichas['Evento'] = fichas['Evento'].replace(to_replace=r'^inc.*', value='incendio', regex=True)
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

fichas1.to_excel(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas1.xlsx', index = None, header=True)
fichas2.to_excel(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas2.xlsx', index = None, header=True)
fichas3.to_excel(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas3.xlsx', index = None, header=True)
fichas4.to_excel(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas4.xlsx', index = None, header=True)
fichas5.to_excel(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas5.xlsx', index = None, header=True)
fichas6.to_excel(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas6.xlsx', index = None, header=True)
fichas7.to_excel(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas7.xlsx', index = None, header=True)
fichas8.to_excel(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas8.xlsx', index = None, header=True)
fichas9.to_excel(r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas9.xlsx', index = None, header=True)

# %%

import pandas as pd

read_file = pd.read_csv (r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas2.csv')
read_file.to_excel (r'C:\Users\Dell\Documents\Unal\AnlisisGeoespacial\DatosFichas\fichas2.xlsx', index = None, header=True)

# %%
