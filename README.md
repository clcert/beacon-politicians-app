<h1 style="line-height: 50px; display: flex">
  <img src="https://www.clcert.cl//img/clcert_oscuro.svg" style="width: 150px; padding-right: 20px"/>
  <div>#DiputadxDelDia</div>
</h1>

La aplicación #DiputadxDelDia elige al azar un(a) Diputado(a) del Congreso Nacional de Chile utilizando el valor aleatorio generado por el Faro de Aleatoriedad de la Universidad de Chile (https://random.uchile.cl) a las 00:01 horas (Chile Continental GMT -04:00 durante hora de invierno) de cada día (el Faro utiliza huso horario GMT). A dicha hora se revela la siguiente información del congresista elegido:
* Fecha de Nacimiento.
* Profesión.
* Circunscripción y Región que representa.
* Partido que milita.
* Porcentaje de Asistencia (considerando inasistencias justificadas e injustificadas).
* Votaciones en los últimos 10 boletines publicados.
Toda la información anterior se obtiene a partir de los datos entregados por la página oficial de la Cámara de Diputados www.camara.cl.

## Comprobar Elección del #DiputadxDelDia

Dentro del actual repositorio se dispone de un script de verificación que recrea el proceso que el CLCERT lleva a cabo todos los días a las 00:01 horas (Chile Continental) para elegir al #DiputadxDelDia.

### Descarga última versión

Soon

### Requisitos

* Python 3.0+
* Instalar requerimientos: `$ pip install -r requirements.txt`

### Ejecutar Script

```
$ python updater.py [opciones] [valores]

Options:
-p          Imprime en consola diputado elegido.
-d [date]   Establece la fecha de generación del valor aleatorio a utilizar (formato AAAA-MM-DD).
-t [time]   Establece la hora de generación del valor aleatorio a utilizar (formato HH:MM).
-e [epoch]  Establece la fecha y hora de generación del valor aleatorio a utilizar en formato epoch en huso horario GMT (https://www.epochconverter.com/).
```

### Ejemplo de uso

Si quiere verificar el #DiputadxDelDia del **18 de Julio de 2018** puede ejecutar uno de los siguientes dos comandos:

```
$ python updater.py -p -d 2018-07-18 -t 00:01
```
```
$ python updater.py -p -e 1531886460
```
