# ElectroHogar: tablero de ventas con KPIs y pronóstico a 12 meses

Análisis de ventas 2026 de una cadena de electrodomésticos: limpieza de datos, KPIs y pronóstico de ventas para 2027.

## Qué incluye
- `python/limpieza.py`: limpia el Excel original (duplicados, espacios, 3 formatos de fecha, descuentos vacíos, categorías inconsistentes).
- `python/pronostico.py`: agrega ventas por mes y calcula el pronóstico a 12 meses (regresión lineal, intervalo del 80 %).
- `data/`: tablas limpias para Power BI (`ventas_mensuales`, `Dim_Productos`, `Dim_Clientes`, `Fact_Objetivos`, `pronostico`). La tabla transaccional completa (22.000 filas) se regenera con `python/limpieza.py` a partir del Excel original.
- `powerbi/Limpieza_PowerQuery.m`: la misma limpieza en Power Query.
- `powerbi/Medidas_DAX.dax`: modelo y medidas (Venta Neta, Ticket Promedio, Descuento Medio, Cumplimiento de meta, variación mensual, pronóstico).

## Resultados 2026
- Venta neta: $59.853 M (22.000 transacciones tras quitar 350 duplicadas).
- Mes más alto: enero ($5.129 M). Más bajo: febrero ($4.531 M).
- Pronóstico 2027: $61.164 M en total. La tendencia (+9 M/mes) no es estadísticamente significativa (p = 0,61): la serie es prácticamente plana.

## Hallazgos de calidad de datos
- La meta financiera cargada suma $2.487 M, contra $59.853 M vendidos (cumplimiento superior a 2.000 %). Probable error de escala; hay que validarlo con el área comercial.
- La categoría se asignó por prefijo de SKU, porque `Dim_Productos` tenía categorías contradictorias.
- Con un solo año de historia no se puede estimar estacionalidad; el pronóstico es una referencia.

## Cómo armar el tablero en Power BI Desktop
1. Obtener datos > Texto/CSV: cargar los CSV de `data/` (o usar `Limpieza_PowerQuery.m` con el Excel original).
2. Crear las relaciones y medidas de `powerbi/Medidas_DAX.dax`.
3. Página 1: tarjetas (Venta Neta, Unidades, Transacciones, Ticket Promedio, Descuento Medio), gráfico de líneas por mes, barras por categoría, región y producto, segmentaciones de región y categoría.
4. Página 2: gráfico de líneas con Venta Neta real y Pronostico con banda (Inferior y Superior).
