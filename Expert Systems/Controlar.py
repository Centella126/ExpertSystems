import matplotlib.pyplot as plt
import time
import sys

# Variables iniciales
x1k = 0
x2k = 2
x3k = 3
n2k = -2
n3k = -3
x2Tk = 0
x3Tk = 0
referencia = float(sys.argv[1])
uk = 0
y = 0

# Listas para almacenar valores para graficar
y_values = []
referencia_values = []
time_values = []

# Configurar la gr�fica en modo interactivo
plt.ion()
fig, ax = plt.subplots()
line1, = ax.plot([], [], label="Salida", color="blue")
line2, = ax.plot([], [], label="Referencia", color="orange")
plt.xlabel("Tiempo (s)")
plt.ylabel("Salida")
plt.title("Salida vs. Referencia en Tiempo Real")
plt.legend()
plt.grid(True)

# Simulaci�n de lazo cerrado (bucle infinito)
k = 0
while True:
    # Ecuaciones del observador de orden m�nimo
    x2Tk = n2k - 4.4593 * x1k
    x3Tk = n3k + 1.2630 * x1k

    # Se�al de control
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
    time_values.append(k * 0.1)

    # Actualizar datos de la gr�fica
    line1.set_data(time_values, y_values)
    line2.set_data(time_values, referencia_values)

    # Ajustar los l�mites de los ejes de la gr�fica din�micamente
    ax.set_xlim(0, max(10, k * 0.1))  # El l�mite X crece conforme pasa el tiempo
    ax.set_ylim(min(min(y_values), min(referencia_values)) - 2, 
                max(max(y_values), max(referencia_values)) + 2)  # Ajusta el l�mite Y con un margen

    # Dibujar y actualizar la gr�fica en tiempo real
    fig.canvas.draw()
    fig.canvas.flush_events()

    # Guardar la gr�fica en cada iteraci�n
    plt.savefig("output.png")

    # Incrementar el contador y esperar un poco
    k += 1
    time.sleep(0.1)  # Espera simulando el delay de Arduino
