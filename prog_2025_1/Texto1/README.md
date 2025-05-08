# Práctica de clase: Texto1

## Descripción

Hacer un programa que haga cambios en un texto introducido.

1. Permita ingresar una línea de texto arbitrario.
2. Desplegar un menú de operaciones, que se puede repetir cuantas veces desee el usuario.
3. Incluya las siguientes operaciones:
    * Pasar a minúsculas.
    * Pasar a mayúsculas.
    * Invertir mayúsculas / minúsculas.
    * Pasar a "capitalización" (Primera letra mayúscula, las demás minúsculas).
    * Pasar a "titulación" (Primera letra mayúscula en cada palabra, las demás minúsculas).
    * Reemplazar espacios por guiones bajos.
4. Mostrar el resultado en pantalla.
5. No permita volver a ingresar otra línea de texto, para eso el programa debe terminar.

Pueden consultar la lista de operaciones de strings en este [enlace](https://www.digitalocean.com/community/tutorials/python-string-functions).

## Ejemplo de interacción

```
> Ingrese la línea de texto:
< hola mundo
> Escriba 1 para pasar a minúsculas, 
>         2 para pasar a mayúsculas, 
>         3 para invertir mayúsculas y minúsculas 
>         4 para pasar a capitalización.
>         5 para pasar a titulación.
>         6 para reemplazar espacios por guiones bajos.
>         7 para salir.
< 2
> Resultado: HOLA MUNDO
> Escriba 1 para pasar a minúsculas, 
>         2 para pasar a mayúsculas, 
>         3 para invertir mayúsculas y minúsculas 
>         4 para pasar a capitalización.
>         5 para pasar a titulación.
>         6 para reemplazar espacios por guiones bajos.
>         7 para salir.
< 5
> Resultado: Hola Mundo
> Escriba 1 para pasar a minúsculas, 
>         2 para pasar a mayúsculas, 
>         3 para invertir mayúsculas y minúsculas 
>         4 para pasar a capitalización.
>         5 para pasar a titulación.
>         6 para reemplazar espacios por guiones bajos.
>         7 para salir.
< 6
> Resultado: hola_mundo
> Escriba 1 para pasar a minúsculas, 
>         2 para pasar a mayúsculas, 
>         3 para invertir mayúsculas y minúsculas 
>         4 para pasar a capitalización.
>         5 para pasar a titulación.
>         6 para reemplazar espacios por guiones bajos.
>         7 para salir.
< 7
> Gracias!
```

## Requisitos mínimos

* Ningún requisito adicional.

## Fecha máxima de entrega

(Plazo antiguo: `2025-04-07T20:00:00-05:00`) 
* Nuevo plazo `2025-05-09T20:00:00-05:00`.

### Evaluación

NOTA: Debido a que aún no se han visto tests unitarios, se desactiva el item "Tests Unitarios", y se suma ese 10% al item "Buenas prácticas".

|Porcentaje|Item            |Descripción                                                                 |
|:--------:|:--------------:|:---------------------------------------------------------------------------|
|30%       |Sintaxis        |Revisión de sintaxis, 0% si aparece un error                                |
|30%       |Funcionalidad   |Cumplimiento de la funcionalidad del programa                               |
|40%       |Buenas prácticas|Revisión de PEP8, existencia de docstrings y comentarios útiles en el código|
|0%        |Tests unitarios |(desactivado)                                                               |


