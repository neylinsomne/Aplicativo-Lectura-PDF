from sqlalchemy import Column, Integer, String, Float, create_engine

def conect_principal():
    DATABASE_TYPE = 'postgresql'
    DBAPI = 'psycopg2'
    #ENDPOINT = '5480'  # dirección del host
    HOST = 'localhost'  # dirección del host
    USER = 'postgres'       # usuario de la base de datos
    PASSWORD = 'xd'         # contraseña del usuario
    PORT = 5436             # puerto mapeado de PostgreSQL en Docker
    DATABASE = 'Pasajes'   # nombre de la base de datos


    # Crear la URL de conexión
    DATABASE_URL = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    engine = create_engine(DATABASE_URL)
    return engine

def ret_data_url():
    DATABASE_TYPE = 'postgresql'
    DBAPI = 'psycopg2'
    #ENDPOINT = '5480'  # dirección del host
    HOST = 'localhost'  # dirección del host
    USER = 'postgres'       # usuario de la base de datos
    PASSWORD = 'xd'         # contraseña del usuario
    PORT = 5436             # puerto mapeado de PostgreSQL en Docker
    DATABASE = 'Pasajes'   # nombre de la base de datos


    # Crear la URL de conexión
    DATABASE_URL = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    return DATABASE_URL