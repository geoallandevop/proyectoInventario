from models.database import get_session
from models.entities import Categoria, UnidadMedida, Usuario, Rol, Producto

def obtener_categorias():
    session = get_session()
    if not session: return []
    try:
        categorias = session.query(Categoria).all()
        return [{"id": c.ID_CATEGORIA, "nombre": c.NOMBRE_CATEGORIA} for c in categorias]
    except Exception:
        return []
    finally:
        session.close()

def obtener_unidades():
    session = get_session()
    if not session: return []
    try:
        unidades = session.query(UnidadMedida).all()
        return [{"id": u.ID_UNIDAD, "nombre": f"{u.NOMBRE_UNIDAD} ({u.SIMBOLO})"} for u in unidades]
    except Exception:
        return []
    finally:
        session.close()

def obtener_roles():
    session = get_session()
    if not session: return []
    try:
        roles = session.query(Rol).all()
        return [{"id": r.ID_ROL, "nombre": r.NOMBRE_ROL} for r in roles]
    except Exception:
        return []
    finally:
        session.close()

def obtener_usuarios():
    session = get_session()
    if not session: return []
    try:
        usuarios = session.query(Usuario).join(Rol).all()
        return [{"id": u.ID_USUARIO, "nombre": u.NOMBRE_COMPLETO, "correo": u.CORREO, "id_rol": u.ID_ROL, "rol": u.rol.NOMBRE_ROL, "estado": u.ESTADO} for u in usuarios]
    except Exception:
        return []
    finally:
        session.close()

def crear_usuario(nombre, correo, password, id_rol):
    session = get_session()
    if not session: return False
    try:
        nuevo = Usuario(NOMBRE_COMPLETO=nombre, CORREO=correo, PASSW_ORD=password, ID_ROL=id_rol, ESTADO=True)
        session.add(nuevo)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False
    finally:
        session.close()

def actualizar_usuario(id_usr, nombre, correo, password, id_rol):
    session = get_session()
    if not session: return False
    try:
        u = session.query(Usuario).get(id_usr)
        if u:
            u.NOMBRE_COMPLETO = nombre
            u.CORREO = correo
            if password: # Si está vacío, no cambia la contraseña
                u.PASSW_ORD = password
            u.ID_ROL = id_rol
            session.commit()
            return True
        return False
    except Exception:
        session.rollback()
        return False
    finally:
        session.close()

def toggle_estado_usuario(id_usuario):
    session = get_session()
    if not session: return
    try:
        u = session.query(Usuario).get(id_usuario)
        if u:
            u.ESTADO = not u.ESTADO
            session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()

def obtener_catalogo():
    session = get_session()
    if not session: return []
    try:
        productos = session.query(Producto).all()
        return [{"id": p.ID_PRODUCTO, "codigo": p.CODIGO_UNICO, "desc": p.DESCRIPCION_PRODUCTO, 
                 "id_cat": p.ID_CATEGORIA, "id_uni": p.ID_UNIDAD, 
                 "stock_min": p.STOCK_MINIMO, "costo": p.COSTO_PROMEDIO, "estado": p.ESTADO} for p in productos]
    except Exception:
        return []
    finally:
        session.close()

def crear_producto(codigo, desc, id_categoria, id_unidad, stock_min, costo):
    session = get_session()
    if not session: return False
    try:
        nuevo = Producto(CODIGO_UNICO=codigo, DESCRIPCION_PRODUCTO=desc, ID_CATEGORIA=id_categoria, ID_UNIDAD=id_unidad, STOCK_MINIMO=stock_min, COSTO_PROMEDIO=costo, ESTADO=True)
        session.add(nuevo)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False
    finally:
        session.close()

def actualizar_producto(id_prod, codigo, desc, id_categoria, id_unidad, stock_min, costo):
    session = get_session()
    if not session: return False
    try:
        p = session.query(Producto).get(id_prod)
        if p:
            p.CODIGO_UNICO = codigo
            p.DESCRIPCION_PRODUCTO = desc
            p.ID_CATEGORIA = id_categoria
            p.ID_UNIDAD = id_unidad
            p.STOCK_MINIMO = stock_min
            p.COSTO_PROMEDIO = costo
            session.commit()
            return True
        return False
    except Exception:
        session.rollback()
        return False
    finally:
        session.close()

def toggle_estado_producto(id_producto):
    session = get_session()
    if not session: return
    try:
        p = session.query(Producto).get(id_producto)
        if p:
            p.ESTADO = not p.ESTADO
            session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()
