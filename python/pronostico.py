"""Pronóstico a 12 meses: regresión lineal sobre 12 puntos mensuales con intervalo de predicción del 80 %.
Entrada: Fact_Ventas.csv (generado por limpieza.py). Salida: pronostico.csv"""
import pandas as pd, numpy as np
from scipy import stats
t=pd.read_csv('Fact_Ventas.csv',parse_dates=['Fecha'])
m=t.groupby(t.Fecha.dt.to_period('M').dt.to_timestamp()).Venta_Neta.sum()
y=m.values/1e6; x=np.arange(len(y))
b,a=np.polyfit(x,y,1); res=y-(a+b*x); s=np.sqrt((res**2).sum()/(len(y)-2))
tv=stats.t.ppf(0.9,len(y)-2); xm=x.mean(); sxx=((x-xm)**2).sum()
rows=[dict(Mes=d.strftime('%Y-%m-%d'),Tipo='Real',Real=round(v*1e6),Pronostico=None,Inferior=None,Superior=None) for d,v in zip(m.index,y)]
for k in range(len(y),len(y)+12):
    f=a+b*k; se=s*np.sqrt(1+1/len(y)+(k-xm)**2/sxx)
    d=m.index[-1]+pd.DateOffset(months=k-len(y)+1)
    rows.append(dict(Mes=d.strftime('%Y-%m-%d'),Tipo='Pronóstico',Real=None,Pronostico=round(f*1e6),Inferior=round((f-tv*se)*1e6),Superior=round((f+tv*se)*1e6)))
pd.DataFrame(rows).to_csv('pronostico.csv',index=False)
print('pendiente (M por mes):',round(b,2),'| p-valor:',round(stats.linregress(x,y).pvalue,2))
