
# 📄 Automatización de Facturas de Agua

Este proyecto permite procesar automáticamente facturas de agua en formato PDF, extrayendo datos clave como la **fecha de emisión** y el **importe total**, renombrando los archivos, generando una **tabla resumen** y uniendo todas las primeras páginas en un único documento.

## 🚀 Funcionalidades

- 📥 Procesa todos los PDFs de una carpeta de entrada
- 🧾 Extrae fecha e importe desde el texto de la factura
- 🏷️ Renombra cada archivo con formato `Agua_MM-YYYY.pdf`
- 📄 Guarda la primera página de cada factura en una carpeta aparte
- 📊 Genera una tabla resumen en PDF con todos los importes y el total
- 📎 Une todas las primeras páginas en un único PDF consolidado

## 🛠️ Tecnologías utilizadas

- `Python 3`
- `pdfplumber`(https://github.com/jsvine/pdfplumber) para extracción de texto
- `pypdf` (https://pypi.org/project/pypdf/) para manipulación de PDFs
- `FPDF` para generar la tabla resumen
- `pandas` (https://pandas.pydata.org/) para estructurar los datos

## 📂 Estructura de carpetas

```
facturas_agua/              # Carpeta de entrada con los PDFs originales
renombradas_agua/           # PDFs renombrados por fecha
unidas_agua/                # Primeras páginas extraídas
portada_resumen_agua.pdf    # Tabla resumen generada
facturas_agua_resumen.pdf   # Documento final con todas las páginas
```

## 📌 Autoría

Desarrollado por [Marta Llorden](https://www.linkedin.com/in/marta-llorden)

## 🔮 Next steps

- Añadir soporte para otros tipos de facturas (electricidad, gas)

