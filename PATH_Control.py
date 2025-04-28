# Brief: Este codigo contiene los comandos para ejecutar los puertos
#        GPIO del raspberry.     
# Version: 1.0
# Date: 20/4/2024
# Author: Fernando Ian Yedra - Jose Eduardo Crecenscio
#         Universidad Iberoamerica - Coordinacion de Ingenieria Mecatronica

from tkinter import messagebox
#import pigpio

SHLD1_GPIO = 4
SHLD2_GPIO = 17
SHLD3_GPIO = 27
SHLD4_GPIO = 22

ELBW1_GPIO = 18
ELBW2_GPIO = 23
ELBW3_GPIO = 24
ELBW4_GPIO = 25

servo_gpios = {
    'shoulder_1': SHLD1_GPIO,
    'shoulder_2': SHLD2_GPIO,
    'shoulder_3': SHLD3_GPIO,
    'shoulder_4': SHLD4_GPIO,
    'elbow_1': ELBW1_GPIO,
    'elbow_2': ELBW2_GPIO,
    'elbow_3': ELBW3_GPIO,
    'elbow_4': ELBW4_GPIO,
}

def execute_trajectory(waypoints):
    if not waypoints:
        messagebox.showerror('Alerta', 'La trayectoria no se ha definido')
        return

    print('Ejecutando trayectoria')
    messagebox.showinfo('Trayectoria mandada a ejecutar', 'Espere a que se termine la trayectoria actual.')
    print('Waypoints', waypoints)

def servo_set_angle(angle, gpio):
    #pi = pigpio.pi()
    #if not pi.connected:
    #    print('Pigpio daemon no se ha inizializado, correr sudo systemctl start pigpiod')
    #    exit()
    #else:
    #    print('Daemon Pigpio inizializado, GPIOs conectados')
    
    try:
        # Verificar que el ángulo se encuentre entre 0 y 180 grados
        angle = float(angle)
        if not 0 <= angle <= 180:
            messagebox.showerror('Ángulo inválido', f'El ángulo para el pin {gpio} debe estar entre 0 y 180 grados.')
            return False
        
        # Aquí se incluye la lógica para mover el servo al ángulo deseado.
        print(f'Simulando colocar el servo del pin {gpio} en {angle} grados')
        #pulse_width = int((angle / 180) * 1000+ 1000)
        #pi.set_servo_pulsewidth(gpio, pulse_width)
        return True
    except ValueError:
        messagebox.showerror('Valor inválido', f'El ángulo para el pin {gpio} debe ser un número.')
        return False

def execute_servos(sEntry1, sEntry2, sEntry3, sEntry4, eEntry1, eEntry2, eEntry3, eEntry4):
    # Se recuperan los valores en los inputs y se guardan en el diccionario
    servo_angles = {}
    servo_angles["shoulder_1"] = sEntry1.get()
    servo_angles["shoulder_2"] = sEntry2.get()
    servo_angles["shoulder_3"] = sEntry3.get()
    servo_angles["shoulder_4"] = sEntry4.get()
    servo_angles["elbow_1"] = eEntry1.get()
    servo_angles["elbow_2"] = eEntry2.get()
    servo_angles["elbow_3"] = eEntry3.get()
    servo_angles["elbow_4"] = eEntry4.get()
    
    all_angles_set = True

    #Se recupera el gpio de cada servo y se manda actualizar su ángulo.
    for servo_name, angle_input in servo_angles.items():
        gpio_pin = servo_gpios[servo_name]
        if not servo_set_angle(angle_input, gpio_pin):
            all_angles_set = False
    
    if all_angles_set:
        messagebox.showinfo('Ángulos actualizados', 'Se han mandado a actualizar la posición de los ángulos. Revisar la consola para más información.')


def home():
    servo_angles = {}
    servo_angles["shoulder_1"] = 20
    servo_angles["shoulder_2"] = 130
    servo_angles["shoulder_3"] = 170
    servo_angles["shoulder_4"] = 20
    servo_angles["elbow_1"] = 90
    servo_angles["elbow_2"] = 90
    servo_angles["elbow_3"] = 90
    servo_angles["elbow_4"] = 90

    #Se recupera el gpio de cada servo y se manda actualizar su ángulo.
    for servo_name, angle_input in servo_angles.items():
        gpio_pin = servo_gpios[servo_name]
        if not servo_set_angle(angle_input, gpio_pin):
            print('Error colocando los servos en home...')

    messagebox.showinfo('Ángulos actualizados', 'Se han colocado los servos en home')

print('Error: correr vista para el main')