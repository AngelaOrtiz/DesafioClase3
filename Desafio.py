import code
import random
from numpy import NaN, append, identity, unicode_
import pandas as pd
import json
import matplotlib.pyplot as plt
from pyparsing import str_type

#Lee Excel, desde la fila que corresponde
bip = pd.read_excel("carga-bip.xlsx", header=9)

#Filtrar datos
#Obtener solo los datos de las columnas: CODIGO, NOMBRE FANTASIA
cod_nom = bip.loc[ : ,["CODIGO","NOMBRE FANTASIA","LONGITUD", "LATITUD","HORARIO REFERENCIAL"]]

#Podemos crear columnas dinámicamente
#asignando los valores de otra columna
cod_nom["COMUNA"] = bip.loc[ : ,["MAIPU"]]

#Define Data Frame
df=pd.DataFrame(data=cod_nom)

#Crea lista de comunas a partir de Excel
listaComuna=df['COMUNA'].to_list()
comunas=[]
for n in listaComuna:
    if n not in comunas:
        if n is not NaN:
            comunas.append(n)
print(comunas)

#Conteo de puntos de carga por comuna
conteo=[]
for r in comunas:
    a=len(cod_nom[cod_nom["COMUNA"]==r])
    conteo.append(a)
#print(conteo)

#Se da formato de archivo json
jsonData={}
for i in range (0,len(comunas)):
    jsonData[comunas[i]]=conteo[i]
#print(jsonData)
objeto=json.dumps(jsonData)
print(objeto)

#Guardar como json
#objeto.to_json("Conteo.json")
with open("jsonData.json","w",encoding="utf-8") as j:
    j.write(json.dumps(jsonData,indent=2))

#Asigna aleatoriamente horarios a los puntos de carga
horario = ["09:00 - 13:00, 14:00 -19:00","08:00 - 13:30, 14:30 -21:00","08:30 - 13:30, 15:00 -20:00","09:30 - 13:00, 15:00 -22:00","10:00 - 13:00, 14:00 -24:00"]
for i in range (0,len(cod_nom)):
    cod_nom["HORARIO REFERENCIAL"] = cod_nom["HORARIO REFERENCIAL"].apply(lambda x: horario[random.randint(0,len(horario)-1)])
puntoHorario=[]
for r in horario:
    a=len(cod_nom[cod_nom["HORARIO REFERENCIAL"]==r])
    puntoHorario.append(a)
#print(puntoHorario)


#Crear un gráfico que indica la cantidad de puntos de carga para cada horario.
plt.close()
plt.scatter(x=horario, y=puntoHorario, s=puntoHorario)
plt.show()
bar_colors = ['tab:red','tab:blue','tab:orange','tab:green','tab:purple']
plt.bar(horario,puntoHorario,label=horario, color=bar_colors)
plt.show()


#Crea un archivo por comuna con sus respectivos puntos de carga
for i in range (0,len(comunas)):
    CreaCSV=cod_nom[cod_nom["COMUNA"]==comunas[i]]
    CreaCSV.to_csv("codigo-bip_"+comunas[i]+".csv", encoding="utf-8")