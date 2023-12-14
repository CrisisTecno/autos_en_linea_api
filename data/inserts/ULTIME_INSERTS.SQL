INSERT INTO sucursal (direccion, telefono, nombre, gerente, contacto, correo_electronico, url_logo, coordenadas, horarios_de_atencion) VALUES
('123 Calle Principal, Ciudad A', '555-0101', 'Sucursal A', 'Gerente A', 'Contacto A', 'correoA@example.com', 'url_logo_a.jpg', '19.4326,-99.1332', '9am-5pm'),
('456 Calle Secundaria, Ciudad B', '555-0202', 'Sucursal B', 'Gerente B', 'Contacto B', 'correoB@example.com', 'url_logo_b.jpg', '34.0522,-118.2437', '10am-6pm'),
('789 Calle Tercera, Ciudad C', '555-0303', 'Sucursal C', 'Gerente C', 'Contacto C', 'correoC@example.com', 'url_logo_c.jpg', '51.5074,-0.1278', '8am-4pm'),
('101 Calle Cuarta, Ciudad D', '555-0404', 'Sucursal D', 'Gerente D', 'Contacto D', 'correoD@example.com', 'url_logo_d.jpg', '35.6895,139.6917', '11am-7pm'),
('202 Calle Quinta, Ciudad E', '555-0505', 'Sucursal E', 'Gerente E', 'Contacto E', 'correoE@example.com', 'url_logo_e.jpg', '55.7558,37.6173', '7am-3pm');
INSERT INTO distribuidor ( gerente, logo_image, coordenadas, direccion, nombre, url_paginaWeb, telefono, email, horarioAtencion) VALUES
('Gerente Dist A', 'logo_dist_a.jpg', '40.7128,-74.0060', 'Calle Distribuidor A, Ciudad F', 'Distribuidor A', 'paginaA.com', '555-1001', 'distA@example.com', '9am-5pm'),
('Gerente Dist B', 'logo_dist_b.jpg', '48.8566,2.3522', 'Calle Distribuidor B, Ciudad G', 'Distribuidor B', 'paginaB.com', '555-2002', 'distB@example.com', '10am-6pm'),
('Gerente Dist C', 'logo_dist_c.jpg', '41.8781,-87.6298', 'Calle Distribuidor C, Ciudad H', 'Distribuidor C', 'paginaC.com', '555-3003', 'distC@example.com', '8am-4pm'),
('Gerente Dist D', 'logo_dist_d.jpg', '52.5200,13.4050', 'Calle Distribuidor D, Ciudad I', 'Distribuidor D', 'paginaD.com', '555-4004', 'distD@example.com', '11am-7pm'),
('Gerente Dist E', 'logo_dist_e.jpg', '-33.8688,151.2093', 'Calle Distribuidor E, Ciudad J', 'Distribuidor E', 'paginaE.com', '555-5005', 'distE@example.com', '7am-3pm');
INSERT INTO distribuidor_sucursal (id_distribuidor, id_sucursal) VALUES
(1, 1),
(2, 2),
(2, 3),
(4, 4),
(5, 5);
INSERT INTO usuario (id_usuario, rol, nombres, apellidos, correo_electronico, num_telefono, url_logo, coordenadas, id_sucursal, id_distribuidor) VALUES
('user1', 'Cliente', 'Nombre1', 'Apellido1', 'user1@example.com', '555-6001', 'url_logo_user1.jpg', '40.7128,-74.0060', 1, 1),
('user2', 'Cliente', 'Nombre2', 'Apellido2', 'user2@example.com', '555-6002', 'url_logo_user2.jpg', '48.8566,2.3522', 2, 1),
('user3', 'Cliente', 'Nombre3', 'Apellido3', 'user3@example.com', '555-6003', 'url_logo_user3.jpg', '41.8781,-87.6298', 1, 3),
('user4', 'Empleado', 'Nombre4', 'Apellido4', 'user4@example.com', '555-6004', 'url_logo_user4.jpg', '52.5200,13.4050', 4, 5),
('user5', 'Empleado', 'Nombre5', 'Apellido5', 'user5@example.com', '555-6005', 'url_logo_user5.jpg', '-33.8688,151.2093', 3, 5);

