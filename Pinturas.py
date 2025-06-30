import sqlite3
import tkinter as tk
from tkinter import font
from tkinter import messagebox


def agregar_pintura():
    ventana_emergente = tk.Toplevel(root)
    ventana_emergente.title("Nueva Pintura")
    ventana_emergente.geometry("400x200")
    ventana_emergente.configure(bg="#e6f7ff")

    # Frame para formulario
    frame_formulario = tk.Frame(ventana_emergente, bg="#f0f8ff")
    frame_formulario.pack(pady=10)

    # Fila 1
    label_color = tk.Label(frame_formulario, text="Color:", bg="#e6f7ff", font=calibri_font)
    label_color.grid(row=0, column=0, padx=10, pady=5, sticky="e")

    entry_color = tk.Entry(frame_formulario, font=calibri_font)
    entry_color.grid(row=0, column=1, padx=10, pady=5)

    # Fila 2
    label_pintura = tk.Label(frame_formulario, text="Pintura:", bg="#e6f7ff", font=calibri_font)
    label_pintura.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry_pintura = tk.Entry(frame_formulario, font=calibri_font)
    entry_pintura.grid(row=1, column=1, padx=10, pady=5)

    # Fila 3
    label_rlm = tk.Label(frame_formulario, text="RLM:", bg="#e6f7ff", font=calibri_font)
    label_rlm.grid(row=2, column=0, padx=10, pady=5, sticky="e")

    entry_rlm = tk.Entry(frame_formulario, font=calibri_font)
    entry_rlm.grid(row=2, column=1, padx=10, pady=5)

    # Función interna que se ejecuta al presionar "Guardar"
    def guardar_pintura():
        color = entry_color.get()
        pintura = entry_pintura.get()
        rlm = entry_rlm.get()

        conexion = sqlite3.connect("Pinturas.db")
        cursor = conexion.cursor()

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS ListadoPinturas (
                    Color TEXT PRIMARY KEY,
                    Pintura TEXT,
                    RLM TEXT
                )
            ''')

        try:
            cursor.execute('INSERT INTO ListadoPinturas (Color, Pintura, RLM) VALUES (?, ?, ?)', (color, pintura, rlm))
            conexion.commit()

            # Limpiar el Listbox
            listbox_pinturas.delete(0, tk.END)
            # Mostrar dato ingresado
            listbox_pinturas.insert(tk.END, f"Color: {color}, Pintura: {pintura}, RLM: {rlm}")

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Ya existe una pintura con ese color.")
        finally:
            conexion.close()
            ventana_emergente.destroy()  # Cierra la ventana al guardar

    # Frame para agrupar los botones horizontalmente
    frame_botones_guardar = tk.Frame(ventana_emergente, bg="#f0f8ff")
    frame_botones_guardar.pack(pady=10)

    boton_guardar = tk.Button(frame_botones_guardar, text="Guardar", command=guardar_pintura, font=calibri_font)
    boton_guardar.pack(side="left", padx=10)

    boton_cancelar = tk.Button(frame_botones_guardar, command=ventana_emergente.destroy, text="Cancelar",
                               font=calibri_font)
    boton_cancelar.pack(side="left", padx=10)

def modificar_pintura():
    pintura_a_modificar = buscar_pintura()

    if not pintura_a_modificar:
        messagebox.showerror("Error", "NO existe una pintura con ese color.")
        entry_name.delete(0, tk.END)
        return  # Sale de la función si no se encontró nada

    ventana_emergente = tk.Toplevel(root)
    ventana_emergente.title("Modificar Pintura")
    ventana_emergente.geometry("400x200")
    ventana_emergente.configure(bg="#e6f7ff")

    # Frame para formulario
    frame_formulario = tk.Frame(ventana_emergente, bg="#f0f8ff")
    frame_formulario.pack(pady=10)

    # Fila 1
    label_color = tk.Label(frame_formulario, text="Color:", bg="#e6f7ff", font=calibri_font)
    label_color.grid(row=0, column=0, padx=10, pady=5, sticky="e")

    entry_color_mod = tk.Entry(frame_formulario, font=calibri_font)
    entry_color_mod.grid(row=0, column=1, padx=10, pady=5)
    entry_color_mod.insert(0, pintura_a_modificar[0])

    # Fila 2
    label_pintura = tk.Label(frame_formulario, text="Pintura:", bg="#e6f7ff", font=calibri_font)
    label_pintura.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry_pintura_mod = tk.Entry(frame_formulario, font=calibri_font)
    entry_pintura_mod.grid(row=1, column=1, padx=10, pady=5)
    entry_pintura_mod.insert(0, pintura_a_modificar[1])

    # Fila 3
    label_rlm = tk.Label(frame_formulario, text="RLM:", bg="#e6f7ff", font=calibri_font)
    label_rlm.grid(row=2, column=0, padx=10, pady=5, sticky="e")

    entry_rlm_mod = tk.Entry(frame_formulario, font=calibri_font)
    entry_rlm_mod.grid(row=2, column=1, padx=10, pady=5)
    entry_rlm_mod.insert(0, pintura_a_modificar[2])

    # Frame para agrupar los botones horizontalmente
    frame_botones_modificar = tk.Frame(ventana_emergente, bg="#f0f8ff")
    frame_botones_modificar.pack(pady=10)

    boton_modificar = tk.Button(frame_botones_modificar, text="Modificar",
                               command=lambda: modificar_pintura_buscada(pintura_a_modificar,
                                                                         entry_color_mod, entry_pintura_mod,
                                                                         entry_rlm_mod, ventana_emergente),
                                font=calibri_font)
    boton_modificar.pack(side="left", padx=10)

    boton_cancelar = tk.Button(frame_botones_modificar, command=ventana_emergente.destroy, text="Cancelar",
                               font=calibri_font)
    boton_cancelar.pack(side="left", padx=10)



def eliminar_pintura():
    pintura_a_borrar=buscar_pintura()

    if not pintura_a_borrar:
        messagebox.showerror("Error", "NO existe una pintura con ese color.")
        entry_name.delete(0, tk.END)
        return  # Sale de la función si no se encontró nada

    ventana_emergente = tk.Toplevel(root)
    ventana_emergente.title("Eliminar Pintura")
    ventana_emergente.geometry("400x200")
    ventana_emergente.configure(bg="#e6f7ff")

    # Frame para formulario
    frame_formulario = tk.Frame(ventana_emergente, bg="#f0f8ff")
    frame_formulario.pack(pady=10)

    # Fila 1
    label_color = tk.Label(frame_formulario, text="Color:", bg="#e6f7ff", font=calibri_font)
    label_color.grid(row=0, column=0, padx=10, pady=5, sticky="e")

    entry_color = tk.Entry(frame_formulario, font=calibri_font)
    entry_color.grid(row=0, column=1, padx=10, pady=5)
    entry_color.insert(0, pintura_a_borrar[0])

    # Fila 2
    label_pintura = tk.Label(frame_formulario, text="Pintura:", bg="#e6f7ff", font=calibri_font)
    label_pintura.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry_pintura = tk.Entry(frame_formulario, font=calibri_font)
    entry_pintura.grid(row=1, column=1, padx=10, pady=5)
    entry_pintura.insert(0, pintura_a_borrar[1])

    # Fila 3
    label_rlm = tk.Label(frame_formulario, text="RLM:", bg="#e6f7ff", font=calibri_font)
    label_rlm.grid(row=2, column=0, padx=10, pady=5, sticky="e")

    entry_rlm = tk.Entry(frame_formulario, font=calibri_font)
    entry_rlm.grid(row=2, column=1, padx=10, pady=5)
    entry_rlm.insert(0, pintura_a_borrar[2])

    # Frame para agrupar los botones horizontalmente
    frame_botones_eliminar = tk.Frame(ventana_emergente, bg="#f0f8ff")
    frame_botones_eliminar.pack(pady=10)

    boton_eliminar = tk.Button(frame_botones_eliminar, text="Eliminar",
                               command=lambda: eliminar_pintura_buscada(pintura_a_borrar, ventana_emergente),
                               font=calibri_font)
    boton_eliminar.pack(side="left", padx=10)

    boton_cancelar = tk.Button(frame_botones_eliminar, command=ventana_emergente.destroy, text="Cancelar",
                               font=calibri_font)
    boton_cancelar.pack(side="left", padx=10)


def listar_pinturas():
    conexion = sqlite3.connect("Pinturas.db")
    cursor = conexion.cursor()

    # Crear tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ListadoPinturas (
            Color TEXT PRIMARY KEY,
            Pintura TEXT,
            RLM TEXT
        )
    ''')

    # Ejecutar la consulta después de asegurarse de que la tabla existe
    cursor.execute("SELECT * FROM ListadoPinturas")
    filas = cursor.fetchall()

    # Limpiar el Listbox
    listbox_pinturas.delete(0, tk.END)

    # Insertar cada fila en el Listbox
    for fila in filas:
        color, pintura, rlm = fila
        listbox_pinturas.insert(tk.END, f"Color: {color}, Pintura: {pintura}, RLM: {rlm}")

    # Cerrar la conexión solo al final
    conexion.close()

