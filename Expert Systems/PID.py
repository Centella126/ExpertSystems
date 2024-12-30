import time
import RPi.GPIO as GPIO
import adafruit_dht

# Definición de pines
PIN_CRUCE_CERO = 12  # Pin para el cruce por cero
PIN_DISPARO = 13     # Pin para el disparo del triac
DHT_PIN = 4          # Pin para el sensor DHT11

# Configuración del sensor DHT11
dht_sensor = adafruit_dht.DHT11(DHT_PIN)

# Variables PID
Setpoint = 35  # Temperatura deseada (°C)
Kp = 6.36      # Ganancia proporcional
Ti = 200       # Tiempo integral (ms)
Td = 50        # Tiempo derivativo (ms)
Ki = Kp / Ti   # Ganancia integral
Kd = Kp * Td   # Ganancia derivativa

# Variables del PID
PID_error = 0      # Error actual
previous_error = 0 # Error previo
integral = 0       # Término integral
derivative = 0     # Término derivativo
output = 0         # Salida del PID (potencia del dimmer)

# Variables para el control del dimmer
detectado = False       # Indica si ocurrió un cruce por cero
valor = 0               # Tiempo de retardo para el disparo del triac
Potencia = 0            # Potencia ajustada (0-20%)

# Variables de tiempo
Tiempo_previo = 0
Tiempo_actual = 0
Read_Delay = 1  # Tiempo de muestreo (segundos)

# Configuración de los pines GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_DISPARO, GPIO.OUT)
GPIO.setup(PIN_CRUCE_CERO, GPIO.IN)

# Función para manejar el cruce por cero
def cruce_cero_callback(channel):
    global detectado
    detectado = True

# Configurar la interrupción para el cruce por cero
GPIO.add_event_detect(PIN_CRUCE_CERO, GPIO.RISING, callback=cruce_cero_callback, bouncetime=300)

# Bucle principal
try:
    while True:
        Tiempo_actual = time.time()

        # Si se detectó el cruce por cero, disparamos el triac
        if detectado:
            # Convertir la potencia a un tiempo de retardo para el dimmer
            valor = int((Potencia / 20.0) * (7600 - 10) + 10)  # 20% máximo de potencia
            print(f"Valor: {valor}, Potencia: {Potencia}")  # Depuración antes del disparo
            time.sleep(valor / 1_000_000.0)  # Retardo en microsegundos
            GPIO.output(PIN_DISPARO, GPIO.HIGH)
            time.sleep(100 / 1_000_000.0)  # Retardo de 100 µs
            GPIO.output(PIN_DISPARO, GPIO.LOW)
            detectado = False  # Restablecer el estado de detección

        # Leer temperatura y calcular el PID a intervalos definidos
        if Tiempo_actual - Tiempo_previo >= Read_Delay:
            Tiempo_previo = Tiempo_actual

            # Leer temperatura del DHT11
            try:
                temperatura = dht_sensor.temperature
                if temperatura is None:
                    print("Error al leer el sensor DHT11")
                    continue

                # Calcular el PID
                PID_error = Setpoint - temperatura
                integral += PID_error * Read_Delay  # Integral acumulada
                derivative = (PID_error - previous_error) / Read_Delay  # Derivada
                output = Kp * PID_error + Ki * integral + Kd * derivative

                # Limitar la salida del PID al 20% máximo
                Potencia = max(0, min(20, output))  # Asegurar que la potencia no supere el 20%

                # Enviar datos a la consola
                print(f"Temperatura: {temperatura}°C, Potencia: {Potencia}%")

                # Guardar error previo
                previous_error = PID_error

            except RuntimeError as e:
                print(f"Error al leer el sensor: {e}")
                continue

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Programa terminado")

finally:
    GPIO.cleanup()  # Liberar recursos GPIO al finalizar
