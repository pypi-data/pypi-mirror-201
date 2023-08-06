# -*- coding: utf-8 -*-
"""
Created Apr-2023

@author: Luis Alfonso Olivares Jimenez
Con agradecimiento al M. en C. Jose Alfredo Herrera González por compartirme ideas para el desarrollo
de este script.

Script para generar una GUI que permita cargar datos 1-D de archivos de texto 
con perfiles de dosis. Automáticamente se calcula la resta y el índice gamma.

Leer el archivo README.md para una mayor descripción.
"""

import sys
import os
import numpy as np
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, 
                             QPushButton, QMessageBox, QFileDialog, QVBoxLayout)
from PyQt6.QtCore import Qt

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvas

#from read_1D_data import txt_to_list, separar_curvas_w2CAD, obtener_datos_w2CAD, obtener_datos_mcc, get_from_txt
from relative_dose_1d.read_1D_data import txt_to_list, separar_curvas_w2CAD, obtener_datos_w2CAD, obtener_datos_mcc, get_from_txt

class Main_Window(QWidget):

    def __init__(self):
        """Constructor for Empty Window Class"""
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Set up the apllication"""
        "x, y, width, height"
        self.setGeometry(200,100,800,400)
        self.setWindowTitle("Relative dose 1D")

        self.setUp()
        self.show()

    def setUp(self):
        "Definir layout"
        self.v_box_layout = QVBoxLayout() # Create layout

        self.open_file_button = QPushButton("Cargar un archivo...", self)
        self.open_file_button.clicked.connect(self.open_file_button_clicked)

        self.borrar_button = QPushButton("Borrar", self)
        self.borrar_button.clicked.connect(self.borrar_grafica)
        
        self.Q_grafica = Q_Bloque_grafica() 
         
        self.v_box_layout.addWidget(self.open_file_button)
        self.v_box_layout.addWidget(self.borrar_button)
        self.v_box_layout.addWidget(self.Q_grafica.Qt_fig)

        self.setLayout(self.v_box_layout)

    # Funciones para los botones

    def open_file_button_clicked(self):
        file_name, _ = QFileDialog.getOpenFileName()
        _ , extension = os.path.splitext(file_name)

        if file_name:    #   ¿Se obtuvo algún archivo?
            lista_principal = txt_to_list(file_name)

            formato = identificar_formato(lista_principal)

            if formato == 'varian':
                all_data = separar_curvas_w2CAD(lista_principal)

                if all_data[0][0] == '$STOM' or all_data[0][0] == '$STOD':
                    valores = obtener_datos_w2CAD(all_data[0])
                    self.Q_grafica.set_data_and_plot(valores)

            if formato == 'ptw':
                #all_data = separar_curvas_w2CAD_mcc(lista_principal)
                valores = obtener_datos_mcc(lista_principal)
                self.Q_grafica.set_data_and_plot(valores)

            if formato == 'txt':
                print('Dentro de txt format')
                valores = get_from_txt(lista_principal) 
                self.Q_grafica.set_data_and_plot(valores)

        if len(self.Q_grafica.last_data) == 2:
            self.open_file_button.setEnabled(False)
            self.calc_difference_and_gamma()

    def borrar_grafica(self):
        self.Q_grafica.ax_perfil.clear()
        self.Q_grafica.ax_perfil_resta.clear()
        self.Q_grafica.ax_gamma.clear()
        self.Q_grafica.fig.canvas.draw()
        self.open_file_button.setEnabled(True)
        self.Q_grafica.last_data = []

    #   Definición de funciones adicionales

    def calc_difference_and_gamma(self):

        data_A = self.Q_grafica.last_data[0]
        data_B = self.Q_grafica.last_data[1]

        # Se calcula el perfil B en las posiciones de A, con base en interpolación.
        data_B_from_A_positions = np.interp(data_A[:,0], data_B[:,0], data_B[:,1], left = np.nan)
    
        difference = data_A[:,1] - data_B_from_A_positions

        added_positions = np.array((data_A[:,0], difference))
        values = np.transpose(added_positions)

        # min_position y max_position permitirán acotar la región a analizar.
        min_position = np.max( (np.min(data_A[:,0]), np.min([data_B[:,0]])) )
        max_position = np.min( (np.max(data_A[:,0]), np.max([data_B[:,0]])) )        
        g, g_percent = gamma_1D(data_A, data_B, min_position = min_position, max_position = max_position)

        self.Q_grafica.plot_resta(values)
        self.Q_grafica.plot_gamma(g)

#   Funciones adicionales

def identificar_formato(list):

    if list[0][0] == '$':
        return 'varian'

    if list[0] == 'BEGIN_SCAN_DATA':
        return 'ptw'
    try:
        num_float = float(list[0][0])
        return 'txt'
    
    except ValueError:
        print("Archivo en formato no valido")
        # Crea una instancia de QMessageBox
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)  # Establece el ícono de advertencia
        msg.setWindowTitle("Advertencia")
        msg.setText("Archivo en formato no valido.")
        # Muestra la ventana emergente y espera a que se cierre
        msg.exec()

def gamma_1D(ref, eval, min_position, max_position, dose_t = 3, dist_t = 2, dose_tresh = 0, interpol = 1):

    '''
    Calculo del índice gamma 1-dimensional para dos perfiles de dosis.
    Los perfiles deberán de encontrarse normalizados del 0 al 100.

     dose_t : float, default = 3
            Tolerancia para la diferencia en dosis [%]

        dist_t : float, default = 3
            Tolerancia para la distancia, en milímetros (criterio DTA).
        dose_tresh : float, default = 10
            Umbral de dosis, en porcentaje (0 a 100). 
            Todo punto en la distribución con un valor menor al umbral es excluido del análisis.
    '''
    num_of_points = ref.shape[0]
    interp_positions = np.linspace(ref[0,0], ref[-1,0], (interpol + 1)*(num_of_points - 1) + 1, endpoint=True)
    eval_from_interp_positions = np.interp(interp_positions, eval[:,0], eval[:,1], left = np.nan, right = np.nan) 
    added_positions = np.array((interp_positions, eval_from_interp_positions))
    eval_from_interp_positions = np.transpose(added_positions)

    #   Para almacenar temporalmente los valores de la función Gamma por cada punto en la distribución de referencia
    gamma = np.zeros( (num_of_points, 2) )
    gamma[:,0] = ref[:,0]

    for i in range(num_of_points):

        if (ref[i,0] < min_position) or (ref[i,0] > max_position):  
            #Si la dimension del perfil de referencia es mayor a la dimensión del perfil a evaluar, se ignoran las 
            # posiciones que se encuentran fuera de la región definida por "min_position" and "max_position".
            gamma[i, 1] = np.nan
            continue

        Gamma_acumulado = np.array([])  # Para acumular el cálculo Gamma de todos los puntos del perfil a evaluar.
        for j in range(eval_from_interp_positions.shape[0]):

            dose_difference = ref[i,1] - eval_from_interp_positions[j,1]
            distance = ref[i,0] - eval_from_interp_positions[j,0]

            Gamma = np.sqrt(
                        (distance**2) / (dist_t**2)
                        + (dose_difference**2) / (dose_t**2))
                        
            Gamma_acumulado = np.append(Gamma_acumulado, Gamma)

        gamma[i,1] = np.min( Gamma_acumulado[ ~np.isnan(Gamma_acumulado) ] )
        if ref[i,1] < dose_tresh:
            gamma[i,1] = np.nan

    # Arroja las coordenadas en donde los valores gamma son menor o igual a 1
    less_than_1_coordinate = np.where(gamma[:,1] <= 1)
    # Cuenta el número de coordenadas en donde se cumple que gamma <= 1
    less_than_1 = np.shape(less_than_1_coordinate)[1]
    # Número de valores gamma diferentes de np.nan
    total_points = np.shape(gamma)[0] - np.shape(np.where(np.isnan(gamma[:,1])))[1]

    #   Índice de aprobación
    gamma_percent = float(less_than_1)/total_points*100

    return gamma, gamma_percent
    

    
class Q_Bloque_grafica:
        
    def __init__(self):
        self.fig = Figure(figsize=(4,3), tight_layout = True, facecolor = 'whitesmoke')
        self.Qt_fig = FigureCanvas(self.fig)

        #   Axes para la imagen
        self.ax_perfil = self.fig.add_subplot(1, 2, 1)
        self.ax_perfil.set_title('Perfiles')
        self.ax_perfil.set_ylabel('Porcentaje [%]')
        self.ax_perfil.set_xlabel('Distancia [mm]')
        self.ax_perfil.grid(alpha = 0.3)

        self.ax_perfil_resta =  self.fig.add_subplot(1, 2, 2)
        #self.ax_perfil_resta.set_title('Resta')
        self.ax_perfil_resta.set_ylabel('Porcentaje [%]')
        self.ax_perfil_resta.set_xlabel('Distancia [mm]')
        self.ax_perfil_resta.grid(alpha = 0.3)

        self.ax_gamma = self.ax_perfil_resta.twinx()
        self.ax_gamma.set_ylabel('gamma')
        #self.ax_gamma.set_ylim((0, 2))

        self.last_data = []
        
    def set_data_and_plot(self, data):
        x = data[:,0]
        y = data[:,1]
        #self.ax_perfil.clear()
        self.ax_perfil.plot(x, y)
        self.ax_perfil.set_ylabel('Porcentaje [%]')
        self.ax_perfil.set_xlabel('Distancia [mm]')
        self.ax_perfil.grid(alpha = 0.3)

        self.fig.canvas.draw()

        self.save_last_data(data)
        
        
    def save_last_data(self, data):
        self.last_data.append(data)
        
    def plot_resta(self, data):
        x = data[:,0]
        y = data[:,1]
        #self.ax_perfil.clear()
        self.ax_perfil_resta.plot(x, y, color='r', label = 'Diferencia', alpha = 0.6)
        self.ax_perfil_resta.set_ylabel('Diferencia')
        self.ax_perfil_resta.set_xlabel('Distancia [mm]')
        self.ax_perfil_resta.grid(alpha = 0.3)
        self.ax_perfil_resta.legend(loc = 'upper left')

        self.fig.canvas.draw()

    def plot_gamma(self, data):
        x = data[:,0]
        y = data[:,1]

        self.ax_gamma.plot(x, y, color='g', label = 'gamma', marker = '.')
        self.ax_gamma.set_ylabel('gamma')
        self.ax_gamma.legend(loc = 'upper right')


        self.fig.canvas.draw()        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main_Window()
    sys.exit(app.exec())

app = QApplication(sys.argv)
window = Main_Window()
sys.exit(app.exec())