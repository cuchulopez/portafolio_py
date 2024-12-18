import psycopg2
from config import USER_DB,PASS_DB,HOST_DB,DB,PORT_DB
from datetime import datetime 
from var import tickers_full
# Diccionario Datos de Conexion

def get_portafolio():
    portafolio = {}
    try:
        db = psycopg2.connect(
            user = USER_DB,
            password = PASS_DB,
            host = HOST_DB,
            database = DB,
            port = PORT_DB
        )
        cursor = db.cursor()

        query = f"select ticker,ratio,cantidad from public.portafolio"
        cursor.execute(query, )

        for ticker,ratio,cantidad in cursor:
            print(f"Accion: {ticker} - Ratio: {ratio} - Cantidad: {cantidad}")
            
        
        cursor.close()
        db.close()

        return portafolio


    except (Exception, psycopg2.DatabaseError) as e:
        print(f"Error connecting to MariaDB Platform: {e}")


def select(accion):
    try:
        db = psycopg2.connect(
            user = USER_DB,
            password = PASS_DB,
            host = HOST_DB,
            database = DB,
            port = PORT_DB
        )
        cursor = db.cursor()

        query = f"select id_ticker,ticker from public.portafolio where ticker = '{accion}'"
        cursor.execute(query, (accion,))

        for id_ticker,ticker in cursor:
            print(f"Id: {id_ticker} - Nombre: {ticker}")
        
        cursor.close()
        db.close()

    except (Exception, psycopg2.DatabaseError) as e:
        print(f"Error connecting to MariaDB Platform: {e}")
    #    for ticker_full in tickers_full:
    #        accion = list(ticker_full[0].keys())[0]
            
            # ratio = ticker_full[1]
            # cant_cedear = list(ticker_full[0].values())[0]  
            
        #     db.execute("INSERT INTO portafolio (ticker,ratio,cantidad) VALUES (?,?,?)",(accion,ratio,cant_cedear))

        # conn.commit()


def update_ticker(ticker,new_cant):
    try:
        db = psycopg2.connect(
            user = USER_DB,
            password = PASS_DB,
            host = HOST_DB,
            database = DB,
            port = PORT_DB
        )
        db.autocommit=True
        cursor = db.cursor()
        query = f"UPDATE portafolio SET cantidad = {new_cant} WHERE ticker = '{ticker}'"
        cursor.execute(query)
        
        cursor.close()
        db.close()

    except (Exception, psycopg2.DatabaseError) as e:
        print(f"Error connecting to MariaDB Platform: {e}")

def update_data(precios_acciones,precios_cedears):
    fecha = datetime.now().strftime("%Y-%m-%d") # YYYY-MM-DD
    hora = datetime.now().strftime("%H:%M:%S")
    try:
        db = psycopg2.connect(
            user = USER_DB,
            password = PASS_DB,
            host = HOST_DB,
            database = DB,
            port = PORT_DB
        )
        cursor = db.cursor()
        
        query = "INSERT INTO portafolio.precios (id_ticker,fecha,hora) VALUES (?,?,?)"
        cursor.execute(query,(2,fecha,hora))

        cursor.close()
        db.close()

    except (Exception, psycopg2.DatabaseError) as e:
        print(f"Error connecting to MariaDB Platform: {e}")

    
    #print(precios_acciones)
    #print(precios_cedears)
    print(fecha, hora)

if __name__ == "__main__":
    # portafolio = get_portafolio()
    update_ticker("PG",49)
    get_portafolio()
