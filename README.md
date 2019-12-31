# Electrocardiograma-Python-Arduino
Registro de señales de electrocardiograma con Python y Arduino, cálculo de latidos por minuto (BPM).

La carpeta ECG contiene el código en Arduino para transmitir los datos de un sensor conectado al puerto A0, 
para registrar la señal de electrocardiograma se utilizó el OPAMP de instrumentación AD8232.

El script ecg.py inicia la comunicación serial con el arduino y la recepción de datos del sensor, utiliza las librerías 
scipy.signal, matplotlib, pandas para manejar los datos, calcular los latidos por minuto, mostrar los datos en "tiempo real" 
y generar gráficas con los datos adquiridos y los resultados obtenidos.

La comunicación serial de ecg.py tiene como parámetros el puerto al que está conectado el Arduino por default el COM4 y el baudrate 
para la comunicación, por default 9600.
