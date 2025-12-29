import psycopg2
import sys

# Forzar a la terminal a manejar errores de salida
sys.stdout.reconfigure(errors='replace')

try:
    conn = psycopg2.connect(
        dbname="technical_test",
        user="postgres",
        password="12345",
        host="localhost",
        port="5432",
        connect_timeout=3
    )
    print("¡Conexión exitosa!")
    conn.close()
except Exception as e:
    # Usamos repr() para ver el código crudo y evitar el error de decode
    print(f"El error real es (formato crudo): {repr(e)}")