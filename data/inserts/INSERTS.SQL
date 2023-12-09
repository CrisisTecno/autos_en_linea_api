
INSERT INTO categoria_de_producto (id_categoria_de_producto, nombre, descripcion) VALUES
(1, 'Sedan', 'Four-door passenger car'),
(2, 'SUV', 'Sport Utility Vehicle'),
(3, 'Truck', 'Pickup truck'),
(4, 'Coupe', 'Two-door sports car'),
(5, 'Hatchback', 'Compact car with a rear door'),
(6, 'Convertible', 'Car with a retractable roof'),
(7, 'Van', 'Multi-purpose vehicle'),
(8, 'Crossover', 'Combines features of a sedan and an SUV'),
(9, 'Electric', 'Powered by electric energy'),
(10, 'Luxury', 'High-end, premium features');

INSERT INTO rol (id_rol, rol_descripcion) VALUES
(1, 'admin'),
(2, 'gerente_sucursal'),
(3, 'distribuidor'),
(4, 'vendedor'),
(5, 'usuario');


INSERT INTO sucursal (id_sucursal, direccion, nombre, horarios_de_atencion, contacto, correo_electronico, coordenadas) VALUES
(1, '123 Main St', 'Main Branch', '9 AM - 6 PM', '123-456-7890', 'mainbranch@example.com', '40.7128° N, 74.0060° W'),
(2, '456 Oak St', 'Oak Branch', '10 AM - 7 PM', '987-654-3210', 'oakbranch@example.com', '34.0522° N, 118.2437° W'),
(3, '789 Pine St', 'Pine Branch', '8 AM - 5 PM', '555-123-4567', 'pinebranch@example.com', '41.8781° N, 87.6298° W'),
(4, '101 Maple St', 'Maple Branch', '11 AM - 8 PM', '111-222-3333', 'maplebranch@example.com', '37.7749° N, 122.4194° W'),
(5, '202 Elm St', 'Elm Branch', '7 AM - 4 PM', '444-555-6666', 'elmbranch@example.com', '32.7767° N, 96.7970° W'),
(6, '303 Cedar St', 'Cedar Branch', '9 AM - 6 PM', '777-888-9999', 'cedarbranch@example.com', '39.7392° N, 104.9903° W'),
(7, '404 Birch St', 'Birch Branch', '10 AM - 7 PM', '333-444-5555', 'birchbranch@example.com', '35.6895° N, 139.6917° E'),
(8, '505 Redwood St', 'Redwood Branch', '8 AM - 5 PM', '666-777-8888', 'redwoodbranch@example.com', '25.7617° N, 80.1918° W'),
(9, '606 Pineapple St', 'Pineapple Branch', '11 AM - 8 PM', '999-000-1111', 'pineapplebranch@example.com', '37.7749° S, 144.9631° E'),
(10, '707 Palm St', 'Palm Branch', '7 AM - 4 PM', '222-333-4444', 'palmbranch@example.com', '33.4484° S, 70.6515° W');


INSERT INTO datos_personales (id_datos_personales, nombres, apellidos, fecha_nacimiento, color_preferido) VALUES
(1, 'John', 'Doe', '1985-05-20', 'Blue'),
(2, 'Jane', 'Smith', '1990-12-15', 'Green'),
(3, 'Bob', 'Johnson', '1988-08-03', 'Red'),
(4, 'Alice', 'Williams', '1995-02-10', 'Yellow'),
(5, 'Charlie', 'Brown', '1982-09-25', 'Purple'),
(6, 'Eva', 'Davis', '1992-04-18', 'Orange'),
(7, 'Michael', 'Miller', '1980-11-30', 'Pink'),
(8, 'Sophia', 'Clark', '1998-07-07', 'Brown'),
(9, 'William', 'Wilson', '1987-03-12', 'Gray'),
(10, 'Olivia', 'Jones', '1993-06-08', 'White');
(11, 'Laura', 'Martínez', '1991-08-22', 'Green'),
(12, 'Carlos', 'García', '1983-04-17', 'Red'),
(13, 'Ana', 'Hernández', '1997-01-10', 'Blue'),
(14, 'Miguel', 'López', '1989-11-05', 'Purple'),
(15, 'Isabel', 'Ramírez', '1994-06-30', 'Orange'),
(16, 'Javier', 'Sánchez', '1986-03-25', 'Yellow'),
(17, 'Sofía', 'Díaz', '1990-09-12', 'Pink'),
(18, 'Alejandro', 'Pérez', '1980-12-03', 'Brown'),
(19, 'María', 'Torres', '1993-05-18', 'Gray'),
(20, 'Eduardo', 'Gómez', '1982-02-09', 'White');
(21, 'Luis', 'Fernández', '1995-09-14', 'Blue'),
(22, 'Ana María', 'Gutierrez', '1984-06-07', 'Green'),
(23, 'Pedro', 'Martínez', '1992-02-28', 'Red'),
(24, 'Sara', 'Gómez', '1989-11-18', 'Yellow'),
(25, 'Juan', 'Ramírez', '1998-07-03', 'Purple'),
(26, 'Carolina', 'Díaz', '1981-04-22', 'Orange'),
(27, 'Ricardo', 'Hernández', '1996-01-15', 'Pink'),
(28, 'Valentina', 'López', '1987-08-09', 'Brown'),
(29, 'Gabriel', 'Sánchez', '1993-05-05', 'Gray'),
(30, 'Mónica', 'Pérez', '1986-12-20', 'White');