def limpiar_pinturas():
    # Limpiar el Listbox
    listbox_pinturas.delete(0, tk.END)

def salir():
    root.destroy()  # Esto cierra la ventana

def buscar_pintura():
    color_buscado = entry_name.get()

    conexion = sqlite3.connect("Pinturas.db")
    cursor = conexion.cursor()

    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS ListadoPinturas (
                            Color TEXT PRIMARY KEY,
                            Pintura TEXT,
                            RLM TEXT
                        )
                    ''')

    try:
        cursor.execute('Select Color, Pintura, RLM from ListadoPinturas where Color = ?', (color_buscado,))
        resultados = cursor.fetchall()

        # Limpiar el Listbox
        listbox_pinturas.delete(0, tk.END)

        if resultados:
            color, pintura, rlm = resultados[0]
            listbox_pinturas.insert(tk.END, f"Color: {color}, Pintura: {pintura}, RLM: {rlm}")
            return color, pintura, rlm
        else:
            return None
    except sqlite3.IntegrityError:
        print("Ya existe ese color en la base de datos")
    finally:
        conexion.close()

def eliminar_pintura_buscada(pintura, ventana_emergente):
    if pintura:
        color = pintura[0]
        conexion = sqlite3.connect("Pinturas.db")
        cursor = conexion.cursor()
        try:
            cursor.execute('DELETE FROM ListadoPinturas WHERE Color = ?', (color,))
            conexion.commit()
            listar_pinturas()
            ventana_emergente.destroy()
        except Exception as e:
            print("Error al eliminar:", e)
        finally:
            conexion.close()

def modificar_pintura_buscada(pintura, entry_color_mod, entry_pintura_mod, entry_rlm_mod, ventana_emergente):
    if pintura:
        color_viejo = pintura[0]  # este es el valor original de la clave primaria

        # Traemos los nuevos datos de las cajas de texto
        color_nuevo = entry_color_mod.get()
        pintura_nuevo = entry_pintura_mod.get()
        rlm_nuevo = entry_rlm_mod.get()
        conexion = sqlite3.connect("Pinturas.db")
        cursor = conexion.cursor()
        try:
            cursor.execute(
                'UPDATE ListadoPinturas SET color = ?, pintura = ?, rlm = ? WHERE color = ?',
                (color_nuevo, pintura_nuevo, rlm_nuevo, color_viejo)
            )
            conexion.commit()
            listar_pinturas()
            ventana_emergente.destroy()
        except Exception as e:
            print("Error al Modificar:", e)
        finally:
            conexion.close()

# Crea la ventana principal
root = tk.Tk()
root.title("Gestión de Pinturas")
root.geometry("680x420")
root.configure(bg="#e6f7ff")

# Fuente Calibri
calibri_font = font.Font(family="Calibri", size=12)

# Elementos de la interfaz
label_name = tk.Label(root, text="Color:", bg="#f0f8ff", font=calibri_font)
label_name.pack(pady=10)

entry_name = tk.Entry(root, font=calibri_font)
entry_name.pack(pady=5)

# Frame para agrupar los botones horizontalmente
frame_botones = tk.Frame(root, bg="#f0f8ff")
frame_botones.pack(pady=10)

button_add = tk.Button(frame_botones, text="Agregar Pintura", command=agregar_pintura, bg="#add8e6", font=calibri_font,
                       width=15)
button_add.pack(side="left", padx=5)

button_update = tk.Button(frame_botones, text="Modificar Pintura", command=modificar_pintura, bg="#90ee90",
                          font=calibri_font, width=15)
button_update.pack(side="left", padx=5)

button_delete = tk.Button(frame_botones, text="Eliminar Pintura", command=eliminar_pintura, bg="#ffcccb",
                          font=calibri_font, width=15)
button_delete.pack(side="left", padx=5)

button_listar = tk.Button(frame_botones, text="Listar Pinturas", command=listar_pinturas, bg="#ffc900",
                          font=calibri_font, width=15)
button_listar.pack(side="left", padx=5)

button_limpiar = tk.Button(frame_botones, text="Limpiar Listado", command=limpiar_pinturas, bg="#ffc900",
                          font=calibri_font, width=15)
button_limpiar.pack(side="left", padx=5)

listbox_pinturas = tk.Listbox(root, width=50, height=10, font=calibri_font)
listbox_pinturas.pack(pady=10)

button_salir = tk.Button(root, text="Salir", command=salir, bg="#ffc900", font=calibri_font, width=15)
button_salir.pack(padx=5)

# Ejecutar la aplicación
root.mainloop()
