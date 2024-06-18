import mariadb
from config import USER_DB,PASS_DB,HOST_DB,DB,PORT_DB
# Diccionario Datos de Conexion

def conn_db():
    try:
        conn = mariadb.connect(
            user = USER_DB,
            password = PASS_DB,
            host = HOST_DB,
            database = DB,
            port = PORT_DB
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")

    cur = conn.cursor()
    try: 
        cur.execute("select name,ratio from cedears")
    except mariadb.Error as e: 
        print(f"Error: {e}")
    
    for (name, ratio) in cur:
        print(f"Nombre: {name} - Ratio: {ratio}")

if __name__ == '__main__':
    conn_db()

