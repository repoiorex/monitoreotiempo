import tkinter as tk
from tkinter import messagebox
import time
from db import verificar_usuario, registrar_hora_login, obtener_usuarios_logueados
import pandas as pd
from db import obtener_usuarios_logueados  # Asegúrate de tener esta función en tu db.py
import tkinter.filedialog



# Función para mostrar los usuarios logueados
def mostrar_usuarios_logueados():
    # Crear ventana para mostrar usuarios logueados
    ventana_usuarios = tk.Tk()
    ventana_usuarios.title("Usuarios Logueados")
    label_admin = tk.Label(ventana_usuarios, text="Bienvenido al Panel de Administrador", font=("Arial", 20))
    label_admin.pack()

    # Obtener los usuarios logueados
    usuarios = obtener_usuarios_logueados()

    # Función para calcular el tiempo de sesión
    def tiempo_sesion(hora_login):
        tiempo_transcurrido = time.time() - hora_login
        horas = int(tiempo_transcurrido // 3600)
        minutos = int((tiempo_transcurrido % 3600) // 60)
        segundos = int(tiempo_transcurrido % 60)
        return f"{horas:02}:{minutos:02}:{segundos:02}"

    # Crear una lista para almacenar la información que se mostrará y se exportará
    usuarios_data = []

    # Mostrar lista de usuarios logueados y su tiempo de sesión
    for i, (id, nombre, usuario, hora_login) in enumerate(usuarios):
        tiempo = tiempo_sesion(hora_login)
        label_usuario = tk.Label(ventana_usuarios, text=f"{nombre} ({usuario}) - Tiempo de sesión: {tiempo}")
        label_usuario.pack()

        # Añadir la información a la lista de datos
        usuarios_data.append([nombre, usuario, tiempo])
        

    # Función para exportar los datos a un archivo Excel
    def exportar_a_excel():
        if usuarios_data:
            # Abrir cuadro de diálogo para elegir la carpeta donde guardar el archivo
            carpeta_destino = tkinter.filedialog.askdirectory(title="Selecciona una carpeta para guardar el archivo")
            
            # Si el usuario no seleccionó ninguna carpeta, salimos de la función
            if not carpeta_destino:
                messagebox.showwarning("Advertencia", "No se ha seleccionado ninguna carpeta. El archivo no será exportado.")
                return

            # Crear un DataFrame de pandas
            df = pd.DataFrame(usuarios_data, columns=["Nombre", "Usuario", "Tiempo de sesión"])

            # Especificar la ruta completa del archivo Excel
            archivo_excel = f"{carpeta_destino}/usuarios_logueados.xlsx"

            try:
                # Guardar el archivo Excel en la ubicación seleccionada
                df.to_excel(archivo_excel, index=False, engine='openpyxl')
                messagebox.showinfo("Éxito", f"El reporte ha sido exportado a {archivo_excel}.")
            except Exception as e:
                messagebox.showerror("Error", f"Hubo un error al guardar el archivo: {e}")
        else:
            messagebox.showwarning("Sin datos", "No hay usuarios logueados para exportar.")

    # Botón para exportar los datos a un archivo Excel
    boton_exportar = tk.Button(ventana_usuarios, text="Exportar a Excel", command=exportar_a_excel)
    boton_exportar.pack()

    # Botón para actualizar la lista de usuarios logueados
    def actualizar_usuarios():
        for widget in ventana_usuarios.winfo_children():
            widget.destroy()

        # Mostrar nuevamente la lista de usuarios logueados
        ventana_usuarios.destroy()
        mostrar_usuarios_logueados()

    # Botón para actualizar la lista de usuarios
    boton_actualizar = tk.Button(ventana_usuarios, text="Actualizar", command=actualizar_usuarios)
    boton_actualizar.pack()
    ventana_usuarios.mainloop()
