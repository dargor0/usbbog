# Práctica de clase: Mascotas1

## Descripción

Hacer un programa que permita el manejo de mascotas en una veterinaria.

1. Haga una clase Mascota y ponga los atributos y métodos que considere necesarios.
2. Haga dos clases derivadas de Mascota: Perro y Gato
3. Haga una interfaz que permita ingresar los datos de la mascota. Los datos mínimos son:

    * Clase (perro o gato)
    * Nombre
    * Edad
    * Raza

4. Cada vez que ingrese un dato, debe registrar la fecha y hora de ingreso, tomando como fecha y hora la actual.
5. Muestre en pantalla los datos de todas las mascotas ingresadas.

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

## Fecha máxima de entrega

`2025-03-31T07:00:00-05:00`

### Evaluación

|Porcentaje|Item            |Descripción                                                                 |
|:--------:|:--------------:|:---------------------------------------------------------------------------|
|30%       |Sintaxis        |Revisión de sintaxis, 0% si aparece un error                                |
|30%       |Funcionalidad   |Cumplimiento de la funcionalidad del programa                               |
|30%       |Buenas prácticas|Revisión de PEP8, existencia de docstrings y comentarios útiles en el código|
|10%       |Tests unitarios |Existencia de al menos un test unitario funcional y que reporte OK          |


