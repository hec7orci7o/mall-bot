CREATE TABLE productos (
    nombre    varchar(45) NOT NULL,
    categoria varchar(25) DEFAULT NULL,
    PRIMARY KEY (nombre)
)

CREATE TABLE imagenes (
    id     int(11)      NOT NULL AUTO_INCREMENT,
    nombre varchar(45)  NOT NULL,
    url    varchar(300) DEFAULT NULL,
    PRIMARY KEY (id,nombre),
    KEY id_producto_img_fk_idx (nombre),
    CONSTRAINT fk_img_prod FOREIGN KEY (nombre) REFERENCES productos (nombre)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
