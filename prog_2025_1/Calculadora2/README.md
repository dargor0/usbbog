# Práctica de clase: Calculadora2

## Descripción

Extender el programa de calculadora sencilla del taller anterior.

1. Permita que el usuario pueda hacer varias operaciones, ya sea preguntando si quiere continuar, o si quiere salir.
2. Pregunte primero por la operación a realizar, antes de los operandos.
3. Permita cancelar la operación en curso cuando esté recibiendo los operandos.
4. Incluya soporte de números fraccionarios (float).
5. Detecte los errores en el ingreso de los operandos, y conteste apropiadamente.
6. Añada las operaciones de potenciación, división entera y módulo.
7. Tenga en cuenta que las operaciones división entera y módulo requieren enteros; haga las conversiones de datos apropiadas.

## Ejemplo de interacción

```
> Escriba 1 para suma, 
>         2 para resta, 
>         3 para multiplicación 
>         4 para división.
>         5 para potenciación.
>         6 para división entera.
>         7 para módulo.
>         8 para salir.
< 1
> Ingrese el operando A (vacío para cancelar):
< 10.5
> Ingrese el operando B (vacío para cancelar):
< 20.1
> El resultado de la suma es: 30.6
> Escriba 1 para suma, 
>         2 para resta, 
>         3 para multiplicación 
>         4 para división.
>         5 para potenciación.
>         6 para división entera.
>         7 para módulo.
>         8 para salir.
< 2
> Ingrese el operando A:
< hola
> Dato inválido, por favor Ingrese el operando A:
<
> Operación cancelada
> Escriba 1 para suma, 
>         2 para resta, 
>         3 para multiplicación 
>         4 para división.
>         5 para potenciación.
>         6 para división entera.
>         7 para módulo.
>         8 para salir.
< 8
> Gracias!
```

## Requisitos mínimos

* Ningún requisito adicional.

## Fecha máxima de entrega

(Plazo antiguo: `2025-03-31T20:00:00-05:00`)
* Simulacro de evaluación: `2025-04-21T20:00:00-05:00`
* Evaluacion definitiva: `2025-04-24T23:00:00-05:00` (sujeto a solicitud de recalificación).

### Evaluación

NOTA: Debido a que aún no se han visto tests unitarios, se desactiva el item "Tests Unitarios", y se suma ese 10% al item "Buenas prácticas".

|Porcentaje|Item            |Descripción                                                                 |
|:--------:|:--------------:|:---------------------------------------------------------------------------|
|30%       |Sintaxis        |Revisión de sintaxis, 0% si aparece un error                                |
|30%       |Funcionalidad   |Cumplimiento de la funcionalidad del programa                               |
|40%       |Buenas prácticas|Revisión de PEP8, existencia de docstrings y comentarios útiles en el código|
|0%        |Tests unitarios |(desactivado)                                                               |


