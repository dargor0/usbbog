# Práctica de clase: CalcFecha1

## Descripción

Hacer un programa que haga cálculos de fechas.

1. Muestre la fecha actual (zona horaria local) en pantalla.
2. Permita que el usuario ingrese una cantidad de segundos (con signo) o cantidad de días (también con signo).
3. Calcule la fecha resultante de sumar la cantidad de tiempo registrada anteriormente (restar en caso de poner un número negativo).

Pueden consultar el paquete de manejo de fechas en este [enlace](https://docs.python.org/3/library/datetime.html).

## Ejemplo de interacción

```
> La fecha actual es: 2025-05-15 19:32:47.992709
> Escriba 1 para ingresar segundos, 
>         2 para ingresar dias,
>         3 para salir.
< 1
> Escriba la cantidad de segundos
< 10000
> La nueva fecha es: 2025-05-15 22:20:43.992709
> 
> La fecha actual es: 2025-05-15 19:34:56.847213
> Escriba 1 para ingresar segundos, 
>         2 para ingresar dias,
>         3 para salir.
< 2
> Escriba la cantidad de días
< -10
> La nueva fecha es: 2025-05-05 19:34:56.847213
>
> La fecha actual es: 2025-05-15 19:36:27.239813
> Escriba 1 para ingresar segundos, 
>         2 para ingresar dias,
>         3 para salir.
< 3
> Gracias!
```

## Requisitos mínimos

* Ningún requisito adicional.

## Fecha máxima de entrega

`2025-04-28T20:00:00-05:00`

### Evaluación

NOTA: Debido a que aún no se han visto tests unitarios, se desactiva el item "Tests Unitarios", y se suma ese 10% al item "Buenas prácticas".

|Porcentaje|Item            |Descripción                                                                 |
|:--------:|:--------------:|:---------------------------------------------------------------------------|
|30%       |Sintaxis        |Revisión de sintaxis, 0% si aparece un error                                |
|30%       |Funcionalidad   |Cumplimiento de la funcionalidad del programa                               |
|40%       |Buenas prácticas|Revisión de PEP8, existencia de docstrings y comentarios útiles en el código|
|0%        |Tests unitarios |(desactivado)                                                               |


