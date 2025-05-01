# Brief: Este codigo contiene la vista para el HMI del robot cuadrupedo
#        de PATH, esta vista funge como main del codigo y manda a llamar
#        otros archivos de python con las funciones de control y movimiento
#        asi como las salidas GPIO del rasp.
# Version: 1.0
# Date: 20/4/2024
# Author: Fernando Ian Yedra - Jose Eduardo Crecenscio - Diego Zamora Garcia 
#         Universidad Iberoamerica - Coordinacion de Ingenieria Mecatronica

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import PATH_Control as control
import math
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Ddefinicion de variables globales
waypoints = [(0, 0)]

# Brief: Funcion que manda actualizar los waypoints para la interfaz grafica
#        usa el arreglo de waypoints para generar la imagen de la trayectoria.
def update_plot():
    ax.clear()

    if waypoints:
        distances = [wp[0] for wp in waypoints]
        angles_rad = [math.radians(wp[1]) for wp in waypoints]

        ax.plot(angles_rad, distances, marker='o', linestyle='-', color='blue', label='Trtajectory')
        ax.plot(angles_rad, distances, marker='x', linestyle='None', color='red')
    
    current_dis = distance_var.get()
    current_angle_deg = rotation_var.get()
    current_angle_rad = math.radians(current_angle_deg)

    ax.plot([0, current_angle_rad], [0, current_dis], color='green', linestyle='--', label='Preview')
    ax.plot(current_angle_rad, current_dis, marker='+', color='lime', markersize='10')

    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_rmax(105)
    ax.set_rticks(range(0, 101, 20))
    ax.set_rlabel_position(-22.5)
    ax.set_title('Waypoint Trajectory', va='bottom')
    ax.tick_params(axis='both', which='major', labelsize=8)
    ax.grid(True)

    canvas.draw()

# Brief: Esta función se encarga de mandar a actualizar el marcador de preview para el gráfico.
def update_preview_label(event=None):
    dist_label_val.config(text=f'{distance_var.get():.1f}')
    rot_label_val.config(text=f'{rotation_var.get():.1f}º')

    update_plot()

# Brief: Esta función obtiene los valores almacenados de ttk y los añade a la lista de waypoints
#        como una tupla.
def add_waypoint():
    dist = distance_var.get()
    angle = rotation_var.get()
    waypoints.append((dist, angle))
    print(f'Waypoint añadido: ({dist:.1f}, {angle:.1f}º)')
    print('Lista de waypoints: ', waypoints)

    update_plot()

# Brief: Función que elemina la última tupla de la lista de waypoints, primero se verifica que la
#        lista no se encuentre vacía.
def remove_waypoint():
    if waypoints:
        removed = waypoints.pop()
        print(f'Waypoint eliminado: ({removed})')
        print(f'Lista de waypoints: ', waypoints)
        update_plot()
    else:
        print('Lista de waypoints vacia')
        messagebox.showwarning('Aviso', 'Lista de waypoints vacia, añadir waypoint.')

# Brief: Funcion para hacer toggle de pantalla completa,
#        se verifica si se encuentra en pantalla completa
#        y se cambia el atributo del root.
def toggle_fullscreen():
    is_fullscreen = root.attributes('-fullscreen')
    root.attributes('-fullscreen', not is_fullscreen)
    root.focus_force()

def on_closing():
    print('Cerrando programa...')
    try:
        plt.close('all')
    except Exception as e:
        print('Error cerrando plot.')
    
    root.destroy()
    print('Ventana de TK inter destruida.')

# Brief: Funciones para incrementar o disminuir el angulo con los botones '+' y '-'
#        del segundo Tab, la funcion de incrementar esta limitada a 180 grados y
#        la funcion de disminuir esta limitada a 0 grados.
def increment_angle(entry_widget, step):
    try:
        current_angle = float(entry_widget.get())
        new_angle = min(current_angle + step, 180)
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, str(new_angle))
    except ValueError:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, "0")

def decrement_angle(entry_widget, step):
    try:
        current_angle = float(entry_widget.get())
        new_angle = max(current_angle - step, 0)
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, str(new_angle))
    except ValueError:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, "0")

#=============================================================================================================
# Aqui comienza la estructura de la interfaz grafica, se declara un root
#=============================================================================================================

