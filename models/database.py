from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ---------------------------------------------------------
# CONFIGURACIÓN DE CONEXIÓN A SQL SERVER
# ---------------------------------------------------------
# Por favor, asegúrate de que el Driver "ODBC Driver 17 for SQL Server" 
# (o la versión que tengas, como 18) esté instalado en Windows.

SERVER = 'DESKTOP-21A3CDJ\SQLEXPRESS' # o 'localhost\\SQLEXPRESS' si usas Express
DATABASE = 'SISTEMA_KARDEX'

# OPCIÓN 1: Autenticación de Windows (Trusted Connection)
CONNECTION_STRING = f"mssql+pyodbc://@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

# OPCIÓN 2: Autenticación de SQL Server (Usuario y Contraseña)
# USER = 'sa'
# PASSWORD = 'tu_password'
# CONNECTION_STRING = f"mssql+pyodbc://{USER}:{PASSWORD}@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server"

Base = declarative_base()

try:
    engine = create_engine(CONNECTION_STRING, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    print(f"Error inicializando el motor de BD: {e}")
    SessionLocal = None

def get_session():
    """Retorna una nueva sesión de base de datos."""
    if SessionLocal:
        return SessionLocal()
    return None
