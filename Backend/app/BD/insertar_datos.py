import sys
import os
import pandas as pd
from shapely import wkt
# Añade la ruta de la carpeta 'Bases' al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

#import modelo
#import conectar
from . import conectar
from . import modelo 
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
# from geoalchemy2 import WKTElement, Geometry
# import geopandas as gpd
# from geopandas import GeoDataFrame
# from shapely.geometry import Point, Polygon, MultiPolygon
# from geoalchemy2.shape import to_shape


def cargar_Aerolineas(gdf,session):
    for index, row in gdf.iterrows():
        aerolinea = modelo.Aerolineas(
            id=row['Codigo'],
            nombre_aerolinea=row['Nombre'],
            )
        session.add(aerolinea)
    session.commit()

def cargar_pasaje(gdf,session):
    for index, row in gdf.iterrows():
        pasaje = modelo.Pasaje(
            codigo_reserva=row['codigo_reserva'],
            id_aerolinea=row['id_aerolinea'],
            id_cliente=row['id_cliente'],
            id_vuelo=row['id_vuelo'],
            asiento=row['asiento'],
            e_ticket=row['e_ticket']
        )
        session.add(pasaje)
    session.commit()



def cargar_vuelo(gdf,session):
    id_vuelos = [] 
    for index, row in gdf.iterrows():
        vuelo = modelo.Vuelo(
            id_aerolinea = row['id_aerolinea'],
            origen = row['origen'],
            fecha_origen = row['fecha_origen'],
            destino = row['destino'],
            fecha_destino = row['fecha_destino']
        )
        session.add(vuelo)
        session.flush()  # Sincroniza la sesión para obtener el id autogenerado
        #row['id_vuelo'] = vuelo.id
        id_vuelos.append(vuelo.id)  # Guarda el id en la lista
    
        gdf['id_vuelo'] = id_vuelos
        
    session.commit()

def cargar_usuario(gdf,session):
    id_clientes = [] 
    for index, row in gdf.iterrows():
        usuario = modelo.Usuario(
            nombre = row['nombre'],
            correo= row['correo']
        )
        session.add(usuario)
        session.flush()
        #row['id_cliente'] = usuario.id
        id_clientes.append(usuario.id)  # Guarda el id en la lista
    
        gdf['id_cliente'] = id_clientes
    session.commit()


def subir_dfs(df):
    engine = conectar.conect_principal()# Conexión a la base de datos
    modelo.Base.metadata.create_all(engine)# Crear todas las tablas en la base de datos si no existen
    Session = sessionmaker(bind=engine)# Crear una sesión de SQLAlchemy
    session = Session()
    df["correo"]="insomnesoul@gmail.com"
    cargar_usuario(df,session)#df[['nombre', 'correo']]
    cargar_vuelo(df,session)
    cargar_pasaje(df,session)
    cargar_usuario(df,session)
    session.close()

# Ejecutar la carga de datos
if __name__ == '__main__':
    engine = conectar.conect_principal()# Conexión a la base de datos
    modelo.Base.metadata.create_all(engine)# Crear todas las tablas en la base de datos si no existen
    Session = sessionmaker(bind=engine)# Crear una sesión de SQLAlchemy
    session = Session()
    df = pd.DataFrame(pd.read_excel("../assets/Aerolineas.xlsx"))
    print(df)
    cargar_Aerolineas(df,session)
    #subir_pdfs()
    session.close()
