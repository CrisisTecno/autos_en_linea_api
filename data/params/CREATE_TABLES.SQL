CREATE TABLE auto (
    id_auto INT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion VARCHAR(255),
    disponibilidad BOOLEAN,
    precio DECIMAL(10, 2),
    categoria_id INT,
    proveedor_id INT,
    sucursal_id INT,
    FOREIGN KEY (categoria_id) REFERENCES categoria_de_producto(id_categoria_de_producto),
    FOREIGN KEY (proveedor_id) REFERENCES proveedor(id_proveedor),
    FOREIGN KEY (sucursal_id) REFERENCES sucursal(id_sucursal)
);

CREATE TABLE transaccion_de_pago (
    id_orden_compra INT PRIMARY KEY,
    fecha_y_hora DATETIME,
    metodo_de_pago VARCHAR(50),
    monto DECIMAL(10, 2)
);

CREATE TABLE detalle_de_orden_de_compra (
    id_detalle_orden_compra INT PRIMARY KEY,
    id_orden_compra INT,
    id_auto INT,
    cantidad INT,
    precio_unitario DECIMAL(10, 2),
    FOREIGN KEY (id_orden_compra) REFERENCES orden_de_compra(id_orden_compra),
    FOREIGN KEY (id_auto) REFERENCES auto(id_auto)
);

CREATE TABLE categoria_de_producto (
    id_categoria_de_producto INT PRIMARY KEY,
    nombre VARCHAR(50),
    descripcion VARCHAR(255)
);


CREATE TABLE orden_de_compra (
    id_orden_compra INT PRIMARY KEY,
    proveedor_id INT,
    fecha_y_hora DATETIME,
    FOREIGN KEY (proveedor_id) REFERENCES proveedor(id_proveedor)
);

CREATE TABLE venta (
    id_venta INT PRIMARY KEY,
    auto_id INT,
    cantidad INT,
    precio_total DECIMAL(10, 2),
    fecha_y_hora DATETIME,
    id_orden_de_compra INT,
    FOREIGN KEY (auto_id) REFERENCES auto(id_auto),
    FOREIGN KEY (id_orden_de_compra) REFERENCES orden_de_compra(id_orden_compra)
);

CREATE TABLE resenas_de_producto (
    id_resena_de_producto INT PRIMARY KEY,
    auto_id INT,
    usuario_id INT,
    calificacion INT,
    comentario VARCHAR(255),
    fecha_y_hora DATETIME,
    FOREIGN KEY (auto_id) REFERENCES auto(id_auto),
    FOREIGN KEY (usuario_id) REFERENCES usuario(id_usuario)
);

CREATE TABLE consulta_auto (
    id_consulta_auto INT PRIMARY KEY,
    auto_id INT,
    usuario_id INT,
    fecha_y_hora DATETIME,
    FOREIGN KEY (auto_id) REFERENCES auto(id_auto),
    FOREIGN KEY (usuario_id) REFERENCES usuario(id_usuario)
);

CREATE TABLE proveedor (
    id_proveedor INT PRIMARY KEY,
    nombre VARCHAR(100),
    contacto VARCHAR(255),
    direccion VARCHAR(255),
    id_datos_personales INT,
    FOREIGN KEY (id_datos_personales) REFERENCES datos_personales(id_datos_personales)
);

CREATE TABLE catalogo (
    id_catalogo INT PRIMARY KEY,
    sucursal_id INT,
    auto_id INT,
    FOREIGN KEY (sucursal_id) REFERENCES sucursal(id_sucursal),
    FOREIGN KEY (auto_id) REFERENCES auto(id_auto)
);

CREATE TABLE notificacion (
    id_notificacion INT PRIMARY KEY,
    mensaje VARCHAR(255),
    destinatario_id INT,
    fecha_y_hora DATETIME,
    FOREIGN KEY (destinatario_id) REFERENCES usuario(id_usuario)
);

CREATE TABLE rol (
    id_rol INT PRIMARY KEY,
    rol_descripcion VARCHAR(50)
);

CREATE TABLE comentario (
    id_comentario INT PRIMARY KEY,
    contenido VARCHAR(255),
    auto_id INT,
    usuario_id INT,
    fecha_y_hora DATETIME,
    FOREIGN KEY (auto_id) REFERENCES auto(id_auto),
    FOREIGN KEY (usuario_id) REFERENCES usuario(id_usuario)
);

CREATE TABLE usuario (
    id_usuario INT PRIMARY KEY,
    contrasena VARCHAR(255),
    rol_id INT,
    id_sucursal INT,
    id_datos_personales INT,
    coordenadas VARCHAR(255),
    FOREIGN KEY (rol_id) REFERENCES rol(id_rol),
    FOREIGN KEY (id_sucursal) REFERENCES sucursal(id_sucursal),
    FOREIGN KEY (id_datos_personales) REFERENCES datos_personales(id_datos_personales)
);

CREATE TABLE datos_personales (
    id_datos_personales INT PRIMARY KEY,
    nombres VARCHAR(100),
    apellidos VARCHAR(100),
    fecha_nacimiento DATE,
    color_preferido VARCHAR(50)
);

CREATE TABLE inventario (
    id_inventario INT PRIMARY KEY,
    sucursal_id INT,
    auto_id INT,
    cantidad_disponible INT,
    estado_producto VARCHAR(50),
    FOREIGN KEY (sucursal_id) REFERENCES sucursal(id_sucursal),
    FOREIGN KEY (auto_id) REFERENCES auto(id_auto)
);
