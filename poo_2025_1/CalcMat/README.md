# Práctica de clase: Calculadora de matrices

## Descripción

Desarrollar un programa sencillo de calculadora de matrices

1. Crear una clase Matriz, que almacene los valores de una matriz 2x2.
2. Implementar los operadores suma, resta y multiplicación.
3. Hacer una interfaz sencilla para introducir matrices 2x2, con un menú de operaciones que contenga las operaciones: suma, resta, multiplicación.

## Ejemplo de interacción

```
> Matriz 1: elemento 0,0
< 3
> Matriz 1: elemento 0,1
< 4
> Matriz 1: elemento 1,0
< 5
> Matriz 1: elemento 1,1
< 6
> Matriz 2: elemento 0,0
< 7
> Matriz 2: elemento 0,1
< 8
> Matriz 2: elemento 1,0
< 9
> Matriz 2: elemento 1,1
< 1
> Matriz 1:
> |3  4|
> |5  6|
> Matriz 2:
> |7  8|
> |9  1|
> Escriba 1 para suma, 
>         2 para resta, 
>         3 para multiplicación 
< 1
> La suma de las dos matrices es:
> |10  12|
> |14  7 |
```

## Requisitos mínimos

* Debe existir una clase llamada `Matriz` y debe usarse al menos dos instancias de esta clase (los dos operadores). El no cumplir con estas condiciones implicará 0.0 en el porcentaje de funcionalidad.
* Se debe usar operadores matemáticos estándar ("+", "-", "*") para hacer las operaciones, en vez de funciones especializadas.  El no cumplir con estas condiciones implicará 0.0 en el porcentaje de funcionalidad.

## Fecha máxima de entrega

(Plazo antiguo: `2025-05-05T07:00:00-05:00`) Plazo extendido: `2025-05-14T07:00:00-05:00`

### Evaluación

|Porcentaje|Item            |Descripción                                                                 |
|:--------:|:--------------:|:---------------------------------------------------------------------------|
|30%       |Sintaxis        |Revisión de sintaxis, 0% si aparece un error                                |
|30%       |Funcionalidad   |Cumplimiento de la funcionalidad del programa                               |
|30%       |Buenas prácticas|Revisión de PEP8, existencia de docstrings y comentarios útiles en el código|
|10%       |Tests unitarios |Existencia de al menos un test unitario funcional y que reporte OK          |
