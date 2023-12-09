INSERT INTO usuario (id_usuario, contrasena, rol, contacto, direccion, id_sucursal, nombres, apellidos, coordenadas, created, lastUpdate, correo_electronico, num_telefono, url_logo, gerente, url_link_web)
VALUES
(101, 'contrasenaA', 'Distribuidor', 'Contacto A', 'Dirección A', 1, 'NombreA', 'ApellidoA', '40.7128,-74.0060', '2023-01-01 08:30:00', '2023-02-15 14:30:00', 'usuarioA@example.com', '123-456-7890', 'url_logo_usuarioA.png', 'Gerente A', 'webA.com'),
(102, 'contrasenaB', 'Distribuidor', 'Contacto B', 'Dirección B', 2, 'NombreB', 'ApellidoB', '34.0522,-118.2437', '2023-01-02 09:00:00', '2023-02-20 12:45:00', 'usuarioB@example.com', '987-654-3210', 'url_logo_usuarioB.png', 'Gerente B', 'webB.com'),
(103, 'contrasenaC', 'Cliente', 'Contacto C', 'Dirección C', 3, 'NombreC', 'ApellidoC', '41.8781,-87.6298', '2023-02-10 10:15:00', '2023-03-01 17:15:00', 'usuarioC@example.com', '555-123-4567', 'url_logo_usuarioC.png', 'Gerente C', 'webC.com'),
(104, 'contrasenaD', 'Cliente', 'Contacto D', 'Dirección D', 4, 'NombreD', 'ApellidoD', '51.5074,-0.1278', '2023-02-15 11:45:00', '2023-03-05 14:00:00', 'usuarioD@example.com', '111-222-3333', 'url_logo_usuarioD.png', 'Gerente D', 'webD.com'),
(105, 'contrasenaE', 'Cliente', 'Contacto E', 'Dirección E', 5, 'NombreE', 'ApellidoE', '37.7749,-122.4194', '2023-03-01 12:00:00', '2023-03-10 16:45:00', 'usuarioE@example.com', '333-444-5555', 'url_logo_usuarioE.png', 'Gerente E', 'webE.com'),
(106, 'contrasenaF', 'Cliente', 'Contacto F', 'Dirección F', NULL, 'NombreF', 'ApellidoF', '45.4215,-75.6993', '2023-03-10 14:30:00', '2023-03-12 10:00:00', 'usuarioF@example.com', '777-888-9999', 'url_logo_usuarioF.png', NULL, NULL);
INSERT INTO sucursal (id_sucursal, id_usuario, direccion, telefono, nombre, gerente, contacto, correo_electronico, created, lastUpdate, url_logo, coordenadas, horarios_de_atencion)
VALUES
(1, 101, 'Calle Principal 123', '123-456-7890', 'Sucursal A', 'Gerente A', 'Contacto A', 'sucursalA@example.com', '2023-01-01 10:00:00', '2023-02-15 14:30:00', 'url_logo_sucursalA.png', '40.7128,-74.0060', 'Lunes a Viernes 9 AM - 6 PM'),
(2, 102, 'Avenida Central 456', '987-654-3210', 'Sucursal B', 'Gerente B', 'Contacto B', 'sucursalB@example.com', '2023-01-02 09:30:00', '2023-02-20 12:45:00', 'url_logo_sucursalB.png', '34.0522,-118.2437', 'Lunes a Sábado 10 AM - 7 PM'),
(3, 103, 'Plaza Principal 789', '555-123-4567', 'Sucursal C', 'Gerente C', 'Contacto C', 'sucursalC@example.com', '2023-02-10 08:45:00', '2023-03-01 17:15:00', 'url_logo_sucursalC.png', '41.8781,-87.6298', 'Lunes a Domingo 8 AM - 8 PM'),
(4, 104, 'Carrera 567', '111-222-3333', 'Sucursal D', 'Gerente D', 'Contacto D', 'sucursalD@example.com', '2023-02-15 11:20:00', '2023-03-05 14:00:00', 'url_logo_sucursalD.png', '51.5074,-0.1278', 'Martes a Sábado 11 AM - 6 PM'),
(5, 105, 'Avenida Principal 890', '333-444-5555', 'Sucursal E', 'Gerente E', 'Contacto E', 'sucursalE@example.com', '2023-03-01 09:00:00', '2023-03-10 16:45:00', 'url_logo_sucursalE.png', '37.7749,-122.4194', 'Miércoles a Domingo 9 AM - 5 PM');
INSERT INTO auto (id_auto, nombre, descripcion, disponibilidad, categoria_de_auto, marca, modelo, anio, kilometraje, precio, sucursal_id, especificaciones)
VALUES
(1, 'Toyota Corolla', 'Compacto y eficiente', true, 'Compacto', 'Toyota', 'Corolla', 2022, '50,000 km', 20000.00, 1, 'Sedán de alta eficiencia energética'),
(2, 'Honda CR-V', 'Espacioso y versátil', true, 'SUV', 'Honda', 'CR-V', 2021, '30,000 km', 25000.00, 2, 'SUV con características avanzadas de seguridad'),
(3, 'Ford Mustang', 'Deportivo y potente', true, 'Deportivo', 'Ford', 'Mustang', 2023, '10,000 km', 35000.00, 3, 'Muscle car con motor V8'),
(4, 'Chevrolet Spark', 'Compacto y ágil', true, 'Compacto', 'Chevrolet', 'Spark', 2022, '40,000 km', 15000.00, 4, 'Pequeño automóvil ideal para la ciudad'),
(5, 'Nissan Rogue', 'Seguro y confiable', true, 'SUV', 'Nissan', 'Rogue', 2021, '35,000 km', 28000.00, 5, 'SUV con características avanzadas de seguridad');
INSERT INTO distribuidor_sucursal (id_relacion, id_usuario, id_sucursal)
VALUES
(1, 101, 1),
(2, 102, 2),
(3, 102, 1),
(4, 101, 2);

