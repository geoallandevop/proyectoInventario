from models.database import get_session
from models.entities import Usuario, Rol

def authenticate_user(email, password):
    """
    Autentica un usuario contra la base de datos SQL Server.
    Retorna (Usuario, mensaje) si es exitoso, o (None, mensaje) si falla.
    """
    session = get_session()
    if not session:
        return None, "Error de conexión a la base de datos."
        
    try:
        # Buscar usuario por correo y estado ACTIVO
        usuario = session.query(Usuario).filter(
            Usuario.CORREO == email,
            Usuario.ESTADO == True
        ).first()
        
        if not usuario:
            return None, "Correo no encontrado o usuario inactivo."
            
        # Conservamos el formato de contraseña utilizado por la base actual.
        if usuario.PASSW_ORD == password:
            return usuario, "Login exitoso"
        else:
            return None, "Contraseña incorrecta."
            
    except Exception as e:
        return None, f"Error en la consulta: {str(e)}"
    finally:
        session.close()

def get_user_role(usuario):
    """Retorna el nombre del rol del usuario para configurar los permisos en el dashboard."""
    session = get_session()
    if not session or not usuario:
        return "DESCONOCIDO"
        
    try:
        rol = session.query(Rol).filter(Rol.ID_ROL == usuario.ID_ROL).first()
        # Normalizamos a mayúsculas para facilitar las condicionales
        return rol.NOMBRE_ROL.upper() if rol else "SIN ROL"
    except Exception:
        return "SIN ROL"
    finally:
        session.close()
