from prettytable import PrettyTable
from var import cant_cedears,cedears,ratios,tickers
import yfinance as yf

# Ejemplo:
# cant_cedears = { 'AAPL.BA':1 }
# cedears = [AAPL.BA]
# ratios = { 'AAPL.BA':10 }
# tickers = ['AAPL']
ba = ".BA"

def obtener_precios_acciones():
       
    precios_acciones = {}

    for ticker in tickers:
        try:
            data = yf.Ticker(ticker)
            precios_acciones[ticker] = data.history(period="1d")["Close"].iloc[-1]
        except:
            precios_acciones[ticker] = 0
        # print(f"{ticker}: $ {round(data.history(period="1d")["Close"].iloc[-1],2)}")

    return precios_acciones

def obtener_precios_cedears():

    precios_cedears = {}
    
    for cedear in cedears:
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
        # cedear = ''.join(list(filter(lambda x: ticker in x, precios_cedears.keys())))
        
        if ticker == "YPF":
            cedear = "YPFD.BA"
        else:
            cedear = ticker + ba

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


def obtener_tabla(precios_acciones,precios_cedears,precios_ccl,valorizado):
    table = PrettyTable()
    table.align = "r"
    table.field_names = ["Accion","Accion (US$)","CEDEARs ($)","CCL ($)","Ratios","Cantidad","Valorizado en $","Valorizado en US$"]

    for ticker, precio in precios_acciones.items():
        # cedear = ''.join(list(filter(lambda x: ticker in x, precios_cedears.keys())))
        precio = precio
        if ticker == "YPF":
            cedear = "YPFD.BA"
        else:
            cedear = ticker + ba

        try:
            table.add_row([ticker,"{:.2f}".format(precio),"{:.2f}".format(precios_cedears[cedear]),"{:.2f}".format(precios_ccl[cedear]),ratios.get(cedear),cant_cedears.get(cedear),"{:.2f}".format(valorizado[cedear]),"{:.2f}".format(valorizado[cedear]/precios_ccl[cedear])])
        except:
            table.add_row([ticker,"{:.2f}".format(precio),"{:.2f}".format(precios_cedears[cedear]),"{:.2f}".format(precios_ccl[cedear]),ratios.get(cedear),cant_cedears.get(cedear),"{:.2f}".format(valorizado[cedear]),"{:.2f}".format(valorizado[cedear]/precios_ccl[cedear])])
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
