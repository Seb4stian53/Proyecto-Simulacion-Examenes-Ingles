import mysql
from conn import get_connection

def fetch_prueba():
    connection = get_connection()

    if connection is None:
       print("No hay conexion en la base de datos")
       return
    
    try:
      cursor = connection.cursor()

      query = "SELECT * FROM prueba"

      cursor.execute(query)

      results = cursor.fetchall()

      for row in results:
        print(row)
    except mysql.connector.Error as err:
        print(f"Error:{err}")
    finally:
        if cursor:
           cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
   fetch_prueba()

      