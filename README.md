# laboratorio3bases


![11](https://github.com/user-attachments/assets/113b610f-1f93-4ea8-998f-b7e8f4218583)
![12](https://github.com/user-attachments/assets/73d2cace-c39a-4d57-94e6-c40ac99b2a6b)
![13](https://github.com/user-attachments/assets/eb9953f7-b346-46b9-b965-0ed58263cd66)

git clone https://github.com/Hugo2049/laboratorio3bases
cd Libros

# Crear el entorno virtual
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# instalar dependencias
pip install django

# Cargar los datos iniciales
python manage.py migrate
python manage.py loaddata data.sql  

# Ejecutar el proyecto
python manage.py runserver

Accede a la aplicación en: http://127.0.0.1:8000

