import sqlite3

conexion = sqlite3.connect('db.sqlite3')
cursor = conexion.cursor()

print("📋 Listado de tablas existentes:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablas = cursor.fetchall()

for tabla in tablas:
    print(f"- {tabla[0]}")
