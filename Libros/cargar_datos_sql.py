import os
import django
from django.db import connection

# Configuración de entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'venta_libros.settings')
django.setup()

def cargar_sql_desde_archivo(archivo_sql):
    with open(archivo_sql, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    with connection.cursor() as cursor:
        cursor.executescript(sql_script)
    
    print("✅ Datos insertados correctamente.")

if __name__ == "__main__":
    cargar_sql_desde_archivo('data.sql')

