import mysql

def get_connection():
    config = {
        'user' : 'root',
        'password' : '',
        'host' : 'localhost',
        'database' : 'nombre',
        'raise_on_warnings' : True
    }

    try: 
        connection = mysql.connector.connect(**config)
        return connection
    except mysql.connector.Error as err:
        print(f"Error {err}")
        return None