import tkinter as tk
from tkinter import messagebox
import time
from db import verificar_usuario, registrar_hora_login, obtener_usuarios_logueados, verificar_admin
from logueados import mostrar_usuarios_logueados

# Función para iniciar sesión
def iniciar_sesion():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    # Verificar si el usuario es administrador
    admin = verificar_admin(usuario, contrasena)
    if admin:
        # Si el login es de un administrador, mostramos la interfaz de administrador
        messagebox.showinfo("Éxito", f"Bienvenido, Administrador {usuario}!")
        ventana_login.destroy()
        mostrar_interfaz_admin()  # Llamamos a la función para la interfaz del admin
        return

    # Verificar si el usuario es válido
    user = verificar_usuario(usuario, contrasena)
    if user:
        # Si el login es correcto, registrar la hora de login
        registrar_hora_login(usuario)
        # Mostrar mensaje de bienvenida y el cronómetro
        messagebox.showinfo("Éxito", f"Bienvenido, {user[1]}!")  # Mostrar nombre del usuario
        ventana_login.destroy()
        mostrar_cronometro(user)
    else:
        # Si el login falla
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# Función para mostrar el cronómetro
def mostrar_cronometro(user):
    ventana_cronometro = tk.Tk()
    ventana_cronometro.title("Cronómetro")

    tiempo_inicio = time.time()

    def actualizar_cronometro():
        tiempo_transcurrido = int(time.time() - tiempo_inicio)
        horas = tiempo_transcurrido // 3600
        minutos = (tiempo_transcurrido % 3600) // 60
        segundos = tiempo_transcurrido % 60
        cronometro_label.config(text=f"{horas:02}:{minutos:02}:{segundos:02}")
        ventana_cronometro.after(1000, actualizar_cronometro)  # Actualiza cada segundo

    cronometro_label = tk.Label(ventana_cronometro, font=("Arial", 30))
    cronometro_label.pack()

    # Iniciar el cronómetro
    actualizar_cronometro()

    ventana_cronometro.mainloop()

# Función para la interfaz del administrador
def mostrar_interfaz_admin():
    #ventana_admin = tk.Tk()
    #ventana_admin.title("Panel de Administrador")

    #label_admin = tk.Label(ventana_admin, text="Bienvenido al Panel de Administrador", font=("Arial", 20))
    #label_admin.pack()

    # Aquí puedes agregar más opciones o funcionalidades para el administrador
    #boton_ver_usuarios = tk.Button(ventana_admin, text="Ver usuarios logueados", command=mostrar_usuarios_logueados)
    #boton_ver_usuarios.pack()
    mostrar_usuarios_logueados()

    #ventana_admin.mainloop()

# Crear la ventana de login
def ventana_login():
    global ventana_login, entry_usuario, entry_contrasena

    ventana_login = tk.Tk()
    ventana_login.title("Login")

    # Etiqueta y campo de usuario
    label_usuario = tk.Label(ventana_login, text="Usuario:")
    label_usuario.pack()
    entry_usuario = tk.Entry(ventana_login)
    entry_usuario.pack()

    # Etiqueta y campo de contraseña
    label_contrasena = tk.Label(ventana_login, text="Contraseña:")
    label_contrasena.pack()
    entry_contrasena = tk.Entry(ventana_login, show="*")
    entry_contrasena.pack()

    # Botón de inicio de sesión
    boton_login = tk.Button(ventana_login, text="Iniciar sesión", command=iniciar_sesion)
    boton_login.pack()

    ventana_login.mainloop()

# Función para mostrar la ventana de usuarios logueados
def ventana_usuarios_logueados():
    mostrar_usuarios_logueados()

# Crear la ventana de login
def ventana_login():
    global ventana_login, entry_usuario, entry_contrasena

    ventana_login = tk.Tk()
    ventana_login.title("Login")

    # Etiqueta y campo de usuario
    label_usuario = tk.Label(ventana_login, text="Usuario:")
    label_usuario.pack()
    entry_usuario = tk.Entry(ventana_login)
    entry_usuario.pack()

    # Etiqueta y campo de contraseña
    label_contrasena = tk.Label(ventana_login, text="Contraseña:")
    label_contrasena.pack()
    entry_contrasena = tk.Entry(ventana_login, show="*")
    entry_contrasena.pack()

    # Botón de inicio de sesión
    boton_login = tk.Button(ventana_login, text="Iniciar sesión", command=iniciar_sesion)
    boton_login.pack()

    ventana_login.mainloop()


if __name__ == "__main__":
    # Crear tablas de la base de datos si no existen
    from db import crear_tablas
    crear_tablas()

    # Llamar a la función para mostrar la ventana de login
    ventana_login()