INSERT INTO registro_actividades_usuario (id_usuario, accion, coordenadas, fecha_hora) VALUES
('user1', 'Inicio de sesión', '40.7128,-74.0060', CURRENT_TIMESTAMP),
('user1', 'Consulta de artículos', '48.8566,2.3522', CURRENT_TIMESTAMP),
('user1', 'Actualización de perfil', '41.8781,-87.6298', CURRENT_TIMESTAMP),
('user4', 'Inicio de sesión', '52.5200,13.4050', CURRENT_TIMESTAMP),
('user5', 'Registro de compra', '-33.8688,151.2093', CURRENT_TIMESTAMP);

INSERT INTO articulo (marca, modelo, categoria, ano, precio, kilometraje, created, lastUpdate, lastInventoryUpdate, enable, mainImage, descripcion, color) VALUES
('Marca A', 'Modelo A', 'Categoria A', '2020', 20000.00, '10000', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE, 'imagen_a.jpg', 'Descripción A', 'Rojo'),
('Marca B', 'Modelo B', 'Categoria B', '2021', 25000.00, '5000', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE, 'imagen_b.jpg', 'Descripción B', 'Azul'),
('Marca C', 'Modelo C', 'Categoria C', '2019', 18000.00, '15000', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE, 'imagen_c.jpg', 'Descripción C', 'Verde'),
('Marca D', 'Modelo D', 'Categoria D', '2018', 15000.00, '20000', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE, 'imagen_d.jpg', 'Descripción D', 'Negro'),
('Marca E', 'Modelo E', 'Categoria E', '2022', 30000.00, '0', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE, 'imagen_e.jpg', 'Descripción E', 'Blanco');

INSERT INTO favoritos (id_usuario, id_articulo, fecha_agregado) VALUES
('user1', 1, CURRENT_TIMESTAMP),
('user1', 2, CURRENT_TIMESTAMP),
('user1', 3, CURRENT_TIMESTAMP),
('user3', 4, CURRENT_TIMESTAMP),
('user4', 5, CURRENT_TIMESTAMP);

INSERT INTO images_articulo (url_image, descripcion, id_articulo) VALUES
('img_articulo1_a.jpg', 'Imagen 1 del Artículo A', 1),
('img_articulo2_b.jpg', 'Imagen 2 del Artículo B', 2),
('img_articulo3_c.jpg', 'Imagen 3 del Artículo C', 1),
('img_articulo4_d.jpg', 'Imagen 4 del Artículo D', 4),
('img_articulo5_e.jpg', 'Imagen 5 del Artículo E', 2);

INSERT INTO especificaciones_articulo (id_especificacion, tipo, id_articulo, nombre_especificacion, valor_especificacion) VALUES
('espec1', 'motor', 1, 'Potencia', '100 HP'),
('espec2', 'motor', 2, 'Potencia', '150 HP'),
('espec3', 'chasis', 3, 'Material', 'Aluminio'),
('espec4', 'seguridad', 4, 'Airbags', '6'),
('espec5', 'rendimiento', 5, 'Eficiencia de Combustible', '20 km/l');


INSERT INTO articulo_sucursal (id_articulo, id_sucursal) VALUES
(1, 1),
(2, 1),
(3, 3),
(4, 4),
(5, 3);

INSERT INTO images_sucursal (url_image, descripcion, id_sucursal) VALUES
('img_sucursal1_a.jpg', 'Imagen Sucursal A', 1),
('img_sucursal2_b.jpg', 'Imagen Sucursal B', 1),
('img_sucursal3_c.jpg', 'Imagen Sucursal C', 3),
('img_sucursal4_d.jpg', 'Imagen Sucursal D', 3),
('img_sucursal5_e.jpg', 'Imagen Sucursal E', 5);
