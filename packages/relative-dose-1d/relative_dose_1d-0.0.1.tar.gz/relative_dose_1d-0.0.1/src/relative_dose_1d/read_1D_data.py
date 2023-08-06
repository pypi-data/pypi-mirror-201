# -*- coding: utf-8 -*-
"""
Created Apr-2023

@author: Luis Alfonso Olivares Jimenez
Con agradecimiento al M. en C. Jose Alfredo Herrera González por compartirme ideas para el desarrollo
de este script.

Script que contiene funciones para extraer datos 1D de un archivo de texto y 
transformalos a un objeto array del paquete numpy.

El archivo de texto deberá de cumplir lo siguiente:
    1.- Contener un solo perfil de datos
    2.- Los datos deberán encontrarse en M filas y dos columnas, (M, 2).
        La primer columa deberá de contener la posción espacial en milímetros y la segunda los datos.

El script se ha probado con los siguientes archivos:

    * Archivo en formato w2CAD (formato usado por el sistema Eclipse 16.1, de la empresa Varian). 
      En el algoritmo, el inicio de los datos se identifica con las palabras: '$STOM' o '$STOD'

    * Archivo en formato mcc (formato usado por el software Verisoft 7.1.0.199, de la empresa PTW).
      En el algoritmo, el inicio de los datos se identifica con la palabra: 'BEGIN_DATA'

    * Archivo en formato txt 
      Los datos deben de encontrarce distribuidos en M filas por 2 columnas y separados
      por un espacio en blanco.
"""

import numpy as np  #Para almacenar los datos en un objeto "array" del paquete numpy
import matplotlib.pyplot as plt #Para visualizar los datos


#%%

"Definición de funciones"

def txt_to_list(filename):
    'Convertir el archivo de texto a un objeto "list" de python'
    with open(filename, encoding='UTF-8', mode = 'r') as file:
        lista_completa = [line.strip() for line in file]
        
    return lista_completa

def get_from_txt(lista):
    curva_n = []
    for line in lista:
        curva_n.append(line.split())
    valores = np.array(curva_n).astype(float)
    return valores

def separar_curvas_w2CAD(lista):
    'Separar las curvas como elementos de una lista'
    curvas = []
    curva_n = []
    for line in lista:
        
        if line == '$STOM' or line == '$STOD':
            curva_n = []
         
        elif line == '$ENOM' or line == '$ENOD':
            curva_n.append(line)
            curvas.append(curva_n)
            
        curva_n.append(line)
        
    return curvas

def obtener_datos_w2CAD(lista):
    'Obtener los datos a graficar (datos entre los caracter < >)'
    # Extraer datos de las lineas que comienzan con el caracter '<'
    data_list = [idx[1:-1].split() for idx in lista if idx[0] == "<"]
    # Converting list to float array
    array_data = np.array(data_list).astype(float)
    return array_data

def separar_curvas_mcc(lines):
    'Separar las curvas como elementos de una lista'
    n = 1
    curvas = []
    curva_n = []
    for line in lines:
        
        if 'BEGIN_SCAN  ' + str(n) in line:
            curva_n = []
         
        elif 'END_SCAN  ' + str(n) in line:
            #curva_n.append(line)
            curvas.append(curva_n)
            n = n + 1
            
        curva_n.append(line)
        
    return curvas

def obtener_datos_mcc(lista):
    'Obtener los datos a graficar de un archivo mcc'
    obtener = False
    curva_n = []
    for line in lista:
        
        if line == 'END_DATA':
            obtener = False
            
        if obtener:
            curva_n.append(line.split())
            
        if line == 'BEGIN_DATA':
            obtener = True


    array_data = np.array(curva_n).astype(float)
    print(array_data.shape)
    array_data[:,1] = 100*array_data[:,1]/np.amax(array_data[:,1])
    return array_data[:,0:2]

#%%
#Run the program
if __name__ == '__main__':

    "Inicio y ejecución del script"

    #filename = "6MViX_Open Field - 00_Measured Depth Doses.txt" 
    filename = "MeasuredProfile_10x10_z50_6MV.data"

    lista_principal = txt_to_list(filename)
    curvas = separar_curvas_w2CAD(lista_principal)
    numero_curvas = len(curvas)

    "Graficar los datos"
    fig, ax = plt.subplots()
    for i in range(numero_curvas):
        data = obtener_datos_w2CAD(curvas[i])
        if numero_curvas > 1:
            x = data[:,2]
            y = data[:,3]
        else:
            x = data[:,0]
            y = data[:,1]
        plt.plot(x, y)
    plt.show()