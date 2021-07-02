import json

input  = ''
output = ''

with open(input, "r") as file:
    data = json.load(file)

with open(output, "w") as file:
    for categoria in data['productos']:
        for producto in data['productos'][categoria]:
            file.write(f"INSERT INTO productos (nombre, categoria) VALUES ('{producto['name']}', '{categoria}');\n")
            for url in producto['imagenes']:
                file.write(f"INSERT INTO imagenes (nombre, url) VALUES ('{producto['name']}', '{url}');\n")
