# Práctica de clase: Mascotas2

## Descripción

Basados en el programa de manejo de mascotas en una veterinaria, del taller anterior ( [Mascotas1](../Mascotas1/README.md) ), extender la funcionalidad por medio de herencia múltiple.

1. Haga una clase Visualizador, que permita imprimir en pantalla el resumen del objeto (clase, nombre, etc.)
    * Haga un método llamado `resumen` que haga esta tarea.
2. Modifique la definición de las clases ya creadas (Mascota, Perro, Gato), para que también incluyan como clase base a Visualizador.
    * **NO** modifique el contenido de las clases ya creadas (Mascota, Perro, Gato).
3. En el resumen en pantalla usar el método `resumen` de la clase Visualizador.
4. Mantenga la misma interfaz de ingreso de datos.

## Ejemplo de interacción

```
> Cuantas mascotas va a ingresar?
< 3
> Mascota 1, que clase es (P)erro o (G)ato?
< perro
> cual es el nombre del Perro?
< Motas
> que edad tiene 'Motas'?
< 1
> de que raza es 'Motas'?
< doberman
> Mascota 2, que clase es (P)erro o (G)ato?
< perro
> cual es el nombre del Perro?
< Firulais
> que edad tiene 'Firulais'?
< 3
> de que raza es 'Firulais'?
< pastor aleman
> Mascota 3, que clase es (P)erro o (G)ato?
< gato
> cual es el nombre del Perro?
< Kity
> que edad tiene 'Kity'?
< 4
> de que raza es 'Kity'?
< siames
> Resumen:
> |Clase |Nombre   |Edad   |Raza         |Fecha de ingreso          |
> |Perro |Motas    |1 años |Doberman     |2025-03-25T13:14:26-05:00 |
> |Perro |Firulais |3 años |Pastor Aleman|2025-03-25T13:14:59-05:00 |
> |Gato  |Kity     |4 años |Siames       |2025-03-25T13:15:15-05:00 |
```

## Requisitos mínimos

* Debe usar al menos una clase base y clases derivadas, también debe instanciar objetos de las clases derivadas definidas en el programa. El no usar clases y objetos implicará 0.0 en el porcentaje de funcionalidad.
* Debe existir una clase llamada `Visualizador`, con un método llamado `resumen`, y que debe usarse para la generación del resumen (se detectarán los llamados a este método). El no cumplir con estas condiciones implicará 0.0 en el porcentaje de funcionalidad.

## Fecha máxima de entrega

`2025-04-28T07:00:00-05:00`

### Evaluación

|Porcentaje|Item            |Descripción                                                                 |
|:--------:|:--------------:|:---------------------------------------------------------------------------|
|30%       |Sintaxis        |Revisión de sintaxis, 0% si aparece un error                                |
|30%       |Funcionalidad   |Cumplimiento de la funcionalidad del programa                               |
|30%       |Buenas prácticas|Revisión de PEP8, existencia de docstrings y comentarios útiles en el código|
|10%       |Tests unitarios |Existencia de al menos un test unitario funcional y que reporte OK          |
