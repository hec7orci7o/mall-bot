# mall-bot V.0

mall bot is a discord bot based on a restaurant mall, allowing the user to order food from different types of restaurants among other things

### Owner - Commands()
- [x] Add a product
- [x] Edit a product
- [x] Delete a product
- [x] Delete an image of a product
- [x] Show the images of a product
### Client - Commands()
- [x] Order a product
- [ ] Help commands

### Usage & Deploy
* #### Install requirements.txt
        
        pip install -r requirements.txt
        
* #### Database config
    
    Tabla de productos:
    
        CREATE TABLE productos (
            nombre  varchar(45) NOT NULL,
            PRIMARY KEY (nombre)
        );
        
    Tabla de imagenes de un productos:

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
* #### Deploy -> Heruku
    * Files needed:
        *    requirements.txt
        *    runtime.txt
        *    Procfile: `worker: python src/main.py`
        *    install the add-on: `ClearDB MySQL`
    * Config Vars:
        * Host: `HOST`*
        * User: `USER`*
        * Password: `PASS`*
        * Database: `DATABASE`*
        * Token: `TOKEN`*
        * Channel: `CHANNEL`*
        * database_default: `CLEARDB_DATABASE_URL`