INSERT INTO images_sucursal (id_images_sucursal, url_image, descripcion, id_sucursal)
VALUES
(1, 'url_imagen_sucursal1.jpg', 'Imagen de Sucursal A', 1),
(2, 'url_imagen_sucursal2.jpg', 'Imagen de Sucursal B', 2),
(3, 'url_imagen_sucursal3.jpg', 'Imagen de Sucursal C', 3),
(4, 'url_imagen_sucursal4.jpg', 'Imagen de Sucursal D', 4),
(5, 'url_imagen_sucursal5.jpg', 'Imagen de Sucursal E', 5);
INSERT INTO catalogo (id_catalogo, sucursal_id, auto_id, created, lastUpdate, lastInventoryUpdate, especificaciones, main_image, descripcion)
VALUES
(1, 1, 1, '2023-03-10 12:00:00', '2023-03-12 15:30:00', '2023-03-12 16:00:00', 'Catálogo de Sucursal A', 'url_imagen_catalogo1.jpg', 'Descripción del Catálogo de Sucursal A'),
(2, 2, 2, '2023-03-10 11:30:00', '2023-03-11 14:45:00', '2023-03-11 15:00:00', 'Catálogo de Sucursal B', 'url_imagen_catalogo2.jpg', 'Descripción del Catálogo de Sucursal B'),
(3, 3, 3, '2023-03-11 09:45:00', '2023-03-11 12:00:00', '2023-03-11 12:15:00', 'Catálogo de Sucursal C', 'url_imagen_catalogo3.jpg', 'Descripción del Catálogo de Sucursal C'),
(4, 4, 4, '2023-03-12 10:15:00', '2023-03-12 13:30:00', '2023-03-12 14:00:00', 'Catálogo de Sucursal D', 'url_imagen_catalogo4.jpg', 'Descripción del Catálogo de Sucursal D'),
(5, 5, 5, '2023-03-11 14:00:00', '2023-03-12 17:15:00', '2023-03-12 17:30:00', 'Catálogo de Sucursal E', 'url_imagen_catalogo5.jpg', 'Descripción del Catálogo de Sucursal E');
INSERT INTO images_catalogo (id_images_catalogo, url_image, descripcion, id_catalogo)
VALUES
(1, 'url_imagen_catalogo1_1.jpg', 'Imagen del Catálogo 1', 1),
(2, 'url_imagen_catalogo2_1.jpg', 'Imagen del Catálogo 2', 2),
(3, 'url_imagen_catalogo3_1.jpg', 'Imagen del Catálogo 3', 3),
(4, 'url_imagen_catalogo4_1.jpg', 'Imagen del Catálogo 4', 4),
(5, 'url_imagen_catalogo5_1.jpg', 'Imagen del Catálogo 5', 5);
