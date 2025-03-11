# Práctica de clase: Tienda3

## Descripción

Extender el programa que maneje un inventario de una tienda, con nuevas funcionalidades.

1. Con base en la clase que modela el producto de la tienda, añadir los siguientes métodos:

    * calcula_precio(cantidad): devuelve el precio a pagar, según la cantidad de producto indicado en el atributo "cantidad"
    * inventario_precio(): devuelve el valor total de mercancía de este producto en el inventario.

2. Mantener la misma interfaz que en el taller Tienda2.
3. Muestre en pantalla los datos de todos los productos recopilados.
4. Muestre en pantalla el precio a pagar por una cantidad de 5 por cada producto.
4. Mantenga el resumen del precio por clasificación.

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
> |Producto |Cantidad     |Precio     |Descripción  |Clasificación |Total en inventario |Precio x5 unidades |
> |pan      |10 unidades  |2000 pesos |pan tajado...|alimentación  |20000 pesos         |10000 pesos        |
> |leche    |15 unidades  |5000 pesos |bolsa de l...|alimentación  |75000 pesos         |25000 pesos        |
> |huevo    |200 unidades |500 pesos  |cartón de ...|alimentación  |100000 pesos        |2500 pesos         |
> Precios por clasificación
> |Clasificación |Precio     |
> |alimentación  |7500 pesos |
```

## Requisitos mínimos

* Debe usar clases e instanciar objetos de la clase definida. El no usar clases y objetos implicará 0.0 en el porcentaje de funcionalidad.
* Debe usar métodos de clase para calcular los precios de inventario y por x5 unidades. El no usar métodos de clase implicará 0.0 en el porcentaje de funcionalidad.

## Fecha máxima de entrega

`2025-03-14T20:00:00-05:00`

### Evaluación

|Porcentaje|Item            |Descripción                                                                 |
|:--------:|:--------------:|:---------------------------------------------------------------------------|
|30%       |Sintaxis        |Revisión de sintaxis, 0% si aparece un error                                |
|30%       |Funcionalidad   |Cumplimiento de la funcionalidad del programa                               |
|30%       |Buenas prácticas|Revisión de PEP8, existencia de docstrings y comentarios útiles en el código|
|10%       |Tests unitarios |Existencia de al menos un test unitario funcional y que reporte OK          |


