

CREATE TABLE distribuidor (
    id_distribuidor INT PRIMARY KEY IDENTITY(1,1),
    gerente VARCHAR(255),
    logo_image VARCHAR(255),
    coordenadas VARCHAR(255),
    direccion VARCHAR(255),
    nombre VARCHAR(255),
    created DATETIME2 ,
    lastUpdate DATETIME2 ,
    url_paginaWeb VARCHAR(255),
    telefono VARCHAR(100),
    email VARCHAR(255)
);

CREATE TABLE distribuidor_sucursal (
    id_relacion INT IDENTITY(1,1)  PRIMARY KEY,
    id_distribuidor INT,
    id_sucursal INT,
    FOREIGN KEY (id_distribuidor) REFERENCES distribuidor(id_distribuidor),
    FOREIGN KEY (id_sucursal) REFERENCES sucursal(id_sucursal)
);

CREATE TABLE usuario (
    id_usuario INT IDENTITY(1,1) PRIMARY KEY ,
    id_usuario_firebase VARCHAR(255),
    rol VARCHAR(100),
    nombres VARCHAR(100),
    apellidos VARCHAR(100),
    correo_electronico VARCHAR(255),
    num_telefono VARCHAR(100),
    url_logo VARCHAR(255),
    coordenadas VARCHAR(255),
    created DATETIME2 ,
    lastUpdate DATETIME2 ,
    id_sucursal INT,
    id_distribuidor INT,
    FOREIGN KEY (id_sucursal) REFERENCES sucursal(id_sucursal),
    FOREIGN KEY (id_distribuidor) REFERENCES distribuidor(id_distribuidor)
);

CREATE TABLE registro_actividades_usuario (
    id_registro INT PRIMARY KEY IDENTITY(1,1),
    id_usuario INT,
    accion VARCHAR(255),
    coordenadas VARCHAR(255),
    fecha_hora DATETIME2,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE articulo (
    id_articulo INT PRIMARY KEY IDENTITY(1,1),
    marca VARCHAR(255),
    modelo VARCHAR(255),
    categoria VARCHAR(255),
    ano VARCHAR(4), 
    precio FLOAT,
    kilometraje VARCHAR(255),
    created DATETIME2,
    lastUpdate DATETIME2,
    lastInventoryUpdate DATETIME2,
    [enable] BIT,
    mainImage VARCHAR(255),
    descripcion TEXT,
    color VARCHAR(255),
    espedition_date DATETIME2
);

CREATE TABLE favoritos (
    id_favorito INT PRIMARY KEY IDENTITY(1,1),
    id_usuario INT,
    id_articulo INT,
    [enable] BIT,
    fecha_agregado DATETIME2,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_articulo) REFERENCES articulo(id_articulo)
);

CREATE TABLE images_articulo (
    id_images_articulo INT IDENTITY(1,1)  PRIMARY KEY,
    url_image TEXT,
    descripcion TEXT,
    id_articulo INT,
    FOREIGN KEY (id_articulo ) REFERENCES articulo (id_articulo)
);

CREATE TABLE articulo_sucursal (
    id_relacion INT IDENTITY(1,1)  PRIMARY KEY,
    id_articulo INT,
    id_sucursal INT,
    FOREIGN KEY (id_articulo) REFERENCES articulo(id_articulo),
    FOREIGN KEY (id_sucursal) REFERENCES sucursal(id_sucursal)
);

CREATE TABLE images_sucursal (
    id_images_sucursal INT IDENTITY(1,1)  PRIMARY KEY,
    url_image TEXT,
    descripcion TEXT,
    id_sucursal INT,
    FOREIGN KEY (id_sucursal) REFERENCES sucursal(id_sucursal)
);

CREATE TABLE especificaciones (
    id_especificacion INT IDENTITY(1,1) PRIMARY KEY,
    tipo VARCHAR(255),
    id_articulo INT,
    FOREIGN KEY (id_articulo) REFERENCES articulo(id_articulo)
);

CREATE TABLE subespecificaciones (
    id_subespecificacion INT IDENTITY(1,1) PRIMARY KEY,
    clave VARCHAR(255),
    valor TEXT,
    id_especificacion INT,
    FOREIGN KEY (id_especificacion) REFERENCES especificaciones(id_especificacion)
);
CREATE TABLE especificaciones_adm (
    id_especificacion INT IDENTITY(1,1) PRIMARY KEY,
    tipo VARCHAR(255) UNIQUE
);
CREATE TABLE subespecificaciones_adm (
    id_subespecificacion INT IDENTITY(1,1) PRIMARY KEY,
    clave VARCHAR(255),
    valor TEXT,
    id_especificacion INT,
    FOREIGN KEY (id_especificacion) REFERENCES especificaciones_adm(id_especificacion)
);

CREATE TABLE marcas_adm(
    id_marca INT IDENTITY(1,1) PRIMARY KEY,
    marca VARCHAR(255),
    id_especificacion INT,
    FOREIGN KEY (id_especificacion) REFERENCES especificaciones_adm(id_especificacion)
);



