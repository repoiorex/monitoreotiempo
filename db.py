import sqlite3
from tkinter import messagebox
import time

# Crear conexión con la base de datos
def conectar_db():
    conn = sqlite3.connect('usuarios.db')
    return conn

# Crear tablas si no existen
def crear_tablas():
    conn = conectar_db()
    cursor = conn.cursor()

    # Tabla para usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        horario TEXT,
        usuario TEXT UNIQUE,
        contrasena TEXT,
        hora_login REAL  -- Guardamos el tiempo en que el usuario se logueó
    );
    ''')

    # Tabla para administradores
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        horario TEXT,
        usuario TEXT UNIQUE,
        contrasena TEXT,
        admin INTEGER DEFAULT 1  -- 1 para admin, 0 para usuarios con permisos limitados si es necesario
    );
    ''')

    conn.commit()
    conn.close()

# Verificar si el usuario y la contraseña son correctos
def verificar_usuario(usuario, contrasena):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE usuario = ? AND contrasena = ?", (usuario, contrasena))
    user = cursor.fetchone()
    conn.close()
    return user

# Verificar si el usuario es administrador
def verificar_admin(usuario, contrasena):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins WHERE usuario = ? AND contrasena = ?", (usuario, contrasena))
    admin = cursor.fetchone()
    conn.close()
    return admin

# Registrar la hora de inicio de sesión
def registrar_hora_login(usuario):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET hora_login = ? WHERE usuario = ?", (time.time(), usuario))
    conn.commit()
    conn.close()

# Obtener todos los usuarios logueados
def obtener_usuarios_logueados():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, usuario, hora_login FROM users WHERE hora_login IS NOT NULL")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios
