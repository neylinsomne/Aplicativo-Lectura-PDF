from BD import insertar_datos, conectar
import lectura
import logging
from datetime import datetime
import pandas as pd
import glob
import lectura
import os
import re

filename = f'logs/pipeline.log'
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename=filename)


def aerolienas():
    engine = conectar.conect_principal()
    df = pd.read_sql_table("Aerolineas", con=engine)
    #aeros=df["nombre_aerolinea"]
    return df

def pipeline_general():
    logging.info(f'Start data pipeline at {datetime.now()}')
    ruta_pdfs = "assets/Tiquetes/*.pdf"
    ruta_jpgs= "assets/Tiquetes/*.jpg"
    archivos_pdf = glob.glob(ruta_pdfs)
    archivos_jpg = glob.glob(ruta_jpgs)
    print(archivos_pdf)
    output_folder = "assets/prueba_imagenes"
    os.makedirs(output_folder, exist_ok=True) 
    logging.info(f'Start conversion pdfs y analizis de estos: {datetime.now()}')
    for archivo in archivos_pdf:#[3:4]: #[:2]
         logging.info(f"Procesando: {archivo} a {datetime.now()}")
         put_pipeline(archivo)
    print(archivos_jpg)
    for jpg in archivos_jpg:
        logging.info(f"ahora leyendo imagenes: a {datetime.now()}")
        put_pipeline(jpg)


def put_pipeline(archivo_path):
    logging.info(f'Start data processing new baby at {datetime.now()}')
    tipo = archivo_path.split(".")[-1].lower()  
    if tipo == "jpg" or tipo == "png":
        logging.info("Se identificó como una imagen, procesar como imagen.")
        logging.warning(f"Recuerda configurar el idioma aquí (imagenes put baby)!!  ")
        idiomas=['en']#,'es']
        df= lectura.procesar_imagen(archivo_path,idiomas)
        
        lista_textos = df['text'].tolist()
        nombre_archivo = os.path.basename(archivo_path).replace('.pdf', '')
        with open(f'textos/textos_de_imagenes/lista_textos_{nombre_archivo}.txt', 'w') as archivo:
            for item in lista_textos:
                archivo.write(f"{item}\n")
        organize(df,lista_textos)
    
    elif tipo == "pdf":
        logging.info("Se identificó como un PDF, procesar como PDF.")
        logging.warning(f"Recuerda configurar el idioma aquí (PDF put baby)!!  {datetime.now()}")
        logging.info(f"Procesando: {archivo_path} a {datetime.now()}")
        logging.warning(f"Recuerda configurar el idioma aquí en pdfs!! ")
        idiomas=['es']
        texto_extraido=lectura.extraer_texto(archivo_path)
        texto_pdf = texto_extraido.split('\n')
        texto_de_pdf = [lectura.eliminar_tildes(linea.strip()) for linea in texto_pdf if linea.strip()]
        
        imagenes_generadas = lectura.prueba_cambio(archivo_path)
        logging.info(f"Imagenes generadas!")
        dataframes = []
        for imagen in imagenes_generadas:
            try:
                df = lectura.procesar_imagen(imagen,idiomas)
                dataframes.append(df)
                #lectura.imprimir_easyocr(imagen,df)
                
            except Exception as e:
                logging.error(f"Problema al procesar la imagen archivo {archivo}(generar el df),{e}{datetime.now()}")
        if dataframes:
            df = pd.concat(dataframes, ignore_index=True)
            #print (df)
        
        else:
            logging.error("No se generaron DataFrames")
       
        #lista_textos = df['text'].tolist()
        nombre_archivo = os.path.basename(archivo_path).replace('.pdf', '')
        with open(f'textos/lista_textos_{nombre_archivo}.txt', 'w') as archivo:
            for item in texto_de_pdf:
                archivo.write(f"{item}\n")
        organize(df,texto_de_pdf)
    else:
        logging.error(f"[{datetime.now()}] Entró un archivo erroneo; este es de: {tipo}")
        dicc={}
        
    #dicc=organize(df,archivo_path)