CREATE TABLE marcas_distribuidor(
    id_marca INT IDENTITY(1,1) PRIMARY KEY,
    marca VARCHAR(255),
    id_distribuidor INT,
    FOREIGN KEY (id_distribuidor) REFERENCES distribuidor(id_distribuidor)
);



CREATE TABLE horarios_distribuidor (
    id_horario INT IDENTITY(1,1) PRIMARY KEY,
    [open]TIME,
    [close] TIME,
    day VARCHAR(10),
    id_distribuidor INT,
    FOREIGN KEY (id_distribuidor) REFERENCES distribuidor(id_distribuidor)
);

CREATE TABLE horarios_sucursal (
    id_horario INT IDENTITY(1,1) PRIMARY KEY,
    [open]TIME,
    [close] TIME,
    day VARCHAR(10),
    id_sucursal INT,
    FOREIGN KEY (id_sucursal) REFERENCES sucursal(id_sucursal)
);


CREATE TABLE sucursal (
    id_sucursal INT IDENTITY(1,1)  PRIMARY KEY,
    direccion VARCHAR(255),
    telefono VARCHAR(255),
    nombre VARCHAR(255),
    gerente VARCHAR(100),
    contacto VARCHAR(255),
    correo_electronico VARCHAR(255),
    created DATETIME2,
    lastUpdate DATETIME2,
    url_logo VARCHAR(255),
    coordenadas VARCHAR(255)
);


-- CREATE TABLE especificaciones_articulo (
--     id_especificacion VARCHAR(255) PRIMARY KEY,
--     tipo VARCHAR(255),
--     id_articulo INT,
--     nombre_especificacion VARCHAR(255),
--     valor_especificacion TEXT,
--     FOREIGN KEY (id_articulo) REFERENCES articulo(id_articulo)
-- );
-- CREATE TABLE auto (
--     id_auto INT IDENTITY(1,1)  PRIMARY KEY,
--     nombre VARCHAR(100),
--     descripcion VARCHAR(255),
--     disponibilidad BOOLEAN,
--     categoria_de_auto VARCHAR(255),
--     marca VARCHAR(150),
--     modelo VARCHAR(150),
--     anio INT,
--     kilometraje VARCHAR(100),
--     precio DECIMAL(10, 2),
--     especificaciones TEXT,
-- );
    -- favoritos VARCHAR(5),
    -- sucursal_id INT,
   -- ESPECIFICACIONES ES UN MAPA?
    -- FOREIGN KEY (sucursal_id) REFERENCES sucursal(id_sucursal)
-- POTENCIA : RPM Y HP CABALLOS DE FUERZA 
-- Y 
--  TRANSMISIION: MANUAL AUTOMATICO

-- quitar catalogo
-- CREATE TABLE catalogo (
--     id_catalogo INT IDENTITY(1,1)  PRIMARY KEY,
--     sucursal_id INT,
--     -- auto_id INT,
--     -- agregar:
--     -- nombre VARCHAR(255),
--     created DATETIME2 DEFAULT CURRENT_DATETIME2,
--     lastUpdate DATETIME2 DEFAULT CURRENT_DATETIME2 ON UPDATE CURRENT_DATETIME2,
--     lastInventoryUpdate DATETIME2 DEFAULT CURRENT_DATETIME2 ON UPDATE CURRENT_DATETIME2,
--     especificaciones TEXT,
--     main_image VARCHAR(255),
--     descripcion TEXT,
--     FOREIGN KEY (sucursal_id) REFERENCES sucursal(id_sucursal)
-- );



-- CREATE TABLE images_sucursal (
--     id_images_sucursal INT IDENTITY(1,1)  PRIMARY KEY,
--     url_image TEXT,
--     descripcion TEXT,
--     id_sucursal INT,
--     FOREIGN KEY (id_sucursal) REFERENCES sucursal(id_sucursal)
-- );

-- -- -- CREAR UN IMAGENES de AUTO, autos favoritos por usuario,
-- -- categoria por auto => que tecnicamente esta relacionado con las
-- --  especificaciones, tabla de registro de filtrado 

-- query para obtener los articulos favoritos y no favoritos
-- SELECT a.id_articulo,
--        a.nombre,
--        a.descripcion,
--        (CASE WHEN f.id_articulo IS NOT NULL THEN TRUE ELSE FALSE END) AS en_favoritos
-- FROM articulo a
-- LEFT JOIN favoritos f ON a.id_articulo = f.id_articulo AND f.id_usuario = 'ID_DEL_USUARIO'

-- CREATE TABLE articulo_distribuidor (
--     id_relacion INT IDENTITY(1,1)  PRIMARY KEY,
--     id_articulo INT,
--     id_sucursal INT,
--     FOREIGN KEY (id_articulo) REFERENCES articulo(id_articulo),
--     FOREIGN KEY (id_distribuidor) REFERENCES distribuidor(id_distribuidor)
-- );