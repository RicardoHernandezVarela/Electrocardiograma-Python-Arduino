import serial
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from drawnow import *

def main():

    # Iniciar la comunicación serial entre la computadora y arduino.
    arduino = serial.Serial('com4', 9600) 
    cantidad = 'a'

    while isinstance(cantidad, float) == False:
        try:
            min = float(input('Tiempo a grabar >> '))

            ###########################################################################
            # Cantidad de muestras que se tomarán, el script no para hasta 
            # que se tengan todas las muestras.
            # Para pruebas utilizar un número pequeño, ejemplo 0.1 = 1500 muestras
            # 250 es la frecuencia de muestreo, 250 muestras por segundo, configurar
            # en el script de arduino.
            ############################################################################

            cantidad = min*60*250 
        except:
            min = input('Introduce de nuevo el tiempo a grabar >> ')

    print('Iniciando')

    plt.ion() # modo interactivo para plotear en tiempo real.

    # Función para plotear en tiempo real.
    def grafRT(): 
        plt.ylim(100,650) #Limites del eje y
        plt.plot(data) #graficar ecg, datos del arreglo data.
        plt.xlabel('tiempo (milisegundos)')
        plt.ylabel('voltaje (mV)')
        plt.title('Electrocardiograma')
        plt.ticklabel_format(useOffset=False) #no autoescalar el eje Y.

    # Arreglo para guardar los datos obtenidos del sensor.
    data = []
    
    #primer = arduino.readline()

    while len(data) < cantidad:
        try:
            info = arduino.readline()
            data.append(float(info))

            drawnow(grafRT)                       
            plt.pause(.00000001)

        except ValueError:
            print("Problema al capturar los datos", end='\n')
            guardar = input('Quieres guardar los datos: s = si, n = no: ')

            if guardar.lower() == 's':
                ecg_data = pd.DataFrame(data=data) #Guardar datos en un dataframe de pandas.
                nombre = input("Nombre del archivo: ")
                archivo = nombre + ".csv"
                ecg_data.to_csv(archivo) # Generar un archivo csv con los datos del ECG.
            else:
                pass

            
    print('Datos capturados', end='\n')

    # Analizar datos adquiridos con el sensor.
    ecg_data = pd.DataFrame(data=data)
    nombre = input("Nombre del archivo: ")
    archivo = nombre + ".csv"
    ecg_data.to_csv(archivo)


    data = pd.read_csv(archivo,delimiter=",")

    ecg_data = data.iloc[:, 1].values #extraer muestras del dataframe, solo columna con valores.

    # Detección de picos R en la señal de ECG.
    peaks, _ = find_peaks(ecg_data, distance=150)
    distancias = np.diff(peaks)

    #print(peaks.size, end='\n')
    #print(distancias.size)

    media = np.mean(distancias)
    #print(type(media))

    # Calcular y mostrar los latidos por minuto (BPM).
    bpm = (ecg_data.size/media)/(ecg_data.size/15000)

    print('Registrados {} latidos por minuto.'.format(round(bpm)))

    # Mostrar la gráfica de los picos R detectados.
    fig1 = plt.figure(1)
    plt.plot(ecg_data, 'b')
    plt.plot(peaks, ecg_data[peaks], 'rx')

    # Mostrar la gráfica de la distribución de la distancia entre picos R, equivalente a un latido.
    fig2 = plt.figure(2)
    plt.hist(distancias)
    plt.xlabel('distancia (muestras)')
    plt.ylabel('frecuencia')
    plt.title('Distribución de distancia entre máximos locales(picos)')
    plt.show()

    # Guardar las gráfica generadas como imagenes.
    guardar = input('Guardar imagenes = s, no guardar = n: ')

    if guardar.lower() ==  's':
        fig1.savefig(nombre + "ecg.png")
        fig2.savefig(nombre + "dist.png")
    else:
        pass

#Llamar la función principal main()
if __name__ == '__main__':
  main()