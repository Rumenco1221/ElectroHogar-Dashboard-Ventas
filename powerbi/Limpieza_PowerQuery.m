// Consulta "Fact_Ventas" (Power Query, Editor avanzado). Origen: hoja Sucia_Hechos_Transacciones del Excel original.
let
  Origen = Excel.Workbook(File.Contents("Data_ElectroHogar_Retail.xlsx"), null, true),
  Hoja = Origen{[Item="Sucia_Hechos_Transacciones", Kind="Sheet"]}[Data],
  Encabezados = Table.PromoteHeaders(Hoja, [PromoteAllScalars=true]),
  Recorte = Table.TransformColumns(Encabezados, {{"SKU_Codigo_Ref", Text.Trim, type text}, {"ID_Cliente_Ref", Text.Trim, type text}, {"ID_Transaccion", Text.Trim, type text}}),
  SinDuplicados = Table.Distinct(Recorte),
  // Fechas en 3 formatos: AAAA-MM-DD, AAAA/MM/DD y DD-MM-AAAA
  Fecha = Table.AddColumn(SinDuplicados, "Fecha", each
      let t = Text.From([Fecha_Operacion]), s = Text.Start(t, 10) in
      if Text.Length(t) >= 10 and Text.At(t, 4) <> "-" and Text.At(t, 4) <> "/" then
         Date.FromText(Text.End(Text.Start(t,10),4) & "-" & Text.Middle(t,3,2) & "-" & Text.Start(t,2))
      else Date.FromText(Text.Replace(s, "/", "-")), type date),
  Descuento = Table.ReplaceValue(Fecha, null, 0, Replacer.ReplaceValue, {"Descuento"}),
  Tipos = Table.TransformColumnTypes(Descuento, {{"Cantidad", Int64.Type}, {"Precio_Unitario", Int64.Type}, {"Descuento", type number}}),
  Final = Table.RemoveColumns(Tipos, {"Fecha_Operacion"})
in
  Final
