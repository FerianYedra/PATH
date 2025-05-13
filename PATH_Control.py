# Brief: Este codigo contiene los comandos para ejecutar los puertos
#        GPIO del raspberry.     
# Version: 1.0
# Date: 20/4/2024
# Author: Fernando Ian Yedra - Jose Eduardo Crecenscio
#         Universidad Iberoamerica - Coordinacion de Ingenieria Mecatronica

from tkinter import messagebox
import pigpio
import time
import math

SHLD1_GPIO = 4
SHLD2_GPIO = 17
SHLD3_GPIO = 27
SHLD4_GPIO = 22

ELBW1_GPIO = 18
ELBW2_GPIO = 23
ELBW3_GPIO = 24
ELBW4_GPIO = 25

pi = pigpio.pi()
if not pi.connected:
     print('Pigpio daemon no se ha inicializad, correr "sudo systemctl start pigpiod"')
     exit()
else:
     print('Daemon Pigpio inicializado, GPIO conectados')

servo_gpios = {
    'elbow_1': ELBW1_GPIO,
    'elbow_2': ELBW2_GPIO,
    'elbow_3': ELBW3_GPIO,
    'elbow_4': ELBW4_GPIO,
    'shoulder_1': SHLD1_GPIO,
    'shoulder_2': SHLD2_GPIO,
    'shoulder_3': SHLD3_GPIO,
    'shoulder_4': SHLD4_GPIO,
}

# Obtener los valores de los servos para hacer el rate limiting o ramping
current_servo_pulse_widths = {gpio: 1500 for gpio in servo_gpios.values()}

SERVO_MIN_PULSE = 1000
SERVO_MAX_PULSE = 2000
SERVO_PULSE_RANGE = SERVO_MAX_PULSE - SERVO_MIN_PULSE
DEFAULT_DURATION = 1.5
STEP_DELAY = 0.1

def update_values(step_entry, mov_entry):
    STEP_DELAY = float(step_entry.get())
    print(f'Step Delay actualizado a: {STEP_DELAY}')
    DEFAULT_DURATION = float(mov_entry.get())
    print(f'Duracion de movimiento actualizada a {DEFAULT_DURATION}')

    messagebox.showinfo('Aviso', 'Valores actualizados')

def angle_to_pulse(angle):
    angle = float(angle)
    angle = max(0, min(180, angle))
    pulse_width = SERVO_MIN_PULSE + angle/(180) * SERVO_PULSE_RANGE

    return int(pulse_width)

def pulse_to_angle(pulse):
    pulse = float(pulse)
    pulse = max(SERVO_MIN_PULSE, min(SERVO_MAX_PULSE, pulse))
    angle = ((pulse - SERVO_MIN_PULSE) / SERVO_PULSE_RANGE)
    return angle 

# Definimos función para el movimiento lento
def move_servo_smooth(gpio, target_angle, duration_sec=DEFAULT_DURATION):
    global current_servo_pulse_widths

    try:
        target_angle = float(target_angle)
        if not 0 <= target_angle <= 180:
            print(f'Ángulo inválido {target_angle}, para pin {gpio} (fuera de rango [0, 180])')
            return False

        target_pulse = angle_to_pulse(target_angle)
        start_pulse = current_servo_pulse_widths.get(gpio, 1500)
        pulse_change = target_pulse - start_pulse

        if abs(pulse_change) < 1 or duration_sec <= 0:
            if start_pulse != target_pulse:
                pi.set_servo_pulsewidth(gpio, target_pulse)
                current_servo_pulse_widths[gpio] = target_pulse
                time.sleep(STEP_DELAY)
            return True

        num_steps = max(1, int(math.ceil(duration_sec / STEP_DELAY)))
        pulse_increment = float(pulse_change) / num_steps

        current_pulse = float(start_pulse)
        for step in range(num_steps):
            current_pulse += pulse_increment
            set_pulse = int(round(current_pulse))
            set_pulse = max(SERVO_MIN_PULSE, min(SERVO_MAX_PULSE, set_pulse))

            pi.set_servo_pulsewidth(gpio, set_pulse)
            current_servo_pulse_widths[gpio] = set_pulse
            time.sleep(STEP_DELAY)
        
        if current_servo_pulse_widths[gpio] != target_pulse:
            pi.set_servo_pulsewidth(gpio, target_pulse)
            current_servo_pulse_widths[gpio] = target_pulse
            time.sleep(STEP_DELAY)
        return True
    
    except ValueError:
        print(f'Error: Valor inválido para ángulo del pin {gpio}')
        return False
    except Exception as e:
        print(f'Error moviendo servo en {gpio}: {e}')
        return False