INSERT INTO proveedor (id_proveedor, nombre, contacto, direccion, id_datos_personales) VALUES
(1, 'Proveedor A', 'Contacto A', 'Dirección A',11), -- Referencia a John Doe
(2, 'Proveedor B', 'Contacto B', 'Dirección B',12 ), -- Referencia a Laura Martínez
(3, 'Proveedor C', 'Contacto C', 'Dirección C', 13), -- Referencia a Luis Fernández
(4, 'Proveedor D', 'Contacto D', 'Dirección D',14),  -- Referencia a Eva Davis
(5, 'Proveedor E', 'Contacto E', 'Dirección E', 15); -- Referencia a Javier Sánchez



INSERT INTO distribuidor (id_distribuidor, nombre, contacto, direccion, id_datos_personales, coordenadas) VALUES
(1, 'Distribuidor A', 'Contacto A', 'Dirección A',16, 'Coordenadas A'), -- Referencia a Jane Smith
(2, 'Distribuidor B', 'Contacto B', 'Dirección B', 17, 'Coordenadas B'), -- Referencia a Carlos García
(3, 'Distribuidor C', 'Contacto C', 'Dirección C', 18, 'Coordenadas C'), -- Referencia a Ana María Gutiérrez
(4, 'Distribuidor D', 'Contacto D', 'Dirección D',19, 'Coordenadas D'),  -- Referencia a Michael Miller
(5, 'Distribuidor E', 'Contacto E', 'Dirección E', 20, 'Coordenadas E'); -- Referencia a Sofía Díaz


INSERT INTO usuario (id_usuario, contrasena, rol_id, id_sucursal, id_datos_personales, coordenadas) VALUES
(1, 'contrasena1', 4, 1, 1, 'Coordenadas Usuario 1'),  -- Rol: Vendedor, Sucursal: Main Branch, Usuario: John Doe
(2, 'contrasena2', 5, 2, 2, 'Coordenadas Usuario 2'), -- Rol: Usuario, Sucursal: Oak Branch, Usuario: Jane Smith
(3, 'contrasena3', 4, 3, 3, 'Coordenadas Usuario 3'), -- Rol: Vendedor, Sucursal: Pine Branch, Usuario: Bob Johnson
(4, 'contrasena4', 2, 4, 4, 'Coordenadas Usuario 4'),  -- Rol: Gerente Sucursal, Sucursal: Maple Branch, Usuario: Alice Williams
(5, 'contrasena5', 3, 5, 5, 'Coordenadas Usuario 5'), -- Rol: Distribuidor, Sucursal: Elm Branch, Usuario: Charlie Brown
(6, 'contrasena6', 4, 1, 6, 'Coordenadas Usuario 6'),  -- Rol: Vendedor, Sucursal: Main Branch, Usuario: Eva Davis
(7, 'contrasena7', 5, 2, 7, 'Coordenadas Usuario 7'), -- Rol: Usuario, Sucursal: Oak Branch, Usuario: Michael Miller
(8, 'contrasena8', 2, 3, 8, 'Coordenadas Usuario 8'), -- Rol: Gerente Sucursal, Sucursal: Pine Branch, Usuario: Sophia Clark
(9, 'contrasena9', 3, 4, 9, 'Coordenadas Usuario 9'),  -- Rol: Distribuidor, Sucursal: Maple Branch, Usuario: William Wilson
(10, 'contrasena10', 5, 5, 10, 'Coordenadas Usuario 10');  -- Rol: Usuario, Sucursal: Elm Branch, Usuario: Olivia Jones