root = tk.Tk()
root.title('HMI | PATH: Nahui 1.0')
root.minsize(600, 400)
root.protocol('WM_DELETE_WINDOW', on_closing)

distance_var = tk.DoubleVar(value=0)
rotation_var = tk.DoubleVar(value=0)

# Se crea un widget tipo notebook, nos permite tener los diferentes tabs del programa.
notebook = ttk.Notebook(root)
notebook.pack(pady=10, padx=10, expand=True, fill='both', ipady=10)

#=============================================================================================================
#                                                 TAB 1
#=============================================================================================================
# Brief: Crear el primer Tab, aqui se encuentra el HMI para crear una nueva trayectoria
#        en este tab se debe de poder generar una trayectoria indicando valores de angulo y
#        desplazamiento generando los waypoints por los cuales el robot debe de pasar.
tab1 = ttk.Frame(notebook)
tab1.columnconfigure(0, weight=3)
tab1.columnconfigure(1, weight=1)
tab1.rowconfigure(0, weight=1)

# Left frame
left_frame = ttk.Frame(tab1, borderwidth=2, relief='groove', padding=10)
left_frame.grid(row=0, column=0, padx=(0,5), pady=5, sticky='nsew')

#left_label = ttk.Label(left_frame, text='Trajectory Preview', font=('Helvetica', 10,'bold'))
#left_label.pack(padx=10, pady=10)

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
plt.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.1)
fig.set_figwidth(1)
fig.set_figheight(1)

