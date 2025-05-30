import sqlite3

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

# Mostrar tablas actuales
print("🔍 Tablas actuales en la base de datos:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
for row in cursor.fetchall():
    print("-", row[0])

# Borrar la vista si ya existe
print("\n🔄 Eliminando vista si ya existe...")
cursor.execute("DROP VIEW IF EXISTS vista_libros_completa")

# Crear de nuevo la vista
print("🛠 Creando vista vista_libros_completa...")
cursor.execute("""
CREATE VIEW vista_libros_completa AS
SELECT 
    l.id AS libro_id,
    l.titulo,
    l.descripcion,
    l.isbn,
    l.precio,
    l.stock,
    l.fecha_publicacion,
    l.paginas,
    g.nombre AS genero,
    ap.nombre AS autor_principal,
    ac.nombre AS autor_colaborador,
    c.nombre AS categoria,
    l.activo
FROM libros_libro l
LEFT JOIN libros_genero g ON g.id = l.genero_id
LEFT JOIN libros_autor ap ON ap.id = l.autor_principal_id
LEFT JOIN libros_libro_autores la ON la.libro_id = l.id
LEFT JOIN libros_autor ac ON ac.id = la.autor_id
LEFT JOIN libros_libro_categorias lc ON lc.libro_id = l.id
LEFT JOIN libros_categoria c ON c.id = lc.categoria_id;
""")

conn.commit()
conn.close()
print("✅ Vista recreada con éxito.")
