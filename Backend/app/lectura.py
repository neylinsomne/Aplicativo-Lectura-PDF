import pandas as pd 
import logging
import glob
import PyPDF2
import easyocr
from io import StringIO
import numpy as np
import cv2
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdf2image import convert_from_path
import shutil
import os
import unicodedata
import matplotlib.pyplot as plt
from PIL import Image

def eliminar_tildes(texto):
    # Normalizar el texto a su forma compatible NFC y luego eliminar las tildes
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'  # 'Mn' significa un carácter de marca, como las tildes
    )


def extraer_texto(in_file): #PDFREADER
    output_string = StringIO()
    
    # Abre el archivo en modo binario
    with open(in_file, 'rb') as f:
        parser = PDFParser(f)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        
        # Procesar cada página
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    
    return output_string.getvalue()

    

def cambiar_pdf_jpg():
    poppler_path='C:/Users/neylp/Downloads/Release-24.07.0-0/poppler-24.07.0/Library/bin'
    ruta_pdf = "assets/Tiquetes/*.pdf"
    ruta_jpg = "assets/Tiquetes/*.jpg"
    ruta_png = "assets/Tiquetes/*.png"
    archivos_pdf = glob.glob(ruta_pdf)
    archivos_jpg = glob.glob(ruta_jpg)
    archivos_png = glob.glob(ruta_png)
    output_folder = "assets/Tiquetes_imagenes"
    os.makedirs(output_folder, exist_ok=True)
    for archivo in archivos_pdf:
        paginas = convert_from_path(pdf_path=archivo,poppler_path=poppler_path)# Convierte PDF a imágenes
        #----- Guardar cada página como una imagen PNG
        for i, pagina in enumerate(paginas):
            nombre_base = os.path.basename(archivo).replace(".pdf", "")
            pagina.save(os.path.join(output_folder, f"{nombre_base}_pagina_{i+1}.png"), "PNG")

    for archivo in archivos_jpg:
        shutil.copy(archivo, output_folder)

    for archivo in archivos_png:
        shutil.copy(archivo, output_folder)
    print(f"Conversión y copia completa. Los archivos están en {output_folder}")    




def procesar_imagen(archivo, idiomas):
    reader = easyocr.Reader(idiomas, gpu = True)
    results = reader.readtext(archivo)
    df=pd.DataFrame(results, columns=['bbox','text','conf'])
    return df

def prueba_cambio(archivo):
    poppler_path='C:/Users/neylp/Downloads/Release-24.07.0-0/poppler-24.07.0/Library/bin'
    output_folder = "assets/prueba_imagenes/archivos"
    os.makedirs(output_folder, exist_ok=True)
    paginas = convert_from_path(pdf_path=archivo,poppler_path=poppler_path)
    imagenes_generadas = []
    for i, pagina in enumerate(paginas):
        nombre_base = os.path.basename(archivo).replace(".pdf", "")
        ruta_imagen = os.path.join(output_folder, f"{nombre_base}_pagina_{i+1}.png")
        pagina.save(ruta_imagen, "PNG")
        imagenes_generadas.append(ruta_imagen)
    return imagenes_generadas


def imprimir_easyocr(img_fn, easyocr_df):
        # Lee la imagen original
    img = cv2.imread(img_fn)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Crea la figura y el eje para la visualización
    fig, ax = plt.subplots(figsize=(10, 10))

    # Mostrar imagen original
    ax.imshow(img)

    # Obtener los resultados de EasyOCR para la imagen actual
    if not easyocr_df.empty:
        for _, row in easyocr_df.iterrows():
            text = row['text']
            bbox = np.array(row['bbox'])

            # Dibujar las líneas del bounding box
            ax.plot([bbox[0][0], bbox[1][0]], [bbox[0][1], bbox[1][1]], color='red', linewidth=0.5)
            ax.plot([bbox[1][0], bbox[2][0]], [bbox[1][1], bbox[2][1]], color='red', linewidth=0.5)
            ax.plot([bbox[2][0], bbox[3][0]], [bbox[2][1], bbox[3][1]], color='red', linewidth=0.5)
            ax.plot([bbox[3][0], bbox[0][0]], [bbox[3][1], bbox[0][1]], color='red', linewidth=0.5)

            # Calcular el punto medio del bounding box
            mid_point = np.mean(bbox, axis=0).astype(int)

            # Dibujar una línea desde el punto medio hasta el texto
            ax.plot([mid_point[0], mid_point[0]], [mid_point[1], mid_point[1]-10], color='blue', linewidth=0.5)

            # Añadir el texto
            ax.text(mid_point[0], mid_point[1]-12, text, color='blue', fontsize=6, ha='center', va='bottom')

    else:
        ax.text(0.5, 0.5, 'No se detectaron textos', fontsize=12, ha='center', transform=ax.transAxes)

    # Ajusta el título y elimina los ejes
    ax.set_title('Resultados EasyOCR', fontsize=24)
    ax.axis('off')

    # Guarda la imagen procesada
    output_folder = "assets/prueba_imagenes/easy_results"
    os.makedirs(output_folder, exist_ok=True)
    output_img_path = os.path.join(output_folder, f"{os.path.basename(img_fn).split('.')[0]}_resultado.png")
    plt.savefig(output_img_path, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"Imagen procesada guardada en {output_img_path}")
    
    
    #ruta_assets = os.path.abspath(os.path.join(os.path.dirname(__file__), '../assets/Tiquetes/*.pdf'))

if __name__ == '__main__':
    ruta_pdfs = "assets/Tiquetes/*.pdf"
    ruta_jpgs= "assets/Tiquetes/*.jpg"
    archivos_pdf = glob.glob(ruta_pdfs)
    archivos_jpg = glob.glob(ruta_jpgs)
    print(archivos_pdf)
    
    output_folder = "assets/prueba_imagenes"
    os.makedirs(output_folder, exist_ok=True) 
    
    for archivo in archivos_pdf[2:3]: #[:2]
         print(f"Procesando: {archivo}")
         imagenes_generadas = prueba_cambio(archivo)
         idiomas=['es']
         for imagen in imagenes_generadas:
    
             df = procesar_imagen(imagen,idiomas)
             print(df.head(), "\n ahora lo chido:", df.columns)  
             #imprimir_easyocr(imagen, df)
    
    # print(archivos_jpg)
    # for jpg in archivos_jpg:
    #     print("ahora leyendo imagenes:")
    #     #lenguajes=input()
    #     idiomas=['en']#,'es']
    #     df= procesar_imagen(jpg,idiomas)
    #     print(df)  
    #     imprimir_easyocr(jpg, df)