from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Aerolineas(Base):
    __tablename__ = 'Aerolineas'
    id = Column(Integer, primary_key=True)
    nombre_aerolinea = Column(String, nullable=False)

    # Relaciones con otras tablas
    vuelos = relationship('Vuelo', back_populates='aerolinea')


class Vuelo(Base):
    __tablename__ = 'Vuelo'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_aerolinea = Column(Integer, ForeignKey('Aerolineas.id'))
    origen = Column(String)
    fecha_origen = Column(String)
    destino = Column(String)
    fecha_destino = Column(String)

    # Relaciones con otras tablas
    aerolinea = relationship('Aerolineas', back_populates='vuelos')
    pasajes = relationship('Pasaje', back_populates='vuelo')

class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    correo = Column(String)
    
    # Relación con Vuelo a través de Pasaje

    pasajes = relationship('Pasaje', back_populates='cliente')

class Pasaje(Base):
    __tablename__ = 'Pasaje'

    codigo_reserva = Column(String, primary_key=True)
    id_aerolinea = Column(Integer, ForeignKey('Aerolineas.id'))
    id_cliente = Column(Integer, ForeignKey('usuario.id'))
    id_vuelo = Column(Integer, ForeignKey('Vuelo.id'))
    asiento = Column(String)
    e_ticket = Column(String)

    # Relaciones con otras tablas
    aerolinea = relationship('Aerolineas')
    cliente = relationship('Usuario', back_populates='pasajes')
    vuelo = relationship('Vuelo', back_populates='pasajes')
