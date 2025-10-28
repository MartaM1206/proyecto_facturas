# librerías
import os
import re
import pdfplumber
from pypdf import PdfReader, PdfWriter
from fpdf import FPDF
import pandas as pd

# Carpetas
input_folder = "facturas_agua"
renamed_folder = "renombradas_agua"
paginas_folder = "unidas_agua"
os.makedirs(renamed_folder, exist_ok=True)
os.makedirs(paginas_folder, exist_ok=True)

# Diccionario para pasar de meses a números
meses = {
    "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
    "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
    "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
}
# lista para generar el resumen
resumen = []

# Procesar cada archivo en la carpeta de entrada
for archivo in os.listdir(input_folder):
    if archivo.endswith(".pdf"):
        ruta = os.path.join(input_folder, archivo)
        with pdfplumber.open(ruta) as pdf:
            texto = pdf.pages[0].extract_text()

            # Buscar la fecha de emisión de la factura
            fecha_formateada = "sin_fecha"
            lineas = texto.split("\n")
            # La fecha de emisión aparece justo debajo de la línea que contiene "fecha de emisión"
            for i, linea in enumerate(lineas):
                if "fecha de emisión" in linea.lower() and i + 1 < len(lineas):
                    siguiente = lineas[i + 1].lower()
                    match_fecha = re.search(r"(\d{1,2}) de (\w+) de (\d{4})", siguiente)
                    if match_fecha:
                        dia, mes_texto, anio = match_fecha.groups()
                        fecha_formateada = f"{meses[mes_texto.lower()]}-{anio}"
                        print(f"📅 Fecha de emisión detectada: {fecha_formateada}")
                    else:
                        print(f"⚠️ Línea siguiente encontrada pero sin fecha válida: {siguiente}")
                    break
            else:
                print("⚠️ No se encontró ninguna línea con 'fecha de emisión'.")

            # Buscar el importe
            importe = "0.00"
            lineas = texto.split("\n")

            for linea in lineas:
                if "total factura" in linea.lower():
                    match_importe = re.search(r"([\d]+[.,][\d]{2})\s*(€|eur)?", linea.lower())
                    if match_importe:
                        importe = match_importe.group(1).replace(",", ".")
                        print(f"✅ Importe detectado: {importe} €")
                    else:
                        print(f"⚠️ Línea encontrada pero sin importe válido: {linea}")
                    break


        # Renombrar los archivos según la fecha
        nuevo_nombre_base = f"Agua_{fecha_formateada}.pdf"
        nuevo_nombre = nuevo_nombre_base
        nueva_ruta = os.path.join(renamed_folder, nuevo_nombre)

        # control de duplicados
        contador = 1
        if os.path.exists(nueva_ruta):
            print(f"⚠️ Archivo duplicado detectado: {nuevo_nombre_base}")
            while os.path.exists(nueva_ruta):
                nuevo_nombre = f"Agua_{fecha_formateada}_{contador}.pdf"
                nueva_ruta = os.path.join(renamed_folder, nuevo_nombre)
                contador += 1
        os.rename(ruta, nueva_ruta)

        # extrae la primera página de cada factura y la guarda en la carpeta de páginas
        reader = PdfReader(nueva_ruta)
        writer = PdfWriter()
        writer.add_page(reader.pages[0])
        pagina_path = os.path.join(paginas_folder, nuevo_nombre)
        with open(pagina_path, "wb") as f:
            writer.write(f)

        # Añadir los datos al resumen
        resumen.append({
            "fecha": fecha_formateada,
            "importe": float(importe),
            "archivo": nuevo_nombre
        })

# convierte la lista de diccionarios resumen en un dataframe de pandas
resumen_df = pd.DataFrame(resumen)
pdf_tabla = FPDF()
pdf_tabla.add_page()
pdf_tabla.set_font("Arial", size=12)
pdf_tabla.cell(60, 10, "Fecha emisión", 1)
pdf_tabla.cell(40, 10, "Importe (EUR)", 1)
pdf_tabla.ln()

# filas por cada factura
for _, fila in resumen_df.iterrows():
    pdf_tabla.cell(60, 10, fila["fecha"], 1)
    pdf_tabla.cell(40, 10, f"{fila['importe']:.2f}", 1)
    pdf_tabla.ln()

#  fila de total 
total = resumen_df["importe"].sum()
pdf_tabla.set_font("Arial", style="B", size=12)
pdf_tabla.cell(60, 10, "TOTAL", 1)
pdf_tabla.cell(40, 10, f"{total:.2f}", 1)
pdf_tabla.ln()

portada_path = "portada_resumen_agua.pdf"
pdf_tabla.output(portada_path)

# une todo en un solo pdf
merger = PdfWriter()
merger.append(portada_path)
for archivo in resumen_df["archivo"]:
    pagina_path = os.path.join(paginas_folder, archivo)
    merger.append(pagina_path)

merger.write("facturas_agua_resumen.pdf")
merger.close()

print("✅ Script completado: facturas renombradas, unidas y resumen generado.")
