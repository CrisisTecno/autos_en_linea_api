CREATE TABLE usuario (
    id_usuario INT PRIMARY KEY,
    contrasena VARCHAR(255),
    rol VARCHAR(100),
    contacto VARCHAR(255),
     direccion VARCHAR(255),
    id_sucursal INT,
    nombres VARCHAR(100),
    apellidos VARCHAR(100),
    coordenadas VARCHAR(255),
    created TIMESTAMP,
    lastUpdate TIMESTAMP,
    correo_electronico VARCHAR(255),
    num_telefono VARCHAR(100),
    url_logo VARCHAR(255),
    gerente VARCHAR(100),
    url_link_web VARCHAR(100),
);

-- la llave foranea a usuario es solo cuando el rol es distribuidor
CREATE TABLE sucursal (
    id_sucursal INT PRIMARY KEY,
    id_usuario INT FOREIGN KEY,
    direccion VARCHAR(255),
    telefono VARCHAR(255),
    nombre VARCHAR(255),
    gerente VARCHAR(100),
    contacto VARCHAR(255),
    correo_electronico VARCHAR(255),
    created TIMESTAMP,
    lastUpdate TIMESTAMP,
    url_logo VARCHAR(255),
    coordenadas VARCHAR(255),
    horarios_de_atencion VARCHAR(255),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
);
CREATE TABLE images_sucursal(
    id_images_sucursal INT PRIMARY KEY,
    url_image TEXT,
    descripcion TEXT,
    id_sucursal FOREIGN KEY,
    FOREIGN KEY (id_sucursal) REFERENCES sucursal(id_sucursal),

);



-- CREATE TABLE distribuidor_sucursal (
--     id_relacion INT PRIMARY KEY,
--     id_usuario INT,
--     id_sucursal INT,
--     FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
--     FOREIGN KEY (id_sucursal) REFERENCES sucursal(id_sucursal)
-- );

CREATE TABLE auto (
    id_auto INT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion VARCHAR(255),
    disponibilidad BOOLEAN,
    categoria_de_auto VARCHAR(255),
    marca VARCHAR(150),
    modelo VARCHAR(150),
    anio INT,
    kilometraje VARCHAR(100),
    precio DECIMAL(10, 2),

    sucursal_id INT FOREIGN KEY,
    especificaciones TEXT,
    FOREIGN KEY (sucursal_id) REFERENCES sucursal(id_sucursal)
);
-- CREATE TABLE auto_categoria(
--     id_categoria_auto INT PRIMARY KEY,
--     categoria VARCHAR(255),
--     descripcion TEXT,
--     id_auto INT FOREIGN KEY,
--     FOREIGN KEY (id_auto) REFERENCES auto(id_auto)
-- );
CREATE TABLE catalogo (
    id_catalogo INT PRIMARY KEY,
    sucursal_id INT FOREIGN KEY,
    auto_id INT,
    created TIMESTAMP,
    lastUpdate TIMESTAMP,
    lastInventoryUpdate TIMESTAMP,
    especificaciones TEXT,
    main_image VARCHAR(255),
    descripcion TEXT,
    FOREIGN KEY (sucursal_id) REFERENCES sucursal(id_sucursal),
);
CREATE TABLE images_catalogo(
    id_images_catalogo INT PRIMARY KEY,
    url_image TEXT,
    descripcion TEXT,
    id_catalogo FOREIGN KEY,
    FOREIGN KEY (id_catalogo) REFERENCES catalogo(id_catalogo),

);


CREATE TABLE notificacion (
    id_notificacion INT PRIMARY KEY,
    mensaje VARCHAR(255),
    usuario_id INT,
    fecha_y_hora TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id_usuario)
);



CREATE TABLE resenas_de_producto (
    id_resena_de_producto INT PRIMARY KEY,
    auto_id INT,
    usuario_id INT,
    calificacion INT,
    comentario VARCHAR(255),
    fecha_y_hora TIMESTAMP,
    FOREIGN KEY (auto_id) REFERENCES auto(id_auto),
    FOREIGN KEY (usuario_id) REFERENCES usuario(id_usuario)
);

CREATE TABLE consulta_auto (
    id_consulta_auto INT PRIMARY KEY,
    auto_id INT,
    usuario_id INT,
    fecha_y_hora TIMESTAMP,
    FOREIGN KEY (auto_id) REFERENCES auto(id_auto),
    FOREIGN KEY (usuario_id) REFERENCES usuario(id_usuario)
);


CREATE TABLE comentario (
    id_comentario INT PRIMARY KEY,
    contenido VARCHAR(255),
    auto_id INT,
    usuario_id INT,
    fecha_y_hora TIMESTAMP,
    FOREIGN KEY (auto_id) REFERENCES auto(id_auto),
    FOREIGN KEY (usuario_id) REFERENCES usuario(id_usuario)
);

CREATE TABLE catalogo_auto (
    id_catalogo_auto INT PRIMARY KEY,
    id_catalogo INT,
    id_auto INT,
    FOREIGN KEY (id_catalogo) REFERENCES catalogo(id_catalogo),
    FOREIGN KEY (id_auto) REFERENCES auto(id_auto)
);

CREATE TABLE inventario (
    id_inventario INT PRIMARY KEY,
    id_sucursal INT,
    id_auto INT,
    cantidad_disponible INT,
    estado_producto VARCHAR(50),
    FOREIGN KEY (id_sucursal) REFERENCES sucursal(id_sucursal),
    FOREIGN KEY (id_auto) REFERENCES auto(id_auto)
);
