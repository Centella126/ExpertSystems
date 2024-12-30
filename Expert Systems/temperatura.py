import time
import adafruit_dht
import board
import pymysql
from datetime import datetime, timedelta

# Configuración de los sensores DHT11
DHT_SENSOR_1 = adafruit_dht.DHT11(board.D4)  # Pin GPIO4 (temperatura real)
DHT_SENSOR_2 = adafruit_dht.DHT11(board.D23)  # Pin GPIO23 (temperatura exterior)

# Función para obtener la temperatura de un sensor
def obtener_temperatura(sensor):
    try:
        temperatura = sensor.temperature
        if temperatura is None:
            print("Esperando valores válidos...")
            return None
        return temperatura
    except RuntimeError as e:
        print(f"Error de lectura: {e}")
        return None

# Conectar a la base de datos MySQL usando PyMySQL
def conectar_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="qwerty123",
        database="Registros_Reales",
        cursorclass=pymysql.cursors.DictCursor  # Esto devuelve los resultados como diccionarios
    )

# Función para obtener el último registro en la base de datos
def obtener_ultimo_registro():
    conn = conectar_db()
    cursor = conn.cursor()

    # Buscar el último registro en la base de datos
    sql = "SELECT hora, dia FROM registros ORDER BY id DESC LIMIT 1"
    cursor.execute(sql)
    ultimo_registro = cursor.fetchone()

    cursor.close()
    conn.close()

    return ultimo_registro

# Función para insertar los datos en la base de datos
def insertar_datos(temperatura_real, temperatura_exterior, hora, dia):
    conn = conectar_db()
    cursor = conn.cursor()

    # Establecer la temperatura deseada en función del día
    if dia <= 18:
        temperatura_deseada = 37.5
    elif 19 <= dia <= 21:
        temperatura_deseada = 37.2
    else:
        temperatura_deseada = 37.5  # Si el día es mayor a 21, ponemos 37.5°C como valor por defecto.

    # Fecha actual
    fecha_hora = datetime.now()
    fecha = fecha_hora.date()

    sql = """
        INSERT INTO registros (fecha, hora, temperatura_real, temperatura_exterior, temperatura_deseada, estado_incubadora, dia)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    valores = (fecha, hora, temperatura_real, temperatura_exterior, temperatura_deseada, "ON", dia)

    try:
        cursor.execute(sql, valores)
        conn.commit()
        print(f"Datos insertados: {temperatura_real}°C (Real), {temperatura_exterior}°C (Exterior), Temperatura deseada: {temperatura_deseada}°C a las {hora}")
    except pymysql.MySQLError as err:
        print(f"Error al insertar datos: {err}")
    finally:
        cursor.close()
        conn.close()

# Bucle para leer los datos y enviarlos a la base de datos
def iniciar_registro():
    # Consultar la base de datos para obtener el último registro
    ultimo_registro = obtener_ultimo_registro()

    if ultimo_registro:
        # Si hay registros, continuar desde el último día y hora
        if isinstance(ultimo_registro['hora'], timedelta):  # Si 'hora' es un timedelta
            horas_completas = ultimo_registro['hora'].seconds // 3600  # Extraemos las horas de timedelta
        elif isinstance(ultimo_registro['hora'], datetime):  # Si 'hora' es un datetime
            horas_completas = ultimo_registro['hora'].hour  # Extraemos las horas de datetime
        else:
            horas_completas = 0  # Si no es ninguno de los dos, usamos 0 horas

        dia_actual = ultimo_registro['dia']
        print(f"Continuando desde la hora {horas_completas}:00:00 del día {dia_actual}")
    else:
        # Si no hay registros, iniciar desde 00:00:00, día 1
        horas_completas = 0
        dia_actual = 1
        print("No hay registros previos. Iniciando desde 00:00:00 del día 1.")

    try:
        while True:
            # Obtener las temperaturas de ambos sensores
            temp_real = obtener_temperatura(DHT_SENSOR_1)
            temp_exterior = obtener_temperatura(DHT_SENSOR_2)

            # Verificar si las temperaturas son válidas
            if temp_real is not None and temp_exterior is not None:
                print(f"Temperaturas leídas: {temp_real}°C (Real), {temp_exterior}°C (Exterior)")

                # Calcular la hora completa (cada hora aumenta de a 1)
                hora_str = f"{horas_completas:02}:00:00"  # La hora asociada es cada hora completa (HH:00:00)
                
                # Insertar los datos en la base de datos
                insertar_datos(temp_real, temp_exterior, hora_str, dia_actual)

                # Incrementar la hora en 1
                horas_completas += 1

                # Verificar si se alcanzaron las 24 horas para cambiar el día
                if horas_completas >= 24:  # 24 horas
                    dia_actual += 1  # Cambiar de día
                    horas_completas = 0  # Reiniciar la hora a 00:00:00

                # Agregar más depuración para confirmar el avance del tiempo
                print(f"Hora actual: {hora_str} - Día: {dia_actual}")
            else:
                print("Esperando una lectura válida de temperatura...")

            # Esperar 5 segundos antes de tomar la siguiente lectura
            time.sleep(5)  # 5 segundos entre cada lectura

    except KeyboardInterrupt:
        print("Programa terminado por el usuario")

    finally:
        DHT_SENSOR_1.exit()  # Libera el recurso del sensor
        DHT_SENSOR_2.exit()  # Libera el recurso del sensor

# Iniciar el proceso
if __name__ == "__main__":
    iniciar_registro()
