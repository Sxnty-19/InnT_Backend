-- ========================================================
-- INNTECH - BASE DE DATOS (PostgreSQL)
-- Versión: COM30_2026-1 - Corte N°2
-- ========================================================

-- 1. Tabla: rol
CREATE TABLE rol (
    id_rol SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    estado BOOLEAN DEFAULT TRUE,
    date_created TIMESTAMP,
    date_updated TIMESTAMP
);

-- 2. Tabla: usuario
CREATE TABLE usuario (
    id_usuario SERIAL PRIMARY KEY,
    id_rol INT NOT NULL,
    primer_nombre VARCHAR(50) NOT NULL,
    segundo_nombre VARCHAR(50),
    primer_apellido VARCHAR(50) NOT NULL,
    segundo_apellido VARCHAR(50) NOT NULL,
    telefono VARCHAR(20) UNIQUE,
    correo VARCHAR(100) UNIQUE,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    estado BOOLEAN DEFAULT TRUE,
    date_created TIMESTAMP,
    date_updated TIMESTAMP,
    FOREIGN KEY (id_rol) REFERENCES rol(id_rol)
);

-- 3. Tabla: modulo
CREATE TABLE modulo (
    id_modulo SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    ruta VARCHAR(255) UNIQUE,
    descripcion TEXT,
    estado BOOLEAN DEFAULT TRUE,
    date_created TIMESTAMP,
    date_updated TIMESTAMP
);

-- 4. Tabla: modulo_rol
CREATE TABLE modulo_rol (
    id_mxr SERIAL PRIMARY KEY,
    id_modulo INT NOT NULL,
    id_rol INT NOT NULL,
    estado BOOLEAN DEFAULT TRUE,
    date_created TIMESTAMP,
    date_updated TIMESTAMP,
    FOREIGN KEY (id_modulo) REFERENCES modulo(id_modulo),
    FOREIGN KEY (id_rol) REFERENCES rol(id_rol)
);

-- 5. Tabla: tipo_documento
CREATE TABLE tipo_documento (
    id_tdocumento SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    estado BOOLEAN DEFAULT TRUE,
    date_created TIMESTAMP,
    date_updated TIMESTAMP
);

-- 6. Tabla: documento
CREATE TABLE documento (
    id_documento SERIAL PRIMARY KEY,
    id_tdocumento INT NOT NULL,
    id_usuario INT NOT NULL,
    numero_documento VARCHAR(50) UNIQUE NOT NULL,
    lugar_expedicion VARCHAR(150) NOT NULL,
    url_imagen TEXT,
    documento_validado BOOLEAN DEFAULT FALSE,
    estado BOOLEAN DEFAULT TRUE,
    date_created TIMESTAMP,
    date_updated TIMESTAMP,
    FOREIGN KEY (id_tdocumento) REFERENCES tipo_documento(id_tdocumento),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

-- 7. Tabla: tipo_habitacion
CREATE TABLE tipo_habitacion (
    id_thabitacion SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,
    capacidad_max INT NOT NULL,
    precio_x_dia NUMERIC(10,2) NOT NULL,
    estado BOOLEAN DEFAULT TRUE,
    date_created TIMESTAMP,
    date_updated TIMESTAMP
);

-- 8. Tabla: habitacion
CREATE TABLE habitacion (
    id_habitacion SERIAL PRIMARY KEY,
    id_thabitacion INT NOT NULL,
    numero VARCHAR(10) UNIQUE NOT NULL,
    limpieza BOOLEAN DEFAULT TRUE,
    estado BOOLEAN DEFAULT TRUE,
    date_created TIMESTAMP,
    date_updated TIMESTAMP,
    FOREIGN KEY (id_thabitacion) REFERENCES tipo_habitacion(id_thabitacion)
);

-- 9. Tabla: reserva
CREATE TABLE reserva (
    id_reserva SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL,
    date_start TIMESTAMP NOT NULL,
    date_end TIMESTAMP NOT NULL,
    tiene_ninos BOOLEAN DEFAULT FALSE,
    tiene_mascotas BOOLEAN DEFAULT FALSE,
    total_cop NUMERIC(10,2) DEFAULT 0,
    capacidad_total INT,
    estado BOOLEAN DEFAULT TRUE,
    date_created TIMESTAMP,
    date_updated TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

-- 10. Tabla: reserva_habitacion
CREATE TABLE reserva_habitacion (
    id_rxh SERIAL PRIMARY KEY,
    id_reserva INT NOT NULL,
    id_habitacion INT NOT NULL,
    estado BOOLEAN DEFAULT TRUE,
    date_created TIMESTAMP,
    date_updated TIMESTAMP,
    FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva),
    FOREIGN KEY (id_habitacion) REFERENCES habitacion(id_habitacion)
);

-- 11. Tabla: usuario_habitacion
CREATE TABLE usuario_habitacion (
    id_uxh SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_habitacion INT NOT NULL,
    id_reserva INT NOT NULL,
    date_check_in TIMESTAMP,
    date_check_out TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE,
    date_created TIMESTAMP,
    date_updated TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_habitacion) REFERENCES habitacion(id_habitacion),
    FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva)
);

-- 12. Tabla: solicitud
CREATE TABLE solicitud (
    id_solicitud SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_habitacion INT NOT NULL,
    descripcion TEXT,
    estado BOOLEAN DEFAULT TRUE,
    date_created TIMESTAMP DEFAULT NOW(),
    date_updated TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_habitacion) REFERENCES habitacion(id_habitacion)
);
