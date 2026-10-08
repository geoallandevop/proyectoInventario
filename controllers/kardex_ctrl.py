from models.database import get_session
from models.entities import Producto, Bodega, ExistenciaBodega, TipoMovimiento, MovimientoKardex, DetalleKardex
from datetime import datetime, date
from sqlalchemy import func

def registrar_movimiento(usuario_id, tipo_movimiento_id, bodega_origen_id, bodega_destino_id, doc_referencia, detalles_productos, motivo_id=None, observaciones=""):
    """
    Lógica de negocio para transacciones. Valida y aplica matemáticas de inventario.
    detalles_productos: list de dicts [{'id_producto': 1, 'cantidad': 10, 'costo_unitario': 5.0}]
    """
    session = get_session()
    if not session:
        return False, "Base de datos no disponible."
        
    try:
        tipo = session.query(TipoMovimiento).get(tipo_movimiento_id)
        if not tipo:
            return False, "Tipo de movimiento inválido."
            
        efecto = tipo.EFECTO_STOCK
        nuevo_folio = f"MOV-{datetime.now().strftime('%Y%m%d%H%M%S')}" 
        
        # Cabecera
        movimiento = MovimientoKardex(
            FOLIO_COMPROBANTE=nuevo_folio,
            ID_TIPO_MOVIMIENTO=tipo_movimiento_id,
            ID_BODEGA_ORIGEN=bodega_origen_id,
            ID_BODEGA_DESTINO=bodega_destino_id,
            DOC_REFERENCIA=doc_referencia,
            ID_MOTIVO=motivo_id,
            ID_USUARIO_REGISTRO=usuario_id,
            FECHA_MOVIMIENTO=datetime.now(),
            ESTADO_APROBACION='APROBADO', # Regla de negocio: Ajustes quedan EN REVISION
            OBSERVACIONES=observaciones
        )
        session.add(movimiento)
        session.flush() # Para obtener ID
        
        # Detalles e Inventario (Matemática Crítica)
        for detalle in detalles_productos:
            id_prod = detalle['id_producto']
            cantidad = detalle['cantidad']
            costo_uni = detalle.get('costo_unitario', 0)
            
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0.")
            
            bodega_afectada = bodega_origen_id if efecto < 0 else (bodega_destino_id if bodega_destino_id else bodega_origen_id)
            existencia = session.query(ExistenciaBodega).filter_by(ID_PRODUCTO=id_prod, ID_BODEGA=bodega_afectada).first()
            
            saldo_anterior = existencia.STOCK_ACTUAL if existencia else 0
            saldo_nuevo = saldo_anterior + (cantidad * efecto)
            
            # REGLA: Bloqueo de Stock Negativo
            if saldo_nuevo < 0:
                raise ValueError(f"Stock insuficiente. Disponible: {saldo_anterior}")
            
            if existencia:
                existencia.STOCK_ACTUAL = saldo_nuevo
            else:
                nueva_existencia = ExistenciaBodega(ID_PRODUCTO=id_prod, ID_BODEGA=bodega_afectada, STOCK_ACTUAL=saldo_nuevo)
                session.add(nueva_existencia)
                
            nuevo_detalle = DetalleKardex(
                ID_MOVIMIENTO=movimiento.ID_MOVIMIENTO,
                ID_PRODUCTO=id_prod,
                CANTIDAD=cantidad,
                COSTO_UNITARIO=costo_uni,
                COSTO_TOTAL=cantidad * costo_uni,
                SALDO_ANTERIOR=saldo_anterior,
                SALDO_NUEVO=saldo_nuevo
            )
            session.add(nuevo_detalle)
            
        session.commit()
        return True, "Operación exitosa."
        
    except ValueError as ve:
        session.rollback()
        return False, str(ve)
    except Exception as e:
        session.rollback()
        return False, str(e)
    finally:
        session.close()

def obtener_inventario():
    """Consulta consolidada para la tabla de semáforos."""
    session = get_session()
    if not session:
        return []
    try:
        return session.query(
            Producto.CODIGO_UNICO,
            Producto.DESCRIPCION_PRODUCTO,
            Producto.STOCK_MINIMO,
            Bodega.NOMBRE_BODEGA,
            ExistenciaBodega.STOCK_ACTUAL
        ).join(ExistenciaBodega, Producto.ID_PRODUCTO == ExistenciaBodega.ID_PRODUCTO)\
         .join(Bodega, Bodega.ID_BODEGA == ExistenciaBodega.ID_BODEGA).all()
    except Exception:
        return []
    finally:
        session.close()

def obtener_bodegas():
    session = get_session()
    if not session: return []
    try:
        bodegas = session.query(Bodega).filter_by(ESTADO=True).all()
        return [{"id": b.ID_BODEGA, "nombre": b.NOMBRE_BODEGA} for b in bodegas]
    except Exception:
        return []
    finally:
        session.close()

def obtener_productos():
    session = get_session()
    if not session: return []
    try:
        productos = session.query(Producto).filter_by(ESTADO=True).all()
        return [{"id": p.ID_PRODUCTO, "codigo": p.CODIGO_UNICO, "nombre": p.DESCRIPCION_PRODUCTO} for p in productos]
    except Exception:
        return []
    finally:
        session.close()

def obtener_stock_producto(id_producto, id_bodega):
    session = get_session()
    if not session: return 0.0
    try:
        existencia = session.query(ExistenciaBodega).filter_by(ID_PRODUCTO=id_producto, ID_BODEGA=id_bodega).first()
        return existencia.STOCK_ACTUAL if existencia else 0.0
    except Exception:
        return 0.0
    finally:
        session.close()


def obtener_resumen_dashboard():
    """Return live counters for the dashboard; an empty dict enables UI fallbacks."""
    session = get_session()
    if not session:
        return {}
    try:
        productos = session.query(func.count(Producto.ID_PRODUCTO)).filter(Producto.ESTADO == True).scalar() or 0
        bodegas = session.query(func.count(Bodega.ID_BODEGA)).filter(Bodega.ESTADO == True).scalar() or 0
        alertas = session.query(func.count(ExistenciaBodega.ID_EXISTENCIA))\
            .join(Producto, Producto.ID_PRODUCTO == ExistenciaBodega.ID_PRODUCTO)\
            .filter(ExistenciaBodega.STOCK_ACTUAL <= Producto.STOCK_MINIMO).scalar() or 0
        inicio = datetime.combine(date.today(), datetime.min.time())
        movimientos = session.query(func.count(MovimientoKardex.ID_MOVIMIENTO))\
            .filter(MovimientoKardex.FECHA_MOVIMIENTO >= inicio).scalar() or 0
        return {"productos": productos, "bodegas": bodegas,
                "alertas": alertas, "movimientos": movimientos}
    except Exception:
        return {}
    finally:
        session.close()
