from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from .database import Base

class Rol(Base):
    __tablename__ = 'ROLES'
    ID_ROL = Column(Integer, primary_key=True, autoincrement=True)
    NOMBRE_ROL = Column(String(50), nullable=False)
    DESCRIPCION = Column(String(200))
    # Relaciones
    usuarios = relationship("Usuario", back_populates="rol")
    roles_permisos = relationship("RolPermiso", back_populates="rol")

class Usuario(Base):
    __tablename__ = 'USUARIOS'
    ID_USUARIO = Column(Integer, primary_key=True, autoincrement=True)
    NOMBRE_COMPLETO = Column(String(100), nullable=False)
    CORREO = Column(String(100), unique=True, nullable=False)
    PASSW_ORD = Column(String(255), nullable=False)
    ID_ROL = Column(Integer, ForeignKey('ROLES.ID_ROL'), nullable=False)
    ESTADO = Column(Boolean, nullable=False, default=True) # 1=ACTIVO, 0=INACTIVO
    # Relaciones
    rol = relationship("Rol", back_populates="usuarios")
    movimientos_registrados = relationship("MovimientoKardex", foreign_keys="[MovimientoKardex.ID_USUARIO_REGISTRO]", back_populates="usuario_registro")
    movimientos_autorizados = relationship("MovimientoKardex", foreign_keys="[MovimientoKardex.ID_USUARIO_AUTORIZA]", back_populates="usuario_autoriza")

class Permiso(Base):
    __tablename__ = 'PERMISOS'
    ID_PERMISO = Column(Integer, primary_key=True, autoincrement=True)
    CODIGO_PERMISO = Column(String(50), unique=True, nullable=False)
    NOMBRE_PERMISO = Column(String(100), nullable=False)
    # Relaciones
    roles_permisos = relationship("RolPermiso", back_populates="permiso")

class RolPermiso(Base):
    __tablename__ = 'ROLES_PERMISOS'
    ID_ROL = Column(Integer, ForeignKey('ROLES.ID_ROL'), primary_key=True)
    ID_PERMISO = Column(Integer, ForeignKey('PERMISOS.ID_PERMISO'), primary_key=True)
    # Relaciones
    rol = relationship("Rol", back_populates="roles_permisos")
    permiso = relationship("Permiso", back_populates="roles_permisos")

class Categoria(Base):
    __tablename__ = 'CATEGORIAS'
    ID_CATEGORIA = Column(Integer, primary_key=True, autoincrement=True)
    NOMBRE_CATEGORIA = Column(String(100), nullable=False)
    DESCRIPCION = Column(String(255))
    # Relaciones
    productos = relationship("Producto", back_populates="categoria")

class UnidadMedida(Base):
    __tablename__ = 'UNIDADES_MEDIDA'
    ID_UNIDAD = Column(Integer, primary_key=True, autoincrement=True)
    NOMBRE_UNIDAD = Column(String(50), nullable=False)
    SIMBOLO = Column(String(10), nullable=False)
    # Relaciones
    productos = relationship("Producto", back_populates="unidad")

class Producto(Base):
    __tablename__ = 'PRODUCTOS'
    ID_PRODUCTO = Column(Integer, primary_key=True, autoincrement=True)
    CODIGO_UNICO = Column(String(50), unique=True, nullable=False)
    DESCRIPCION_PRODUCTO = Column(String(200), nullable=False)
    ID_CATEGORIA = Column(Integer, ForeignKey('CATEGORIAS.ID_CATEGORIA'), nullable=False)
    ID_UNIDAD = Column(Integer, ForeignKey('UNIDADES_MEDIDA.ID_UNIDAD'), nullable=False)
    STOCK_MINIMO = Column(Float, nullable=False, default=0.0)
    COSTO_PROMEDIO = Column(Float, nullable=False, default=0.0)
    ESTADO = Column(Boolean, nullable=False, default=True)
    # Relaciones
    categoria = relationship("Categoria", back_populates="productos")
    unidad = relationship("UnidadMedida", back_populates="productos")
    existencias = relationship("ExistenciaBodega", back_populates="producto")
    detalles_kardex = relationship("DetalleKardex", back_populates="producto")

class Bodega(Base):
    __tablename__ = 'BODEGAS'
    ID_BODEGA = Column(Integer, primary_key=True, autoincrement=True)
    NOMBRE_BODEGA = Column(String(100), nullable=False)
    UBICACION = Column(String(200))
    ESTADO = Column(Boolean, nullable=False, default=True)
    # Relaciones
    existencias = relationship("ExistenciaBodega", back_populates="bodega")