def servo_set_angle(angle, gpio):
    try:
        # Verificar que el ángulo se encuentre entre 0 y 180 grados
        angle = float(angle)
        if not 0 <= angle <= 180:
            messagebox.showerror('Ángulo inválido', f'El ángulo para el pin {gpio} debe estar entre 0 y 180 grados.')
            return False
        
        # Aquí se incluye la lógica para mover el servo al ángulo deseado.
        print(f'Simulando colocar el servo del pin {gpio} en {angle} grados')
        pulse_width = int((angle / 180) * 1000+ 1000)
        pi.set_servo_pulsewidth(gpio, pulse_width)
        return True
    except ValueError:
        messagebox.showerror('Valor inválido', f'El ángulo para el pin {gpio} debe ser un número.')
        return False

def execute_servos(sEntry1, sEntry2, sEntry3, sEntry4, eEntry1, eEntry2, eEntry3, eEntry4, duration_per_servo=1):
    # Se recuperan los valores en los inputs y se guardan en el diccionario
    servo_angles = {}
    servo_angles["shoulder_1"] = float(sEntry1.get())
    servo_angles["shoulder_2"] = float(sEntry2.get())
    servo_angles["shoulder_3"] = float(sEntry3.get())
    servo_angles["shoulder_4"] = float(sEntry4.get())
    servo_angles["elbow_1"] = float(eEntry1.get())
    servo_angles["elbow_2"] = float(eEntry2.get())
    servo_angles["elbow_3"] = float(eEntry3.get())
    servo_angles["elbow_4"] = float(eEntry4.get())
    
    all_angles_set = True
    start_time = time.time()

    #Se recupera el gpio de cada servo y se manda actualizar su ángulo.
    for servo_name, angle_input in servo_angles.items():
        gpio_pin = servo_gpios[servo_name]
        print(f'Moviendo {servo_name} (GPIO: {gpio_pin}) a {angle_input:.1f}º...')
        if not move_servo_smooth(gpio_pin, angle_input, duration_sec=duration_per_servo):
            all_angles_set = False
    
    if all_angles_set:
        messagebox.showinfo('Ángulos actualizados', 'Se han mandado a actualizar la posición de los ángulos. Revisar la consola para más información.')
    else:
        messagebox.showerror('Error moviendo servos', 'No todos los servos se movieron a la posición deseada.')


def home():
    servo_angles = {}
    servo_angles["shoulder_1"] = 90
    servo_angles["shoulder_2"] = 90
    servo_angles["shoulder_3"] = 90
    servo_angles["shoulder_4"] = 90
    servo_angles["elbow_1"] = 170
    servo_angles["elbow_2"] = 20
    servo_angles["elbow_3"] = 20
    servo_angles["elbow_4"] = 170

    #Se recupera el gpio de cada servo y se manda actualizar su ángulo.
    for servo_name, angle_input in servo_angles.items():
        gpio_pin = servo_gpios[servo_name]
        time.sleep(0.5)
        if not servo_set_angle(angle_input, gpio_pin):
            print('Error colocando los servos en home...')

    messagebox.showinfo('Ángulos actualizados', 'Se han colocado los servos en home')

print('Leyendo funciones de control...')

def move_servo(servo_angles, duration=1):
    for servo_name, angle_input in servo_angles.items():
        gpio_pin = servo_gpios[servo_name]
        if not move_servo_smooth(gpio_pin, angle_input, duration_sec=duration):
            print('Error moviendo servos')

def forward1():
    print('Forward 1')
    servo_angles = {}

    # Move to home
    servo_angles["elbow_1"] = 170
    servo_angles["elbow_2"] = 20
    servo_angles["elbow_3"] = 20
    servo_angles["elbow_4"] = 170
    servo_angles["shoulder_1"] = 90
    servo_angles["shoulder_2"] = 90
    servo_angles["shoulder_3"] = 90
    servo_angles["shoulder_4"] = 90

    move_servo(servo_angles)

    # Sequence 1
    servo_angles = {}  
    servo_angles['shoulder_2'] = 0
    servo_angles['shoulder_3'] = 180
    move_servo(servo_angles)

    # Sequence 2
    servo_angles = {}
    servo_angles["elbow_1"] = 110
    servo_angles['elbow_4'] = 110
    move_servo(servo_angles)

    # Sequence 3
    servo_angles = {}
    servo_angles['shoulder_3'] = 90
    servo_angles['elbow_4'] = 170
    servo_angles['elbow_1'] = 170
    move_servo(servo_angles)

    # Sequence 4
    servo_angles = {}
    servo_angles["elbow_4"] = 110
    servo_angles['elbow_1'] = 110
    servo_angles["shoulder_2"] = 90
    move_servo(servo_angles)

    # Sequence 5
    servo_angles = {}
    servo_angles['elbow_1'] = 170
    servo_angles['elbow_4'] = 170
    move_servo(servo_angles)
    
