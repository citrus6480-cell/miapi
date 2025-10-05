from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de tu DB en Railway
DB_USER = "root"
DB_PASSWORD = "oIEMTnSEGsGZXoImnDVyytAZhlYRQxYC"  # si tu MySQL local no tiene clave, déjalo vacío
DB_HOST = "shinkansen.proxy.rlwy.net"
DB_PORT = "47944"  # el puerto por defecto de MySQL
DB_NAME = "railway" 

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# Conexión
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
