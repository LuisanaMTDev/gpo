> - [!NOTE] Feature
Guardar el archivo que suba el usuario en Redis, darle un ID unique 
y darle ese unique ID al usuario para que cada vez que haga una request mi backend pueda acceder al csv del usuario que hizo la
request.

Usar TTL (Time To Live) de redis para que nos datos sean semipermanentes (no se guarden para siempre).

## Feature
Para asignaturas 70/30, con dos valores únicos en la columna "Tipos", ordenar los filas por su tipo (Laboratorio, Teoria) en el DataFrame (backend),
separándolas por tipo en la interfaz, en el template (interfaz) agregarle una clase a todos los elementos de un mismo tipo y
al último elemento del tipo Laboratorio agregarle un estilo (css) para que actúe cómo separación para el usuario usando .class:last-of-type.

- [X] Ordenar las filas por tipos con pandas.
- [ ] Agregar las clases y el estilo separador.

## Current
- [ ] Terminar el renderizado de los datos en el archivo csv y las opciones de filtración.
- [ ] Agregar una flask session desde el endpoint /send-file que almacene como valor el redis key del archivo csv del usuario,
para poder ponerlo como header de mis request con htmx (en el atributo htmx hx-headears).

