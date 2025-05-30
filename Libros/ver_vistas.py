import sqlite3

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

print("📋 Vistas disponibles en la base de datos:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
vistas = cursor.fetchall()

if vistas:
    for vista in vistas:
        print("-", vista[0])
else:
    print("⚠️ No se encontraron vistas.")

conn.close()
