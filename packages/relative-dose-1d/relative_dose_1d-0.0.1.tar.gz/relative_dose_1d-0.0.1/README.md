# relative_dose_1d
Tool for 1-dimensional relative dosimetry analysis in radiotherapy

![image_gui](/docs/assets/GUI.PNG)

## Introducción
El paquete *relative_dose_1d* permite calcular la resta e índice gamma entre dos perfiles de dosis.

El paquete se ha probado con los siguientes archivos:

    * Archivo en formato w2CAD (formato usado por el sistema Eclipse 16.1, de la empresa Varian). 
      En el algoritmo, el inicio de los datos se identifica con las palabras: '$STOM' o '$STOD'

    * Archivo en formato mcc (formato usado por el software Verisoft 7.1.0.199, de la empresa PTW).
      En el algoritmo, el inicio de los datos se identifica con la palabra: 'BEGIN_DATA'

    * Archivo en formato txt 
      Los datos deben de encontrarce distribuidos en M filas por 2 columnas y separados
      por un espacio en blanco.

Para un correcto funcionamiento, el archivo de texto deberá de cumplir con los siguientes características:

    1.- Contener un solo perfil de datos
    2.- Los datos deberán encontrarse en M filas y dos columnas, (M, 2).
        La primer columa deberá de contener la posción espacial en milímetros y la segunda los datos.

## Instalación
**En Linux**<br/>
El método más sencillo de instalación es escribiendo en una terminal:
```bash
pip install relative_dose_1d
```
**En Windows**<br/>
Previo a la instalación, es necesario contar con un administrador de paquetes. Para quienes no estén familiarizados con los paquetes Python, se recomienda utilizar la plataforma [ANACONDA](https://www.anaconda.com/products/individual).
Una vez que se ha instalado ANACONDA, abrir el inicio de Windows y buscar *Anaconda Prompt*. Dentro de la terminal (ventana con fondo negro), seguir la indicación descrita para Linux (párrafo anterior).

Una vez realizada la instalación, abrimos una terminal (o Anaconda Prompt en el caso de Windows) y escribimos el comando **python**:

```bash
python
```
Posteriormente, escribimos:

```python
import relative_dose_1d.GUI
```