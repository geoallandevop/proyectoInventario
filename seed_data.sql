USE SISTEMA_KARDEX;

-- 1. TIPOS_MOVIMIENTOS
INSERT INTO TIPOS_MOVIMIENTOS (NOMBRE_TIPO, EFECTO_STOCK) VALUES 
('ENTRADA', 1),
('SALIDA', -1),
('DEVOLUCION', 1),
('AJUSTE_POSITIVO', 1),
('AJUSTE_NEGATIVO', -1);

-- 2. MOTIVOS_EXCEPCIONES
INSERT INTO MOTIVOS_EXCEPCIONES (DESCRIPCION_MOTIVO) VALUES 
('Producto Dañado'),
('Diferencia en Conteo Físico'),
('Devolución de Cliente'),
('Vencimiento');

-- 3. BODEGAS
INSERT INTO BODEGAS (NOMBRE_BODEGA, UBICACION, ESTADO) VALUES 
('Bodega Central', 'Edificio Principal - Planta Baja', 1),
('Bodega Sucursal Norte', 'Zona 4', 1);

-- 4. CATEGORIAS
INSERT INTO CATEGORIAS (NOMBRE_CATEGORIA, DESCRIPCION) VALUES 
('Electrónica', 'Equipos electrónicos y de cómputo'),
('Mobiliario', 'Sillas, escritorios y muebles de oficina'),
('Papelería', 'Insumos de oficina generales');

-- 5. UNIDADES_MEDIDA
INSERT INTO UNIDADES_MEDIDA (NOMBRE_UNIDAD, SIMBOLO) VALUES 
('Unidad', 'Un'),
('Caja (12 Unidades)', 'Cj'),
('Paquete', 'Pq');

-- 6. PRODUCTOS
INSERT INTO PRODUCTOS (CODIGO_UNICO, DESCRIPCION_PRODUCTO, ID_CATEGORIA, ID_UNIDAD, STOCK_MINIMO, COSTO_PROMEDIO, ESTADO) VALUES 
('ELEC-001', 'Laptop Dell Latitude 3420', 1, 1, 5, 5500.00, 1),
('ELEC-002', 'Monitor LG 24 Pulgadas', 1, 1, 10, 1200.00, 1),
('MOB-001', 'Silla Ergonómica Ejecutiva', 2, 1, 4, 850.00, 1),
('PAP-001', 'Resma de Papel Tamaño Carta', 3, 2, 20, 35.00, 1);

-- 7. EXISTENCIAS_BODEGAS (Para que el semáforo y la tabla tengan datos vivos)
INSERT INTO EXISTENCIAS_BODEGAS (ID_PRODUCTO, ID_BODEGA, STOCK_ACTUAL) VALUES 
(1, 1, 15), -- Óptimo (Verde)
(2, 1, 8),  -- Bajo stock, menor al mínimo de 10 (Amarillo)
(3, 1, 0),  -- Agotado (Rojo)
(4, 2, 50); -- Óptimo en otra bodega (Verde)

-- 8. PERMISOS
INSERT INTO PERMISOS (CODIGO_PERMISO, NOMBRE_PERMISO) VALUES
('INV_CONSULTA', 'Consultar Inventario'),
('INV_REGISTRO', 'Registrar Movimientos'),
('ADM_USUARIOS', 'Gestionar Usuarios'),
('ADM_CATALOGO', 'Gestionar Catálogo'),
('ADM_AUTORIZA', 'Autorizar Ajustes');

-- 9. ROLES_PERMISOS (Asignando permisos básicos según el diagrama)
-- Administrador (ID 1): Todo
INSERT INTO ROLES_PERMISOS (ID_ROL, ID_PERMISO) VALUES (1,1), (1,2), (1,3), (1,4), (1,5);
-- Encargado de Bodega (ID 2): Consulta y Registro
INSERT INTO ROLES_PERMISOS (ID_ROL, ID_PERMISO) VALUES (2,1), (2,2);
-- Consulta/supervision (ID 3): Solo Consulta
INSERT INTO ROLES_PERMISOS (ID_ROL, ID_PERMISO) VALUES (3,1);
