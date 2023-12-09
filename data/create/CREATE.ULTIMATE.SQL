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
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    lastUpdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    correo_electronico VARCHAR(255),
    num_telefono VARCHAR(100),
    url_logo VARCHAR(255),
    gerente VARCHAR(100),
    url_link_web VARCHAR(100)
);
CREATE TABLE sucursal (
    id_sucursal INT PRIMARY KEY,
    id_usuario INT,
    direccion VARCHAR(255),
    telefono VARCHAR(255),
    nombre VARCHAR(255),
    gerente VARCHAR(100),
    contacto VARCHAR(255),
    correo_electronico VARCHAR(255),
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    lastUpdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    url_logo VARCHAR(255),
    coordenadas VARCHAR(255),
    horarios_de_atencion VARCHAR(255),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE distribuidor_sucursal (
    id_relacion INT PRIMARY KEY,
    id_usuario INT,
    id_sucursal INT,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_sucursal) REFERENCES sucursal(id_sucursal)
);

CREATE TABLE images_sucursal (
    id_images_sucursal INT PRIMARY KEY,
    url_image TEXT,
    descripcion TEXT,
    id_sucursal INT,
    FOREIGN KEY (id_sucursal) REFERENCES sucursal(id_sucursal)
);

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
    sucursal_id INT,
    especificaciones TEXT,
    FOREIGN KEY (sucursal_id) REFERENCES sucursal(id_sucursal)
);

CREATE TABLE catalogo (
    id_catalogo INT PRIMARY KEY,
    sucursal_id INT,
    auto_id INT,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    lastUpdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    lastInventoryUpdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    especificaciones TEXT,
    main_image VARCHAR(255),
    descripcion TEXT,
    FOREIGN KEY (sucursal_id) REFERENCES sucursal(id_sucursal)
);

CREATE TABLE images_catalogo (
    id_images_catalogo INT PRIMARY KEY,
    url_image TEXT,
    descripcion TEXT,
    id_catalogo INT,
    FOREIGN KEY (id_catalogo) REFERENCES catalogo(id_catalogo)
);
