-- ========================================================
-- INNTECH - SCRIPT DE INSERCIÓN DE DATOS
-- Versión: COM30_2026-1 - Corte N°2
-- ========================================================

INSERT INTO rol (
    nombre, 
    descripcion, 
    date_created,
    date_updated
) VALUES
('Administrador', 'Rol con todos los permisos del sistema.', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
('Limpiador', 'Rol encargado de gestionar la limpieza de las habitaciones.', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
('Cliente', 'Rol para los usuarios que realizan reservas y usan los servicios del hotel.', '2026-01-01 00:00:00', '2026-01-01 00:00:00');

INSERT INTO tipo_documento (
    nombre, 
    descripcion, 
    date_created,
    date_updated
) VALUES
('Cédula de Ciudadanía', 'Documento de identificación para ciudadanos colombianos mayores de 18 años.', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
('Tarjeta de Identidad', 'Documento de identificación para menores de edad entre 7 y 17 años.', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
('Registro Civil', 'Documento que acredita el nacimiento de una persona.', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
('Cédula de Extranjería', 'Documento de identificación para extranjeros residentes en Colombia.', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
('Pasaporte', 'Documento internacional de viaje emitido por el país de origen.', '2026-01-01 00:00:00', '2026-01-01 00:00:00');

INSERT INTO tipo_habitacion (
    nombre, 
    descripcion, 
    capacidad_max, 
    precio_x_dia, 
    date_created,
    date_updated
) VALUES
('Habitación Sencilla', NULL, 1, 40000.00, '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
('Habitación Doble', NULL, 2, 60000.00, '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
('Habitación Múltiple', NULL, 3, 80000.00, '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
('Habitación Quintuple', NULL, 5, 100000.00, '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
('Habitación Sextuple', NULL, 6, 120000.00, '2026-01-01 00:00:00', '2026-01-01 00:00:00');

INSERT INTO habitacion (
    id_thabitacion, 
    numero, 
    date_created,
    date_updated
) VALUES
-- Piso 2
(1, '201', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
(1, '202', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
(1, '203', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
(2, '204', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
(2, '205', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),

-- Piso 3
(1, '301', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
(1, '302', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
(2, '303', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
(2, '304', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
(2, '305', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),

-- Piso 4
(3, '401', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
(3, '402', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
(3, '403', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
(3, '404', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
(3, '405', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),

-- Piso 5
(4, '501', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
(4, '502', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
(4, '503', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
(5, '504', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
(5, '505', '2026-01-01 00:00:00', '2026-01-01 00:00:00');

INSERT INTO modulo (nombre, ruta, descripcion, date_created, date_updated)
VALUES 
('Reservar', '/c-reservar', '', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
('Historial (Reservas)', '/c-reservas-h', '', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
('Solicitudes', '/c-solicitar', '', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
('Informacion Turistica', '/c-informaciont', '', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
('Habitaciones', '/l-habitaciones', '', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
('G. Roles', '/a-roles', '', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
('G. Usuarios', '/a-usuarios', '', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
('G. Documentos', '/a-documentos', '', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
('G. Habitaciones', '/a-habitaciones', '', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
('G. Reservas', '/a-reservas', '', '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
('G. Solicitudes', '/a-solicitudes', '', '2026-01-01 00:00:00', '2026-01-01 00:00:00');

INSERT INTO modulo_rol (id_modulo, id_rol, date_created, date_updated)
VALUES 
(1, 3, '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
(2, 3, '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
(3, 3, '2026-01-01 00:00:00', '2026-01-01 00:00:00'),
(4, 3, '2026-01-01 00:00:00', '2026-01-01 00:00:00');
