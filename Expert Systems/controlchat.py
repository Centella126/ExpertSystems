#!/usr/bin/env python3
import matplotlib.pyplot as plt
import time
import sys

# Leer el argumento de la línea de comandos
if len(sys.argv) > 1:
    try:
        referencia = float(sys.argv[1])  # Convertimos a float
    except ValueError:
        print("Error: El argumento de referencia debe ser un número.")
        sys.exit(1)
else:
    referencia = 10.0  # Valor por defecto si no se proporciona un argumento

# Variables iniciales
x1k = 0
x2k = 2
x3k = 3
n2k = -2
n3k = -3
x2Tk = 0
x3Tk = 0
uk = 0
y = 0

# Listas para almacenar valores para graficar
y_values = []
referencia_values = []
time_values = []

# Configurar la gráfica interactiva
plt.ion()  # Habilitar modo interactivo
fig, ax = plt.subplots()
line1, = ax.plot([], [], label="Salida", color="blue")
line2, = ax.plot([], [], label="Referencia", color="orange")
ax.set_xlim(0, 10)  # Limitar el eje x (puedes ajustar según el tiempo de simulación)
ax.set_ylim(-5, 20)  # Limitar el eje y (ajusta según tu referencia y salida)
ax.set_xlabel("Tiempo (s)")
ax.set_ylabel("Salida")
ax.set_title("Salida vs. Referencia en Tiempo Real")
ax.legend()
ax.grid(True)

# Tiempo de simulación (ajusta el rango según el tiempo total que deseas simular)
t_total = 100  # 100 iteraciones como ejemplo
dt = 0.1       # Tiempo de muestreo de 100 ms

# Simulación de lazo cerrado
for k in range(t_total):
    t = k * dt

    # Ecuaciones del observador de orden mínimo
    x2Tk = n2k - 4.4593 * x1k
    x3Tk = n3k + 1.2630 * x1k

    # Señal de control
    uk = 0.6678 * (referencia + 0.07223 * x1k + 0.3065 * x2Tk + 0.387 * x3Tk)

    # Ecuaciones del sistema
    x1k1 = 0.3 * x2k + 0.6 * x3k
    x2k1 = 0.2 * x1k - 0.7 * x2k - 0.35 * x3k + 1.8 * uk
    x3k1 = -0.4 * x1k + 0.2 * x2k + 0.1 * x3k + 0.9 * uk
    y = x1k

    # Ecuaciones del observador
    n2k1 = 0.6378 * n2k + 2.3256 * n3k + 0.2931 * y + 1.8 * uk
    n3k1 = -0.1789 * n2k - 0.6578 * n3k - 0.433 * y + 0.9 * uk

    # Actualizar variables de estado
    x1k = x1k1
    x2k = x2k1
    x3k = x3k1
    n2k = n2k1
    n3k = n3k1

    # Almacenar valores para graficar
    y_values.append(y)
    referencia_values.append(referencia)
    time_values.append(t)

    # Actualizar los datos de la gráfica en tiempo real
    line1.set_data(time_values, y_values)
    line2.set_data(time_values, referencia_values)
    ax.set_xlim(0, max(10, t))  # Ajustar el límite del eje x dinámicamente
    ax.figure.canvas.draw()
    ax.figure.canvas.flush_events()

    # Pausa simulando el delay de hardware
    time.sleep(dt)

# Desactivar el modo interactivo y mostrar la gráfica final
plt.ioff()
plt.show()
