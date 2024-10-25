from datetime import datetime
from precios import *
from db import select,update_data


if __name__ == "__main__":
   fecha_hoy = datetime.now().strftime("%H:%M - %d/%m/%Y")
   valorizado_total = 0

   precios_acciones = obtener_precios_acciones()
   precios_cedears = obtener_precios_cedears()
   precios_ccl = obtener_precios_ccl(precios_acciones, precios_cedears)
   valorizado = obtener_valorizado(precios_cedears)
   table_portafolio = obtener_tabla(precios_acciones,precios_cedears,precios_ccl,valorizado)
   
   # select('NDVA')
   # update_data(precios_acciones,precios_cedears)


   for cedear, precio in valorizado.items():
      valorizado_total += precio

   print("\n",fecha_hoy)
   print(table_portafolio)
   print(f"Dolar CCL (promedio): $ {dolar_ccl_promedio(precios_ccl):.2f}")
   print(f"Total Valorizado: $ {valorizado_total:.2f}  -  US$ {(valorizado_total / dolar_ccl_promedio(precios_ccl)):.2f}\n")

