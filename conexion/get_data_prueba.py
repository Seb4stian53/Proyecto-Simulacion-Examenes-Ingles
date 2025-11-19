from database.conn import db
from mysql.connector import Error

def insertar_usuario(matricula, tipo, nombre, usuario):
    connection = db.get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO users (matricula, tipo_usuario, nombre, usuario) VALUES (%s, %s, %s, %s)"
            values = (matricula, tipo, nombre, usuario)
            cursor.execute(query, values)
            connection.commit()
            print('Usuario agregado exitosamente')
            return cursor.lastrowid
        except Error as e:
            print(f'Error al crear el usuario: {e}')
            return None
        finally:
            cursor.close()
            db.close_connection()

def obtener_usuarios():
    connection = db.get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM users"
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(f'Error al obtener usuarios: {e}')
            return None
        finally:
            cursor.close()
            db.close_connection()

if __name__ == "__main__":
    insertar_usuario("20005262", 0, "Sebastian Contreras", "seb4stian53")
    insertar_usuario("12345", 0, 'Carlito Hiram', 'carlex')
    insertar_usuario("20003025", 0, 'Gabriel Cardenas', 'Gabo05')
    
    usuarios = obtener_usuarios()
    if usuarios:
        for usuario in usuarios:
            print(usuario)