def rotate1():
    print('Rotate 1')
    servo_angles = {}

    # Move to home
    servo_angles["elbow_1"] = 170
    servo_angles["elbow_2"] = 20
    servo_angles["elbow_3"] = 20
    servo_angles["elbow_4"] = 170
    servo_angles["shoulder_1"] = 90
    servo_angles["shoulder_2"] = 90
    servo_angles["shoulder_3"] = 90
    servo_angles["shoulder_4"] = 90
    move_servo(servo_angles)

    # Sequence 1
    servo_angles = {}
    servo_angles["elbow_1"] = 110
    servo_angles["elbow_4"] = 110
    servo_angles["shoulder_3"] = 180
    move_servo(servo_angles)

    # Sequence 2
    servo_angles = {}
    servo_angles["elbow_4"] = 170
    servo_angles["elbow_1"] = 170
    move_servo(servo_angles)

    # Sequence 4
    servo_angles = {}
    servo_angles["elbow_4"] = 110
    servo_angles["elbow_1"] = 110
    servo_angles["shoulder_2"] = 160
    move_servo(servo_angles)

    # Sequence 5
    servo_angles = {}
    servo_angles["elbow_1"] = 170
    servo_angles["elbow_4"] = 170
    move_servo(servo_angles)


    # Sequence 6
    servo_angles = {}
    servo_angles["elbow_3"] = 80
    servo_angles["elbow_2"] = 80
    servo_angles["shoulder_1"] = 180
    move_servo(servo_angles)

    # Sequence 7
    servo_angles = {}
    servo_angles["elbow_2"] = 20
    servo_angles["elbow_3"] = 20
    move_servo(servo_angles)

    # Sequence 8
    servo_angles = {}
    servo_angles["elbow_2"] = 80
    servo_angles["elbow_3"] = 80
    servo_angles["shoulder_4"] = 180
    move_servo(servo_angles)

    # Sequence 9
    servo_angles = {}
    servo_angles["elbow_3"] = 20
    servo_angles["elbow_2"] = 20
    move_servo(servo_angles)

    # Sequence 10
    servo_angles = {}
    servo_angles["shoulder_3"] = 90
    servo_angles["shoulder_4"] = 90
    servo_angles["shoulder_2"] = 90
    servo_angles["shoulder_1"] = 90
    move_servo(servo_angles)


def execute_trajectory(waypoints):
    if not waypoints:
        messagebox.showerror('Alerta', 'La trayectoria no se ha definido')
        return
    x0 = 0
    y0 = 0
    print('Waypoints:', waypoints) 
    for i, data in enumerate(waypoints):
        if i == 0:
            continue

        x1 = int(data[0]) * math.cos(data[1] * math.pi / 180)
        y1 = int(data[0]) * math.sin(data[1] * math.pi / 180)

        X = x1 - x0
        Y = y1 - y0

        dist = int(math.sqrt(X**2 + Y**2))
        rot = math.degrees(math.atan2(Y/X))

        print(f'Moviendo a waypoint {i} de {len(waypoints)-1}: ({data[0]},{data[1]})')
        print(f'Item {i}:  distance: {dist}, rotation: {rot}')

        # Se efectua el giro
        for k in range(int(rot/10)):
            if rot != 0:
                print(f'Ejecutando rotate1: {k}')
                rotate1()
            else:
                print('Trayectoria con rotación vacía')

        # Se efectua el desplazamiento lineal
        for j in range(dist):
            if dist != 0:
                print(f'Ejecutando forward1: {j}')
                forward1()
            else:
                print('Trayectoria con distancia vacía.')
        
        # Update initial Point
        x0 = x1
        y0 = y1

    print('Ejecutando trayectoria')
    messagebox.showinfo('Trayectoria mandada a ejecutar', 'Espere a que se termine la trayectoria actual.')
