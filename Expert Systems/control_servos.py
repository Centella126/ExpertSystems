import RPi.GPIO as GPIO  # type: ignore
import sys
import time

# Configurar el modo de los pines GPIO
GPIO.setmode(GPIO.BCM)

def conf_Servo(gpio_pin):
    """Configura el pin GPIO para el servo y crea la señal PWM."""
    GPIO.setup(gpio_pin, GPIO.OUT)
    pwm = GPIO.PWM(gpio_pin, 50)  # Frecuencia de 50Hz
    pwm.start(0)  # Inicia el PWM con ciclo de trabajo en 0
    return pwm

def conf_servo_angulo(pwm, angle):
    """Configura el ángulo del servo (0 a 180 grados)."""
    cycle = 2 + (angle / 18)  # Calcula el ciclo de trabajo
    pwm.ChangeDutyCycle(cycle)  # Cambia el ciclo de trabajo para el ángulo
    time.sleep(0.5)  # Espera para que el servo se mueva
    pwm.ChangeDutyCycle(0)  # Detiene el PWM para no dañar el servo

def cerrar_servos():
    """Cierra los servos a la posición predeterminada."""
    pwm_18 = conf_Servo(18)
    pwm_17 = conf_Servo(17)

    try:
        conf_servo_angulo(pwm_18, 90)
        conf_servo_angulo(pwm_17, 90)
    finally:
        pwm_18.stop()
        pwm_17.stop()
        GPIO.cleanup()

def abrir_servos():
    """Abre los servos a la posición predeterminada."""
    pwm_18 = conf_Servo(18)
    pwm_17 = conf_Servo(17)

    try:
        conf_servo_angulo(pwm_18, 180)
        conf_servo_angulo(pwm_17, 0)
    finally:
        pwm_18.stop()
        pwm_17.stop()
        GPIO.cleanup()

# Determinar qué acción realizar
if len(sys.argv) > 1:
    accion = sys.argv[1]
    if accion == 'cerrar':
        cerrar_servos()
    elif accion == 'abrir':
        abrir_servos()
    else:
        print("Acción inválida. Usa 'cerrar' o 'abrir'.")
else:
    print("No se especificó ninguna acción.")
