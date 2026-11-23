"""Limpieza de datos de ElectroHogar. Uso: python limpieza.py (ajustar la ruta del Excel original)."""
import pandas as pd, numpy as np
f='Data_ElectroHogar_Retail.xlsx'
t=pd.read_excel(f,'Sucia_Hechos_Transacciones'); p=pd.read_excel(f,'Dim_Productos'); c=pd.read_excel(f,'Dim_Clientes'); o=pd.read_excel(f,'Fact_Objetivos')
log={}
log['filas_origen']=len(t)
for k in ['SKU_Codigo_Ref','ID_Cliente_Ref','ID_Transaccion']: t[k]=t[k].str.strip()
t=t.drop_duplicates(); log['duplicados_eliminados']=log['filas_origen']-len(t)
s=t.Fecha_Operacion.astype(str).str.strip()
iso=s.str.match(r'^\d{4}[-/]'); dmy=s.str.match(r'^\d{2}-\d{2}-\d{4}$')
assert (iso|dmy).all()
t['Fecha']=pd.NaT
t.loc[iso,'Fecha']=pd.to_datetime(s[iso].str[:10].str.replace('/','-'),format='%Y-%m-%d')
t.loc[dmy,'Fecha']=pd.to_datetime(s[dmy],format='%d-%m-%Y')
t['Fecha']=pd.to_datetime(t['Fecha'])
log['descuento_nulo_a_0']=int(t.Descuento.isna().sum()); t['Descuento']=t.Descuento.fillna(0)
t['Venta_Bruta']=t.Cantidad*t.Precio_Unitario; t['Venta_Neta']=(t.Venta_Bruta*(1-t.Descuento)).round(2)
catmap={'ELEC':'Electrónica','LBLA':'Línea Blanca','TECN':'Tecnología','HOGA':'Hogar'}
p['SKU_Clave']=p.SKU_Clave.str.strip(); p['Categoria']=p.SKU_Clave.str[:4].map(catmap); p=p.rename(columns={'Producto_Descripcion':'Producto'})[['SKU_Clave','Producto','Categoria']]
c['ID_Cliente_Clave']=c.ID_Cliente_Clave.str.strip()
t=t.rename(columns={'SKU_Codigo_Ref':'SKU','ID_Cliente_Ref':'ID_Cliente'})
assert t.SKU.isin(p.SKU_Clave).all() and t.ID_Cliente.isin(c.ID_Cliente_Clave).all()
t=t.merge(p,left_on='SKU',right_on='SKU_Clave').merge(c,left_on='ID_Cliente',right_on='ID_Cliente_Clave')
fact=t[['ID_Transaccion','Fecha','SKU','ID_Cliente','Cantidad','Precio_Unitario','Descuento','Venta_Bruta','Venta_Neta']].sort_values('Fecha')
fact.to_csv('Fact_Ventas.csv',index=False); p.to_csv('Dim_Productos.csv',index=False)
c.rename(columns={'ID_Cliente_Clave':'ID_Cliente','Region_Geografica':'Region'}).to_csv('Dim_Clientes.csv',index=False)
o['Fecha']=pd.to_datetime(dict(year=o.Anio,month=o.Mes_Num,day=1))
o.rename(columns={'Categoria_Agrupador':'Categoria'})[['Fecha','Categoria','Meta_Financiera']].to_csv('Fact_Objetivos.csv',index=False)
log['filas_limpias']=len(fact); log['venta_neta']=float(fact.Venta_Neta.sum()); log['meta']=int(o.Meta_Financiera.sum())
print(log)