canvas = FigureCanvasTkAgg(fig, master=left_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

# Right frame
right_frame = ttk.Frame(tab1, borderwidth=2, relief='groove', padding='10 15 10 15')
right_frame.grid(row=0, column=1, padx=(5,0), pady=5, sticky='nsew')

right_label = ttk.Label(right_frame, text='Trajectory Configuration', font=('Helvetica', 8,'bold'))
#right_label.pack(padx=10, pady=10)

right_frame.columnconfigure(0, weight=0)
right_frame.columnconfigure(1, weight=1)

row_idx = 0

# Distance configuration
ttk.Label(right_frame, text='Distance:', font=15).grid(row=row_idx, column=0, sticky='w', pady=5)
dist_label_val = ttk.Label(right_frame, text='0.0', font=10)
dist_label_val.grid(row=row_idx, column=1, sticky='e', pady=5)
row_idx += 1

distance_slider = ttk.Scale(right_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=distance_var, command=update_preview_label)
distance_slider.grid(row=row_idx, column=0, columnspan=2, sticky='ew', pady=(0, 15), ipady=2)
row_idx += 1

#Rotation configuration
ttk.Label(right_frame, text='Rotation:', font=15).grid(row=row_idx, column=0, sticky='w', pady=5)
rot_label_val = ttk.Label(right_frame, text='0.0º', font=10)
rot_label_val.grid(row=row_idx, column=1, sticky='e', pady=5)
row_idx += 1

rotation_slider = ttk.Scale(right_frame, from_=0, to=360, orient=tk.HORIZONTAL, variable=rotation_var, command=update_preview_label)
rotation_slider.grid(row=row_idx, column=0, columnspan=2, sticky='ew', pady=(0, 25), ipady=2)
row_idx += 1

# Button configuration
add_button = ttk.Button(right_frame, text='Add Waypoint', command=add_waypoint)
add_button.grid(row=row_idx, column=0, columnspan=2, sticky='ew', pady=5, ipady=10)
row_idx += 1

remove_button = ttk.Button(right_frame, text='Remove Waypoint', command=remove_waypoint)
remove_button.grid(row=row_idx, column=0, columnspan=2, sticky='ew', pady=5, ipady=10)
row_idx += 1

ttk.Label(right_frame, text='').grid(row=row_idx, column=0, pady=10)
row_idx += 1

execute_traj = ttk.Button(right_frame, text='Execute Trajectory', command=lambda: control.execute_trajectory(waypoints), style='Accent.TButton')
execute_traj.grid(row=row_idx, column=0, columnspan=2, sticky='ew', pady=10, ipady=10)
row_idx += 1

# Add Tab 1 to notebook
notebook.add(tab1, text='Trajectory Control')

#=============================================================================================================
#                                                 TAB 2
#=============================================================================================================
# Brief: Crear el segundo Tab, aqui se mantiene el codigo usado para hacer pruebas de servos.
#        Para cada servo se da un boton en el que se puede ingresar un angulo en grado al que 
#        se pueden mover los servos.
tab2 = ttk.Frame(notebook)
inner_frame = ttk.Frame(tab2, padding='10')
inner_frame.pack(expand=True)

# Shoulder servos
row_num = 0
ttk.Label(inner_frame, text='Shoulder servos', font=('Helvetica', 8,'bold')).grid(row=row_num, column=0, columnspan=6, pady=2)
row_num += 1

ttk.Label(inner_frame, text="Shoulder 1 Angle:").grid(row=row_num, column=0, sticky="e", padx=5, pady=5)
shoulder_1_entry = ttk.Entry(inner_frame)
shoulder_1_entry.insert(0, '0')
shoulder_1_entry.grid(row=row_num, column=1, padx=5, pady=5)
shoulder_1_dec_button10 = ttk.Button(inner_frame, text="-10", width=5, command=lambda: decrement_angle(shoulder_1_entry, 10))
shoulder_1_dec_button10.grid(row=row_num, column=2, padx=2, pady=5)
shoulder_1_dec_button = ttk.Button(inner_frame, text="-", width=2, command=lambda: decrement_angle(shoulder_1_entry, 1))
shoulder_1_dec_button.grid(row=row_num, column=3, padx=2, pady=5)
shoulder_1_inc_button = ttk.Button(inner_frame, text="+", width=2, command=lambda: increment_angle(shoulder_1_entry, 1))
shoulder_1_inc_button.grid(row=row_num, column=4, padx=2, pady=5)
shoulder_1_inc_button10 = ttk.Button(inner_frame, text="+10", width=5, command=lambda: increment_angle(shoulder_1_entry, 10))
shoulder_1_inc_button10.grid(row=row_num, column=5, padx=2, pady=5)
row_num += 1

ttk.Label(inner_frame, text="Shoulder 2 Angle:").grid(row=row_num, column=0, sticky="e", padx=5, pady=5)
shoulder_2_entry = ttk.Entry(inner_frame)
shoulder_2_entry.insert(0, '0')
shoulder_2_entry.grid(row=row_num, column=1, padx=5, pady=5)
shoulder_2_dec_button10 = ttk.Button(inner_frame, text="-10", width=5, command=lambda: decrement_angle(shoulder_2_entry,10))
shoulder_2_dec_button10.grid(row=row_num, column=2, padx=2, pady=5)
shoulder_2_dec_button = ttk.Button(inner_frame, text="-", width=2, command=lambda: decrement_angle(shoulder_2_entry, 1))
shoulder_2_dec_button.grid(row=row_num, column=3, padx=2, pady=5)
shoulder_2_inc_button = ttk.Button(inner_frame, text="+", width=2, command=lambda: increment_angle(shoulder_2_entry, 1))
shoulder_2_inc_button.grid(row=row_num, column=4, padx=2, pady=5)
shoulder_2_inc_button10 = ttk.Button(inner_frame, text="+10", width=5, command=lambda: increment_angle(shoulder_2_entry, 10))
shoulder_2_inc_button10.grid(row=row_num, column=5, padx=2, pady=5)
row_num += 1

ttk.Label(inner_frame, text="Shoulder 3 Angle:").grid(row=row_num, column=0, sticky="e", padx=5, pady=5)
shoulder_3_entry = ttk.Entry(inner_frame)
shoulder_3_entry.insert(0, '0')
shoulder_3_entry.grid(row=row_num, column=1, padx=5, pady=5)
shoulder_3_dec_button10 = ttk.Button(inner_frame, text="-10", width=5, command=lambda: decrement_angle(shoulder_3_entry, 10))
shoulder_3_dec_button10.grid(row=row_num, column=2, padx=2, pady=5)
shoulder_3_dec_button = ttk.Button(inner_frame, text="-", width=2, command=lambda: decrement_angle(shoulder_3_entry, 1))
shoulder_3_dec_button.grid(row=row_num, column=3, padx=2, pady=5)
shoulder_3_inc_button = ttk.Button(inner_frame, text="+", width=2, command=lambda: increment_angle(shoulder_3_entry, 1))
shoulder_3_inc_button.grid(row=row_num, column=4, padx=2, pady=5)
shoulder_3_inc_button10 = ttk.Button(inner_frame, text="+10", width=5, command=lambda: increment_angle(shoulder_3_entry, 10))
shoulder_3_inc_button10.grid(row=row_num, column=5, padx=2, pady=5)
row_num += 1

ttk.Label(inner_frame, text="Shoulder 4 Angle:").grid(row=row_num, column=0, sticky="e", padx=5, pady=5)
shoulder_4_entry = ttk.Entry(inner_frame)
shoulder_4_entry.insert(0, '0')
shoulder_4_entry.grid(row=row_num, column=1, padx=5, pady=5)
shoulder_4_dec_button10 = ttk.Button(inner_frame, text="-10", width=5, command=lambda: decrement_angle(shoulder_4_entry, 10))
shoulder_4_dec_button10.grid(row=row_num, column=2, padx=2, pady=5)
shoulder_4_dec_button = ttk.Button(inner_frame, text="-", width=2, command=lambda: decrement_angle(shoulder_4_entry, 1))
shoulder_4_dec_button.grid(row=row_num, column=3, padx=2, pady=5)
shoulder_4_inc_button = ttk.Button(inner_frame, text="+", width=2, command=lambda: increment_angle(shoulder_4_entry, 1))
shoulder_4_inc_button.grid(row=row_num, column=4, padx=2, pady=5)
shoulder_4_inc_button10 = ttk.Button(inner_frame, text="+10", width=5, command=lambda: increment_angle(shoulder_4_entry, 10))
shoulder_4_inc_button10.grid(row=row_num, column=5, padx=2, pady=5)
row_num += 1

ttk.Separator(inner_frame, orient='horizontal').grid(row=row_num, column=0, columnspan=6, sticky='ew', pady=10)
row_num += 1

#Elbow servos
ttk.Label(inner_frame, text="Elbow Servos", font=('Helvetica', 8,'bold')).grid(row=row_num, column=0, columnspan=4, pady=2)
row_num += 1

ttk.Label(inner_frame, text="Elbow 1 Angle:").grid(row=row_num, column=0, sticky="e", padx=5, pady=5)
elbow_1_entry = ttk.Entry(inner_frame)
elbow_1_entry.insert(0, '0')
elbow_1_entry.grid(row=row_num, column=1, padx=5, pady=5)
elbow_1_dec_button10 = ttk.Button(inner_frame, text="-10", width=5, command=lambda: decrement_angle(elbow_1_entry, 10))
elbow_1_dec_button10.grid(row=row_num, column=2, padx=2, pady=5)
elbow_1_dec_button = ttk.Button(inner_frame, text="-", width=2, command=lambda: decrement_angle(elbow_1_entry, 1))
elbow_1_dec_button.grid(row=row_num, column=3, padx=2, pady=5)
elbow_1_inc_button = ttk.Button(inner_frame, text="+", width=2, command=lambda: increment_angle(elbow_1_entry, 1))
elbow_1_inc_button.grid(row=row_num, column=4, padx=2, pady=5)
elbow_1_inc_button10 = ttk.Button(inner_frame, text="+10", width=5, command=lambda: increment_angle(elbow_1_entry, 10))
elbow_1_inc_button10.grid(row=row_num, column=5, padx=2, pady=5)
row_num += 1

ttk.Label(inner_frame, text="Elbow 2 Angle:").grid(row=row_num, column=0, sticky="e", padx=5, pady=5)
elbow_2_entry = ttk.Entry(inner_frame)
elbow_2_entry.insert(0, '0')
elbow_2_entry.grid(row=row_num, column=1, padx=5, pady=5)
elbow_2_dec_button10 = ttk.Button(inner_frame, text="-10", width=5, command=lambda: decrement_angle(elbow_2_entry, 10))
elbow_2_dec_button10.grid(row=row_num, column=2, padx=2, pady=5)
elbow_2_dec_button = ttk.Button(inner_frame, text="-", width=2, command=lambda: decrement_angle(elbow_2_entry, 1))
elbow_2_dec_button.grid(row=row_num, column=3, padx=2, pady=5)
elbow_2_inc_button = ttk.Button(inner_frame, text="+", width=2, command=lambda: increment_angle(elbow_2_entry, 1))
elbow_2_inc_button.grid(row=row_num, column=4, padx=2, pady=5)
elbow_2_inc_button10 = ttk.Button(inner_frame, text="+10", width=5, command=lambda: increment_angle(elbow_2_entry, 10))
elbow_2_inc_button10.grid(row=row_num, column=5, padx=2, pady=5)
row_num += 1

ttk.Label(inner_frame, text="Elbow 3 Angle:").grid(row=row_num, column=0, sticky="e", padx=5, pady=5)
elbow_3_entry = ttk.Entry(inner_frame)
elbow_3_entry.insert(0, '0')
elbow_3_entry.grid(row=row_num, column=1, padx=5, pady=5)
elbow_3_dec_button10 = ttk.Button(inner_frame, text="-10", width=5, command=lambda: decrement_angle(elbow_3_entry, 10))
elbow_3_dec_button10.grid(row=row_num, column=2, padx=2, pady=5)
elbow_3_dec_button = ttk.Button(inner_frame, text="-", width=2, command=lambda: decrement_angle(elbow_3_entry, 1))
elbow_3_dec_button.grid(row=row_num, column=3, padx=2, pady=5)
elbow_3_inc_button = ttk.Button(inner_frame, text="+", width=2, command=lambda: increment_angle(elbow_3_entry, 1))
elbow_3_inc_button.grid(row=row_num, column=4, padx=2, pady=5)
elbow_3_inc_button10 = ttk.Button(inner_frame, text="+10", width=5, command=lambda: increment_angle(elbow_3_entry, 10))
elbow_3_inc_button10.grid(row=row_num, column=5, padx=2, pady=5)
row_num += 1

ttk.Label(inner_frame, text="Elbow 4 Angle:").grid(row=row_num, column=0, sticky="e", padx=5, pady=5)
elbow_4_entry = ttk.Entry(inner_frame)
elbow_4_entry.insert(0, '0')
elbow_4_entry.grid(row=row_num, column=1, padx=5, pady=5)
elbow_4_dec_button10 = ttk.Button(inner_frame, text="-10", width=5, command=lambda: decrement_angle(elbow_4_entry, 10))
elbow_4_dec_button10.grid(row=row_num, column=2, padx=2, pady=5)
elbow_4_dec_button = ttk.Button(inner_frame, text="-", width=2, command=lambda: decrement_angle(elbow_4_entry, 1))
elbow_4_dec_button.grid(row=row_num, column=3, padx=2, pady=5)
elbow_4_inc_button = ttk.Button(inner_frame, text="+", width=2, command=lambda: increment_angle(elbow_4_entry, 1))
elbow_4_inc_button.grid(row=row_num, column=4, padx=2, pady=5)
elbow_4_inc_button10 = ttk.Button(inner_frame, text="+10", width=5, command=lambda: increment_angle(elbow_4_entry, 10))
elbow_4_inc_button10.grid(row=row_num, column=5, padx=2, pady=5)
row_num += 1

# Execute Button
button_frame = ttk.Frame(inner_frame)
button_frame.grid(row=row_num, column=0, columnspan=6, pady=(15, 5))

execute_button = ttk.Button(button_frame, text="Execute Servos", command=lambda: control.execute_servos(shoulder_1_entry, shoulder_2_entry, shoulder_3_entry, shoulder_4_entry, elbow_1_entry, elbow_2_entry, elbow_3_entry, elbow_4_entry))
execute_button.pack(side=tk.LEFT, padx=5)

# Home Button
home_button = ttk.Button(button_frame, text='Set servos home', command=control.home)
home_button.pack(side=tk.LEFT, padx=5)

# Forward Button Test
forward_button = ttk.Button(button_frame, text='Test Forward (1)', command=control.forward1)
forward_button.pack(side=tk.LEFT, padx=5)

# Add Tab 2 to notebook
notebook.add(tab2, text='Servo Test')


#=============================================================================================================
#                                                 TAB 3
#=============================================================================================================
# Brief: Aqui se pueden definir variables de control como el valor de los PID's etc.
tab3 = ttk.Frame(notebook)
notebook.add(tab3, text='Control Config')
toggle_tab3 = ttk.Button(tab3, text='Toggle Fullscreen', command=toggle_fullscreen)
toggle_tab3.pack(side=tk.TOP, pady=5, ipady=10)

# Se crea el boton para hacer toggle a fullscreen
fullscreen_button = ttk.Button(root, text='Toggle fullscreen', command=toggle_fullscreen)
fullscreen_button.pack(side=tk.BOTTOM, pady=5, ipady=10)

root.mainloop()
