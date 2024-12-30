
import time
import adafruit_dht
import board
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Configuración del sensor DHT11
DHT_SENSOR = adafruit_dht.DHT11(board.D4)  # Usa el pin GPIO4, cámbialo si usas otro

# Inicializar listas para almacenar los datos de temperatura y humedad
temperaturas = []
humedades = []
tiempos = []

# Configuración de la gráfica en matplotlib
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
fig.suptitle("Lecturas de Temperatura y Humedad en Tiempo Real")

# Función para actualizar la gráfica en tiempo real
def actualizar(frame):
    try:
        # Lee la temperatura y la humedad
        temperatura = DHT_SENSOR.temperature
        humedad = DHT_SENSOR.humidity
        tiempo_actual = time.time()

        # Verifica que las lecturas sean válidas
        if temperatura is not None and humedad is not None:
            # Almacena los datos en las listas
            temperaturas.append(temperatura)
            humedades.append(humedad)
            tiempos.append(tiempo_actual)

            # Limita la cantidad de datos en la gráfica a los últimos 20 puntos
            temperaturas_grafica = temperaturas[-20:]
            humedades_grafica = humedades[-20:]
            tiempos_grafica = [t - tiempos[0] for t in tiempos[-20:]]

            # Actualiza la gráfica de temperatura
            ax1.clear()
            ax1.plot(tiempos_grafica, temperaturas_grafica, color='red')
            ax1.set_ylabel("Temperatura (°C)")
            ax1.set_ylim(0, 50)

            # Actualiza la gráfica de humedad
            ax2.clear()
            ax2.plot(tiempos_grafica, humedades_grafica, color='blue')
            ax2.set_ylabel("Humedad (%)")
            ax2.set_ylim(0, 100)

        else:
            print("Esperando valores válidos...")

    except RuntimeError as e:
        print(f"Error de lectura: {e}")

# Crear la animación de la gráfica en tiempo real
ani = animation.FuncAnimation(fig, actualizar, interval=2000)

# Mostrar la gráfica
plt.show()
