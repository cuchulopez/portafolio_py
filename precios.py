from prettytable import PrettyTable
from var import tickers_full
import yfinance as yf


# Ejemplo:
# Formato de variable tickers_full (tuplas) = ({Acción:Cantidad de CEDEARS}, Ratio)

ba = ".BA"
cant_cedears = {}
ratios = {}

def tickerToCedear(ticker):
    if ticker == "YPF":
        cedear = "YPFD.BA"
    else:
        cedear = ticker + ba

    return cedear

for ticker_full in tickers_full:
    ticker = list(ticker_full[0].keys())[0]

    cedear = tickerToCedear(ticker)

    ratios[cedear] = ticker_full[1]
    cant_cedears[cedear] = list(ticker_full[0].values())[0]

def obtener_precios_acciones():
       
    precios_acciones = {}
    precios_acciones_dia_anterior = {}

    for ticker_full in tickers_full:
        try:
            ticker = list(ticker_full[0].keys())[0]
            data = yf.Ticker(ticker)
            precios_acciones[ticker] = data.history(period="1d")["Close"].iloc[-1]
            precio_dia_anterior = data.history(period="2d")["Close"].iloc[-2]
            precios_acciones_dia_anterior[ticker] = (precios_acciones[ticker] - precio_dia_anterior) / precio_dia_anterior * 100
        except:
            precios_acciones[ticker] = 0
            precios_acciones_dia_anterior[ticker] = 0

        # print(f"{ticker}: $ {round(data.history(period="1d")["Close"].iloc[-1],2)}")

    return precios_acciones,precios_acciones_dia_anterior



def obtener_precios_cedears():

    precios_cedears = {}
    
    for ticker_full in tickers_full:
        ticker = list(ticker_full[0].keys())[0]
        cedear = tickerToCedear(ticker)

        try:
            data = yf.Ticker(cedear)
            precios_cedears[cedear] = data.history(period="1d")["Close"].iloc[-1]
            
        except:
            precios_cedears[cedear] = 0
        
        # print(f"${cedear}: ${round(data.history(period="1d")["Close"].iloc[-1],2)}")

    return precios_cedears



def obtener_precios_ccl(precios_acciones, precios_cedears):

    precios_ccl = {}
   
    for ticker,precio in precios_acciones.items():
        cedear = tickerToCedear(ticker)

        try:
            ccl = (ratios.get(cedear) * precios_cedears[cedear])/precio
        except:
            ccl = 0
        precios_ccl[cedear] = ccl
    
    return precios_ccl


def obtener_valorizado(precios_cedears):
    valorizado_cedear = {}
    
    for cedear, precio in precios_cedears.items():
        valorizado_cedear[cedear] = precio * cant_cedears[cedear]

    return valorizado_cedear


def obtener_tabla(precios_acciones,precios_cedears,precios_acciones_dia_anterior,precios_ccl,valorizado):
    table = PrettyTable()
    table.align = "r"
    table.field_names = ["Accion","Accion (US$)","Variacion (%)","CEDEARs ($)","CCL ($)","Ratios","Cantidad","Valorizado en $","Valorizado en US$"]

    # ratios = 

    for ticker, precio in precios_acciones.items():
        precio = precio
        cedear = tickerToCedear(ticker)

        try:
            table.add_row([ticker,"{:.2f}".format(precio),"{:.2f}".format(precios_acciones_dia_anterior[ticker]),"{:.2f}".format(precios_cedears[cedear]),"{:.2f}".format(precios_ccl[cedear]),ratios.get(cedear),cant_cedears.get(cedear),"{:.2f}".format(valorizado[cedear]),"{:.2f}".format(valorizado[cedear]/precios_ccl[cedear])])
        except:
            table.add_row([ticker,"{:.2f}".format(precio),"{:.2f}".format(precios_acciones_dia_anterior[ticker]),"{:.2f}".format(precios_cedears[cedear]),"{:.2f}".format(precios_ccl[cedear]),ratios.get(cedear),cant_cedears.get(cedear),"{:.2f}".format(valorizado[cedear]),"{:.2f}".format(valorizado[cedear]/precios_ccl[cedear])])
    return table


def dolar_ccl_promedio(precios_ccl):
    dolar_ccl_promedio_aux = 0
    for precio in precios_ccl.values():
       dolar_ccl_promedio_aux += precio
    
    return dolar_ccl_promedio_aux / len(precios_ccl)

if __name__ == '__main__':
    obtener_precios_acciones()
    obtener_precios_cedears()
    obtener_precios_ccl()
    obtener_valorizado()
    obtener_tabla()
