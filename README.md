<h1>
  <img src="https://www.clcert.cl/img/clcert_oscuro.svg" style="width: 150px; padding-right: 20px"/>
  <a href="https://diputado.labs.clcert.cl">#DiputadxDelDia</a>
</h1>

La aplicación **#DiputadxDelDia** elige al azar un(a) Diputado(a) del Congreso Nacional de Chile utilizando el valor aleatorio generado por el [Faro de Aleatoriedad de la Universidad de Chile](https://random.uchile.cl) a las 00:00 horas (Chile Continental GMT -04:00 durante hora de invierno) de cada día (el Faro utiliza huso horario GMT). A dicha hora se revela la siguiente información del congresista elegido:
* Edad.
* Profesión (si aplica).
* Circunscripción y Región que representa.
* Partido que milita.
* Porcentaje de Asistencia (considerando inasistencias justificadas e injustificadas).
* Distribución de Asignaciones (gastos operativos y en personal de apoyo)
* Votaciones en los últimos 10 boletines publicados.

Toda la información anterior se obtiene a partir de los datos entregados por la página oficial de la Cámara de Diputados [www.camara.cl](https://www.camara.cl).

## Comprobar la Elección del #DiputadxDelDia

Dentro del presente repositorio se dispone de un script de verificación, el cual recrea el proceso que Random UChile lleva a cabo todos los días a las 00:00 horas (Chile Continental) para elegir al (a la) #DiputadxDelDia.

### Requisitos para Verificación

* Python 3.0+
* Instalar requerimientos: `$ pip3 install -r backend/requirements.txt`

### Ejecutar Script de Verificación

```
$ python updater.py --verify [opciones] [valores]

Opciones:
-d [date]   Establece la fecha de generación del valor aleatorio a utilizar (formato DD-MM-AAAA).
-t [time]   Establece la hora de generación del valor aleatorio a utilizar (formato HH:MM).
-e [epoch]  Establece la fecha y hora de generación del valor aleatorio a utilizar en formato epoch en huso horario GMT (https://www.epochconverter.com/).
```

### Ejemplo de uso

Si quiere verificar el #DiputadxDelDia del **20 de Enero de 2023** puede ejecutar uno de los siguientes dos comandos:

```
$ python3 updater.py --verify -d 2023-01-30 -t 00:00
```
```
$ python3 updater.py --verify -e 1675047600000
```

## Levantar Proyecto Completo
La aplicación cuenta con un *backend* en Flask, el cual se encarga de servir los datos de lxs diputadxs. Al mismo tiempo, cuenta con un *frontend* en Next.js el cual consume los datos y los muestra de forma más amigable. 

### Usando Docker
**Requisitos**: Docker, docker compose.

Es posible levantar ambas partes del proyecto de forma sencilla utilizando `docker compose`:
```
$ docker compose up --build -d
```
La aplicación quedará corriendo en `localhost:3000`.

### Sin Docker
**Requisitos**: Python3.6+, npm.

#### Backend
Primero será necesario levantar el backend, para ello seguimos los siguientes pasos:
```bash
# Cambio de directorio
$ cd backend

# Instalación de requisitos
$ pip3 install -r requirements.txt

# Obtener data del último diputado.
$ python3 updater.py

# Servir el Backend
$ python3 app.py
```
#### Frontend
Para levantar el frontend, habrá que usar *node package manager*:
```
# Cambio de directorio
$ cd frontend

# Instalación de paquetes
$ npm install

# Servir Frontend
$ npm run serve
```
