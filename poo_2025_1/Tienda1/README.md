# Práctica de clase: Tienda1

## Descripción

Hacer un programa que maneje un inventario de una tienda.

1. Haga una clase para modelar un producto de la tienda con los siguientes atributos

    * Nombre
    * Precio unitario
    * Cantidad

2. Implemente la interfaz de usuario para preguntar por tres (3) productos y recopilar sus atributos.
3. Asegúrese de que el precio unitario se muestre en `pesos` o `COP` y la cantidad en `unidades`.
4. Muestre en pantalla los datos de los tres (3) productos recopilados.

## Ejemplo de interacción

```
> Producto 1, cual es el nombre?
< pan
> cual es el precio de 'pan'?
< 2000
> que cantidad hay de 'pan'?
< 10
> Producto 2, cual es el nombre?
< leche
> cual es el precio de 'leche'?
< 5000
> que cantidad hay de 'leche'?
< 15
> Producto 3, cual es el nombre?
< huevo
> cual es el precio de 'huevo'?
< 500
> que cantidad hay de 'huevo'?
< 200
> Resumen:
> |Producto |Cantidad     |Precio     |
> |pan      |10 unidades  |2000 pesos |
> |leche    |15 unidades  |5000 pesos |
> |huevo    |200 unidades |500 pesos  |
```

## Requisitos mínimos

* Debe usar clases e instanciar objetos de la clase definida. El no usar clases y objetos implicará 0.0 en el porcentaje de funcionalidad.

## Fecha máxima de entrega

`2025-02-28T20:00:00-05:00`

### Evaluación

|Porcentaje|Item            |Descripción                                                                 |
|:--------:|:--------------:|:---------------------------------------------------------------------------|
|30%       |Sintaxis        |Revisión de sintaxis, 0% si aparece un error                                |
|30%       |Funcionalidad   |Cumplimiento de la funcionalidad del programa                               |
|30%       |Buenas prácticas|Revisión de PEP8, existencia de docstrings y comentarios útiles en el código|
|10%       |Tests unitarios |Existencia de al menos un test unitario funcional y que reporte OK          |


