# mall-bot V.3

mall bot is a bar-based discord bot that serves a variety of bizarre products

---

### Owner - Commands()
- [x] Add a product: `$insert 'name' 'category' 'url:opt'`
- [x] Edit a product name: `$update 'old:name' 'new:name'`
- [x] Edit a product category `$update 'name' 'new:category'`
- [x] Delete a product: `$delete 'id'`
- [x] Delete an image of a product: `$clear 'name'`
- [x] Show the id of the images of a product: `$select 'name'`
### Client - Commands()
- [x] Order a product
- [x] Show the menu
- [ ] Help commands

---

### Database config
    
* Tabla de categorias:

        CREATE TABLE categorias (
            nombre varchar(25) NOT NULL,
            PRIMARY KEY (nombre)
        );
    
* Tabla de productos:
    
        CREATE TABLE productos (
            nombre  varchar(45) NOT NULL,
            PRIMARY KEY (nombre)
        );
        
* Tabla de imagenes de un productos:

        CREATE TABLE imagenes (
            id     int(11)      NOT NULL AUTO_INCREMENT,
            nombre varchar(45)  NOT NULL,
            url    varchar(300) DEFAULT NULL,
            PRIMARY KEY (id,nombre),
            KEY id_producto_img_fk_idx (nombre),
            CONSTRAINT fk_img_prod FOREIGN KEY (nombre) REFERENCES productos (nombre) 
            ON DELETE CASCADE 
            ON UPDATE CASCADE
        );
        
---

### Deploy -> Local vs Heruku
#### Local requirements:
* requirements.txt: `pip install -r requirements.txt`
#### Heruku requirements:
* requirements.txt
* runtime.txt: `python-3.9.6`
* Procfile: `worker: python src/main.py`
* install the add-on: `ClearDB MySQL`


#### ENV VARIABLES - Both methods:

Al crear la bbdd con `ClearDB MySQL` se crea otra env var que aparece con el nombre de: `CLEARDB_DATABASE_URL`, esta variable de entorno es opcional pero de ella se extraeran algunas de las siguientes.
`CLEARDB_DATABASE_URL` = mysql://`USER`:`PASS`@`HOST`/`DATABASE`?reconnect=true
* DB-Host: `HOST`
* DB-Name: `DATABASE`
* DB-User: `USER`
* DB-Password: `PASS`
* Bot-Token: `TOKEN`
* Bot-Admin: `STAFF`
* Log-Channel: `CHANNEL`
