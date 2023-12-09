CREATE TABLE categoria_de_producto (
    id_categoria_de_producto INT PRIMARY KEY,
    nombre VARCHAR(50),
    descripcion VARCHAR(255)
);
CREATE TABLE rol (
    id_rol INT PRIMARY KEY,
    rol_descripcion VARCHAR(50)
);
CREATE TABLE sucursal (
    id_sucursal INT PRIMARY KEY,
    direccion VARCHAR(255),
    nombre VARCHAR(255),
    horarios_de_atencion VARCHAR(255),
    contacto VARCHAR(255),
    correo_electronico VARCHAR(255),
    coordenadas VARCHAR(255)
);

CREATE TABLE datos_personales (
    id_datos_personales INT PRIMARY KEY,
    nombres VARCHAR(100),
    apellidos VARCHAR(100),
    fecha_nacimiento DATE,
    color_preferido VARCHAR(50)
);
CREATE TABLE transaccion_de_pago (
    id_orden_compra INT PRIMARY KEY,
    fecha_y_hora DATETIME,
    metodo_de_pago VARCHAR(50),
    monto DECIMAL(10, 2)
);