import os
import re
import PyPDF2
import tkinter as tk
from tkinter import filedialog


def unir_pdf(archivos, archivo_salida):
    fusionador = PyPDF2.PdfMerger()
    for archivo in archivos:
        fusionador.append(archivo)

    with open(archivo_salida, 'wb') as archivo_salida:
        fusionador.write(archivo_salida)


def buscar_archivos_en_carpeta(carpeta, extension=".PDF"):
    archivos_encontrados = []
    for ruta, _, archivos in os.walk(carpeta):
        for archivo in archivos:
            if archivo.upper().endswith(extension.upper()):
                archivos_encontrados.append(os.path.join(ruta, archivo))
    return archivos_encontrados


def obtener_numero_legajo(nombre_archivo):
    # Buscar el número de legajo después de la variante de "Leg" o "Legajo"
    match = re.search(r'(Legajo|Leg)_*(\d+)', nombre_archivo, re.IGNORECASE)
    if match:
        return int(match.group(2))
    else:
        return None


def unir_archivos_por_legajo(carpeta, archivo_salida):
    archivos_en_carpeta = buscar_archivos_en_carpeta(carpeta)
    archivos_por_legajo = {}

    for archivo in archivos_en_carpeta:
        numero_legajo = obtener_numero_legajo(archivo)
        if numero_legajo is not None:
            if numero_legajo in archivos_por_legajo:
                archivos_por_legajo[numero_legajo].append(archivo)
            else:
                archivos_por_legajo[numero_legajo] = [archivo]

    for numero_legajo, archivos in archivos_por_legajo.items():
        if len(archivos) >= 2:
            print(f"Uniendo archivos del legajo {numero_legajo}...")
            for archivo in archivos:
                print(f" - {archivo}")
                # Obtener la ruta del directorio del archivo main.py
                directorio_actual = os.path.dirname(os.path.abspath(__file__))
                # Crear la carpeta "output" si no existe
                carpeta_output = os.path.join(directorio_actual, "output")
                if not os.path.exists(carpeta_output):
                    os.makedirs(carpeta_output)
                # Ruta absoluta para el archivo de salida dentro de la carpeta "output"
                ruta_salida = os.path.join(carpeta_output, f"{numero_legajo}.pdf")
                print(f"Archivos a unir: {archivos}")
                unir_pdf(archivos, ruta_salida)
        else:
            print(f"No hay suficientes archivos para el legajo {numero_legajo}")

    print("Proceso completado.")


def seleccionar_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        carpeta_con_archivos.set(carpeta)


def unir_archivos():
    carpeta = carpeta_con_archivos.get()
    archivo_salida = nombre_archivo_salida.get()

    if not carpeta:
        mensaje.set("Por favor, selecciona una carpeta.")
        return

    if not archivo_salida:
        archivo_salida = "resultado"

    unir_archivos_por_legajo(carpeta, archivo_salida)
    mensaje.set("Proceso completado.")


# Crear la ventana principal de la aplicación
ventana = tk.Tk()
ventana.title("Unir Archivos PDF por Legajo")

# Variables para almacenar la carpeta y el nombre del archivo de salida
carpeta_con_archivos = tk.StringVar()
nombre_archivo_salida = tk.StringVar()

# Etiqueta y campo de texto para seleccionar la carpeta con archivos PDF
lbl_carpeta = tk.Label(ventana, text="Carpeta con archivos PDF:")
lbl_carpeta.pack(pady=5)
txt_carpeta = tk.Entry(ventana, textvariable=carpeta_con_archivos)
txt_carpeta.pack(pady=5)
btn_seleccionar_carpeta = tk.Button(ventana, text="Seleccionar Carpeta", command=seleccionar_carpeta)
btn_seleccionar_carpeta.pack(pady=5)

# Etiqueta y campo de texto para ingresar el nombre del archivo de salida
lbl_archivo_salida = tk.Label(ventana, text="Nombre del archivo de salida:")
lbl_archivo_salida.pack(pady=5)
txt_archivo_salida = tk.Entry(ventana, textvariable=nombre_archivo_salida)
txt_archivo_salida.pack(pady=5)

# Botón para iniciar la unión de archivos
btn_unir_archivos = tk.Button(ventana, text="Unir Archivos", command=unir_archivos)
btn_unir_archivos.pack(pady=10)

# Etiqueta para mostrar mensajes
mensaje = tk.StringVar()
lbl_mensaje = tk.Label(ventana, textvariable=mensaje)
lbl_mensaje.pack(pady=5)

# Iniciar el bucle de la interfaz gráfica
ventana.mainloop()
