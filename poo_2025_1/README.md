# Programación Orientada a Objetos (POO) - 2025-1

Recursos sobre el desarrollo de la asignatura.

## Prácticas de clase

Las prácticas consisten en ejercicios propuestos por el docente, para entrega a través de github. Se requiere cumplir con los siguientes requisitos:

* Cada estudiante debe crear un repositorio llamado `entregas-poo-2025-1` (usar este nombre exacto), y dentro de éste hacer subcarpetas con el nombre exacto de la práctica a entregar.
* Dentro de cada carpeta añadir uno o varios archivos, según las necesidades del ejercicio. De esos archivos, uno sólo debe ser el punto de entrada de su programa.
    * Los archivos deben tener la extensión correcta (por ejemplo los archivos de Python tienen extensión `".py"`). El evaluador ignorará cualquier archivo sin extensión.
    * Si usa Python como lenguaje de programación, se recomienda usar este [archivo de plantilla](template.py) para las entregas, para evitar problemas con el software de evaluación del ejercicio.
    * Si usa otro lenguaje de programación, debe añadir en la carpeta de la práctica un archivo de texto plano llamado `lang.txt`, que debe contener una sola línea con el nombre del lenguaje de programación usado. Esto con el fin de que el software de evaluación pueda interpretar correctamente su ejercicio. Si no lo hace, el software de evaluación asumirá que usa Python. Para más información ver la sección [Otros lenguajes de programación](#otros-lenguajes-de-programación).
    * Si usa herramientas como Google Colab o Jupyter para desarrollar en Python, debe añadir en la carpeta de la práctica un archivo de texto plano llamado `lang.txt`, que debe contener una sola línea con el nombre del entorno que usó. Por ejemplo si usó Google Colab, debe poner dentro del archivo `lang.txt` el texto `colab`.
* Opcionalmente (recomendado) debe existir uno o varios archivos de test unitario, que deben comenzar con el prefijo `test_`.
* **ACTUALIZADO**: Debe hacer el commit de los archivos del ejercicio antes del lunes siguiente de cada semana a las 07:00 hora local Colombiana (UTC-5). Cualquier commit que involucre archivos de dicha práctica después de esta fecha límite, será ignorado para efectos de evaluación.
* Se recomienda usar [pycodestyle](https://pypi.org/project/pycodestyle/) para revisar cumplimiento de estilo según PEP8 para cumplir con el porcentaje de buenas prácticas.

### Evaluación

|Porcentaje|Item            |Descripción                                                                  |
|:--------:|:--------------:|:----------------------------------------------------------------------------|
|30%       |Sintaxis        |Revisión de sintaxis, 0% si aparece un error                                 |
|30%       |Funcionalidad   |Cumplimiento de la funcionalidad del programa, requisitos mínimos            |
|30%       |Buenas prácticas|Revisión de PEP8, existencia de docstrings y comentarios útiles en el código |
|10%       |Tests unitarios |Existencia de al menos un test unitario funcional y que reporte OK           |

### Cronograma

|Número|Fecha     |Nombre                          |Descripción                 |Evaluado en corte|
|:----:|:--------:|:------------------------------:|:---------------------------|:---------------:|
|1     |2025-02-25|[Tienda1](Tienda1/README.md)    |Inventario de tienda 1      |1                |
|2     |2025-03-04|[Tienda2](Tienda2/README.md)    |Inventario de tienda 2      |1                |
|3     |2025-03-11|[Tienda3](Tienda3/README.md)    |Inventario de tienda 3      |2                |
|-     |2025-03-18|                                | (sin práctica)             |                 |
|4     |2025-03-25|[Mascotas1](Mascotas1/README.md)|Mascotas en el veterinario 1|2                |
|-     |2025-04-01|                                | (sin práctica)             |                 |
|-     |2025-04-08|                                | (sin práctica)             |                 |
|6     |2025-04-22|[Mascotas2](Mascotas2/README.md)|Mascotas en el veterinario 2|3                |
|7     |2025-04-29|[CalcMat](CalcMat/README.md)    |Calculadora de matrices     |3                |
|8     |2025-05-06|                                |                            |                 |
|9     |2025-05-13|                                |                            |                 |
|10    |2025-05-20|                                |                            |                 |
|11    |2025-05-27|                                |                            |                 |

### Otros lenguajes de programación

Si usa otros lenguajes de programación, debe tener en cuenta:

* Debe incluir el archivo `lang.txt` en la carpeta de su taller, si no lo hace, la herramienta evaluará incorrectamente el ejercicio, y no se admitirán reclamos posteriores con respecto a la evaluación.
* El uso de herramientas como Google Colab o Jupyter notebooks implica que se debe incluir este archivo, para notificar al evaluador de que debe hacer la conversión de archivo `".ipynb"` a `".py"`. Si no lo hace, la herramienta evaluará incorrectamente el ejercicio, y no se admitirán reclamos posteriores con respecto a la evaluación.
    * Para uso de Google Colab, debe incluir el texto `colab`.
    * Para otras herramientas, debe consultarlo con el docente.
* Detalles de lenguajes específicos:
    * `C` o `C++`: 
        * La evaluación se realizará usando el compilador `gcc` versión 14.2 sobre plataforma Linux.
        * Se usará el estándar C23 para C y C++20 para C++ (se incluirá en los flags de compilación).
        * Evite usar librerías dependientes de Windows o librerías no estándar, pues muy posiblemente fallará en el proceso de compilación. Si requiere usar librerías externas, debe adjuntar un Makefile (para usar make) o un CMakeLists.txt (para usar cmake) con las instrucciones de compilación.
        * La evaluación de sintaxis consiste en una compilación correcta sin errores ni warnings; la herramienta detectará los warnings generados y restará 2% de nota por cada warning emitido.
        * La evaluación de funcionalidad usará la entrada y salida estándar (stdin y stdout) para interactuar con el programa compilado, evite usar la salida de error (stderr), la herramienta ignorará esta salida.
        * La evaluación de buenas prácticas se hará con respecto a la guía de [estilo de google](https://google.github.io/styleguide/cppguide.html), la verificación se hará con la herramienta [cpplint](https://github.com/cpplint/cpplint). La herramienta no buscará docstrings (pues no se menciona en la guía de estilo), en su lugar buscará comentarios asociados a las principales estructuras del archivo: un comentario general de archivo, y comentarios asociados a funciones y clases.
