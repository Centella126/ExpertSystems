import RPi.GPIO as GPIO # type: ignore
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

def mover_servos_fijos():
    """Mueve los servos a los ángulos predefinidos."""
    # Configurar los servos en los pines GPIO 18 y 17
    pwm_18 = conf_Servo(18)
    pwm_17 = conf_Servo(17)

    try:
        # Mover el servo en el pin GPIO 18 a 180 grados
        conf_servo_angulo(pwm_18, 180)

        # Mover el servo en el pin GPIO 17 a 90 grados
        conf_servo_angulo(pwm_17, 90)
    finally:
        # Detener los PWM y limpiar los pines GPIO
        pwm_18.stop()
        pwm_17.stop()
        GPIO.cleanup()

# Llamar a la función para mover los servos
mover_servos_fijos()