class ExistenciaBodega(Base):
    __tablename__ = 'EXISTENCIAS_BODEGAS'
    ID_EXISTENCIA = Column(Integer, primary_key=True, autoincrement=True)
    ID_PRODUCTO = Column(Integer, ForeignKey('PRODUCTOS.ID_PRODUCTO'), nullable=False)
    ID_BODEGA = Column(Integer, ForeignKey('BODEGAS.ID_BODEGA'), nullable=False)
    STOCK_ACTUAL = Column(Float, nullable=False, default=0.0)
    # Relaciones
    producto = relationship("Producto", back_populates="existencias")
    bodega = relationship("Bodega", back_populates="existencias")

class TipoMovimiento(Base):
    __tablename__ = 'TIPOS_MOVIMIENTOS'
    ID_TIPO_MOVIMIENTO = Column(Integer, primary_key=True, autoincrement=True)
    NOMBRE_TIPO = Column(String(50), nullable=False) # ENTRADA, SALIDA, DEVOLUCION, AJUSTE
    EFECTO_STOCK = Column(Integer, nullable=False) # 1 para sumar, -1 para restar, 0 neutral
    # Relaciones
    movimientos = relationship("MovimientoKardex", back_populates="tipo_movimiento")

class MotivoExcepcion(Base):
    __tablename__ = 'MOTIVOS_EXCEPCIONES'
    ID_MOTIVO = Column(Integer, primary_key=True, autoincrement=True)
    DESCRIPCION_MOTIVO = Column(String(200), nullable=False)
    # Relaciones
    movimientos = relationship("MovimientoKardex", back_populates="motivo")

class MovimientoKardex(Base):
    __tablename__ = 'MOVIMIENTOS_KARDEX'
    ID_MOVIMIENTO = Column(Integer, primary_key=True, autoincrement=True)
    FOLIO_COMPROBANTE = Column(String(50), nullable=False)
    ID_TIPO_MOVIMIENTO = Column(Integer, ForeignKey('TIPOS_MOVIMIENTOS.ID_TIPO_MOVIMIENTO'), nullable=False)
    ID_BODEGA_ORIGEN = Column(Integer, ForeignKey('BODEGAS.ID_BODEGA'), nullable=True)
    ID_BODEGA_DESTINO = Column(Integer, ForeignKey('BODEGAS.ID_BODEGA'), nullable=True)
    DOC_REFERENCIA = Column(String(100))
    ID_MOTIVO = Column(Integer, ForeignKey('MOTIVOS_EXCEPCIONES.ID_MOTIVO'), nullable=True)
    ID_USUARIO_REGISTRO = Column(Integer, ForeignKey('USUARIOS.ID_USUARIO'), nullable=False)
    FECHA_MOVIMIENTO = Column(DateTime, nullable=False)
    ESTADO_APROBACION = Column(String(20), default='APROBADO') # APROBADO, RECHAZADO, EN REVISION
    ID_USUARIO_AUTORIZA = Column(Integer, ForeignKey('USUARIOS.ID_USUARIO'), nullable=True)
    FECHA_AUTORIZACION = Column(DateTime, nullable=True)
    OBSERVACIONES = Column(Text)
    
    # Relaciones
    tipo_movimiento = relationship("TipoMovimiento", back_populates="movimientos")
    bodega_origen = relationship("Bodega", foreign_keys=[ID_BODEGA_ORIGEN])
    bodega_destino = relationship("Bodega", foreign_keys=[ID_BODEGA_DESTINO])
    motivo = relationship("MotivoExcepcion", back_populates="movimientos")
    usuario_registro = relationship("Usuario", foreign_keys=[ID_USUARIO_REGISTRO], back_populates="movimientos_registrados")
    usuario_autoriza = relationship("Usuario", foreign_keys=[ID_USUARIO_AUTORIZA], back_populates="movimientos_autorizados")
    detalles = relationship("DetalleKardex", back_populates="movimiento")

class DetalleKardex(Base):
    __tablename__ = 'DETALLE_KARDEX'
    ID_DETALLE = Column(Integer, primary_key=True, autoincrement=True)
    ID_MOVIMIENTO = Column(Integer, ForeignKey('MOVIMIENTOS_KARDEX.ID_MOVIMIENTO'), nullable=False)
    ID_PRODUCTO = Column(Integer, ForeignKey('PRODUCTOS.ID_PRODUCTO'), nullable=False)
    CANTIDAD = Column(Float, nullable=False)
    COSTO_UNITARIO = Column(Float, nullable=False)
    COSTO_TOTAL = Column(Float, nullable=False)
    SALDO_ANTERIOR = Column(Float, nullable=False)
    SALDO_NUEVO = Column(Float, nullable=False)
    # Relaciones
    movimiento = relationship("MovimientoKardex", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_kardex")
