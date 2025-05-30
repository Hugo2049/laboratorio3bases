from django.db import connection

def crear_vista_ventas():
    with connection.cursor() as cursor:
        cursor.execute("DROP VIEW IF EXISTS vista_ventas_completa")
        cursor.execute("""
        CREATE VIEW vista_ventas_completa AS
        SELECT 
            v.id AS venta_id,
            v.fecha_venta,
            c.nombre || ' ' || c.apellido AS cliente,
            l.titulo AS libro,
            v.cantidad,
            v.precio_unitario,
            v.descuento,
            v.estado
        FROM libros_venta v
        JOIN libros_cliente c ON v.cliente_id = c.id
        JOIN libros_libro l ON v.libro_id = l.id;
    """)
        print("✅ Vista 'vista_ventas_completa' creada con éxito.")
