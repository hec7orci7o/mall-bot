CREATE TABLE productos (
    nombre varchar(45) NOT NULL,
    PRIMARY KEY (nombre)
);

CREATE TABLE imagenes (
    nombre varchar(45) NOT NULL,
    url varchar(300) DEFAULT NULL,
    PRIMARY KEY (nombre),
    KEY id_producto_img_fk_idx (nombre),
    CONSTRAINT fk_img_prod FOREIGN KEY (nombre) REFERENCES productos (nombre) 
    ON DELETE CASCADE
    ON UPDATE CASCADE
);