def organize(df_img,texto_pdf): ## se encarga de organizar el
    xd=aerolienas()
    aeros = xd['nombre_aerolinea'].str.lower().str.strip().tolist()
    print(aeros)
    #print ("ESTO ES AERO: ",aero)
    df_img['text'] = df_img['text'].str.lower().str.strip()
    print(df_img['text'])
    palabra= None
    logging.info("Usando imagen para analizar la aerolinea")
    for index, text in df_img['text'].items():
        text = text.lower().strip()
        if text in aeros:
            palabra = text
            print(f"la palabra es {palabra}")
    if palabra==None: 
        logging.error("NO SE ENCONTRÓ QUE FUERA DE UNA DE LAS AEROLINEAS REGISTRADAS!!")
        #break
               
    logging.info(f"Texto procesado: es de la aerolinea {palabra}")
    
    aerolinea_id = xd.loc[xd['nombre_aerolinea'].str.lower().str.strip() == palabra, 'id']
    if not aerolinea_id.empty:
        info = {"id_aerolinea": aerolinea_id.values[0]}
    else:
        logging.error(f"No se encontró el ID para la aerolínea {palabra}")
        info = {"id_aerolinea": None}
    
    if palabra=="avianca":
        for i, linea in enumerate(texto_pdf):
            info['nombre'] = texto_pdf[0].strip()
            if linea == "Verifica la sala en las pantallas del aeropuerto":
                try:
                    info['origen'] = texto_pdf[i + 4].strip()
                except: info['origen']=None
                try:
                    info['fecha_origen'] = texto_pdf[i + 2].strip()
                except: info['fecha_origen']=None
                try:
                    info['destino'] = texto_pdf[i + 9].strip()
                except: info['destino']=None
                try:
                    info['fecha_destino'] = texto_pdf[i + 8].strip()
                except: info['fecha_destino']=None
               
            elif linea == "ASIENTO":
                info['asiento'] = texto_pdf[i + 1].strip()
            if "Reserva" in linea:
                info["codigo_reserva"] = linea.split(":")[1].strip()
            
            elif "E-ticket" in linea:
                info["e_ticket"] = linea.split(":")[1].strip()
        
        print("PRINTEANDO INFO: \n", info)
        df = pd.DataFrame([info])
        insertar_datos.subir_dfs(df)
    if palabra=="wingo":
        return 0
    if palabra=="air Europa":
        return info
    if palabra=="jetsmart":
        for i, linea in enumerate(texto_pdf):
            if linea == "Pasajero":
                info['nombre'] = texto_pdf[i + 1].strip()
            elif linea == "Codigo de reserva":
                info['codigo_reserva'] = texto_pdf[i + 1].strip()
            elif linea == "Fecha":
                fecha=texto_pdf[i + 1].strip()    
            elif linea == "Origen":
                info['origen'] = texto_pdf[i + 2].strip() + texto_pdf[i + 3].strip()
                tiempo_origen = re.search(r'\d{2}:\d{2} \w{2}', texto_pdf[i + 4])
                if tiempo_origen:
                    info['fecha_origen'] = fecha + ' ' + tiempo_origen.group()   # Extrae solo el tiempo
                else:info['fecha_origen']=None
            elif linea == "Destino":
                info['destino'] = texto_pdf[i + 2].strip() + texto_pdf[i + 3].strip()
                tiempo_destino = re.search(r'\d{2}:\d{2} \w{2}', texto_pdf[i + 3])
                if tiempo_destino:
                    info['fecha_destino'] = fecha + ' ' + tiempo_destino.group()  # Extrae solo el tiempo
                else:info['fecha_destino']=None    
            elif linea == "ASIENTO":
                info['asiento'] = texto_pdf[i + 5].strip()
        info['e_ticket']=None
        print("PRINTEANDO INFO: \n", info)
        df = pd.DataFrame([info])
        insertar_datos.subir_dfs(df) 
    if palabra=="latam":
        return info
    if palabra=="klm":
        return info
    


if __name__ == '__main__':
    archivo_path="assets/Tiquetes/Pasabordo1.pdf"
    put_pipeline(archivo_path)
    