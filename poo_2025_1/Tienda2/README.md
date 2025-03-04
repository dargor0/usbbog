# Práctica de clase: Tienda2

## Descripción

Extender el programa que maneje un inventario de una tienda, con nuevas funcionalidades.

1. Con base en la clase que modela el producto de la tienda, añadir los siguientes atributos:

    * Descripción: texto adicional que explique las características del producto.
    * Clasificación: es como una "etiqueta" que le permita clasificar el producto dentro de un conjunto de productos: por ejemplo "alimentación", "aseo", "licores", etc. La elección de etiquetas es libre.

2. Cambie la interfaz de usuario para añadir una cantidad arbitraria de productos (puede preguntar por el número de productos a ingresar), y recopilar los nuevos atributos.
3. Muestre en pantalla los datos de todos los productos recopilados.
4. Muestre un resumen del precio por clasificación, es decir, calcule el precio de todos los productos de una clasificación y muestrela como el precio de esa clasificación.

## Ejemplo de interacción

```
> Cuantos productos va a ingresar?
< 3
> Producto 1, cual es el nombre?
< pan
> cual es el precio de 'pan'?
< 2000
> que cantidad hay de 'pan'?
< 10
> introduzca la descripción de 'pan':
< pan tajado marca bimbo
> qué clasificación tiene 'pan'?
< alimentación
> Producto 2, cual es el nombre?
< leche
> cual es el precio de 'leche'?
< 5000
> que cantidad hay de 'leche'?
< 15
> introduzca la descripción de 'leche':
< bolsa de leche marca alpina
> qué clasificación tiene 'leche'?
< alimentación
> Producto 3, cual es el nombre?
< huevo
> cual es el precio de 'huevo'?
< 500
> que cantidad hay de 'huevo'?
< 200
> introduzca la descripción de 'huevo':
< cartón de huevos x30 marca el granjero
> qué clasificación tiene 'huevo'?
< alimentación
> Resumen:
> |Producto |Cantidad     |Precio     |Descripción  |Clasificación |
> |pan      |10 unidades  |2000 pesos |pan tajado...|alimentación  |
> |leche    |15 unidades  |5000 pesos |bolsa de l...|alimentación  |
> |huevo    |200 unidades |500 pesos  |cartón de ...|alimentación  |
> Precios por clasificación
> |Clasificación |Precio     |
> |alimentación  |7500 pesos |
```

## Requisitos mínimos

* Debe usar clases e instanciar objetos de la clase definida. El no usar clases y objetos implicará 0.0 en el porcentaje de funcionalidad.

## Fecha máxima de entrega

`2025-03-07T20:00:00-05:00`

### Evaluación

|Porcentaje|Item            |Descripción                                                                 |
|:--------:|:--------------:|:---------------------------------------------------------------------------|
|30%       |Sintaxis        |Revisión de sintaxis, 0% si aparece un error                                |
|30%       |Funcionalidad   |Cumplimiento de la funcionalidad del programa                               |
|30%       |Buenas prácticas|Revisión de PEP8, existencia de docstrings y comentarios útiles en el código|
|10%       |Tests unitarios |Existencia de al menos un test unitario funcional y que reporte OK          |


