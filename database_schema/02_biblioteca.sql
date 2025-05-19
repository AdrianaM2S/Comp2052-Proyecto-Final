DROP DATABASE IF EXISTS gestor_biblioteca;
CREATE DATABASE gestor_biblioteca CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE gestor_biblioteca;

CREATE TABLE role (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(64) UNIQUE
);

CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) UNIQUE,
    email VARCHAR(120) UNIQUE,
    password_hash VARCHAR(256),
    role_id INT,
    FOREIGN KEY (role_id) REFERENCES role(id)
);

CREATE TABLE libro (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150),
    autor VARCHAR(100),
    isbn VARCHAR(20),
    categoria VARCHAR(50),
    estado ENUM('Disponible', 'Prestado'),
    anio_publicacion INT
);

ALTER TABLE libro 
ADD COLUMN bibliotecario_id INT,
ADD CONSTRAINT fk_bibliotecario FOREIGN KEY (bibliotecario_id) REFERENCES user(id) ON DELETE CASCADE;

INSERT INTO role (name) VALUES ('Admin'), ('Bibliotecario'), ('Lector');