# Ejercicios Tema 1 - Sistemas de Radiacion Electromagnetica

Scripts de ejemplo y ejercicios para el Tema 1 (*Fundamentos de electromagnetismo y radiacion*).

## Contenido

| Archivo | Lamina(s) | Herramienta | Contenido |
|---------|-----------|-------------|-----------|
| `ejemplo_adaptacion_antena.py` | Ejemplo practico: adaptar una antena; carta de Smith (1/2, 2/2) | **scikit-rf** | Recrea paso a paso el ejemplo (Gamma, VSWR, C = 79.6 pF, Z_t = 38.7 ohm), lo verifica con parametros S y dibuja la trayectoria `z_L -> z' -> centro` en la carta de Smith |


## Herramientas exploradas

Ademas de **scikit-rf**, se exploran estas herramientas de codigo abierto:

- **ngspice / PySpice** - simulacion de circuitos y lineas de transmision (onda estacionaria y VSWR). `ejercicio_swr_ngspice.py` usa la biblioteca `libngspice` via PySpice; `linea_swr.cir` usa el binario `ngspice`.
- **4nec2 / xnec2c / nec2c / PyNEC** - metodo de momentos (NEC2) para antenas de hilo. `ejercicio_dipolo_pynec.py` usa **PyNEC** (port Python de NEC2) y genera `dipolo_4nec2.nec` para abrirlo en 4nec2/xnec2c.
- **Octave / numpy / scipy** - calculo y graficacion de campos.
- Otras alternativas: **Qucs** (circuitos RF con carta de Smith), **OpenEMS** (FDTD), **MMANA-GAL** (analisis de antenas).

## Como ejecutar

### 1. Instalar dependencias

```bash
python3 -m pip install --user scikit-rf numpy scipy matplotlib
python3 -m pip install --user pynec pyspice
```

Para ngspice (PySpice usa la biblioteca compartida):
```bash
# Debian/Ubuntu:  sudo apt install ngspice
# (instala tambien libngspice; si falta, el paquete es libngspice0)
```

Si `libngspice.so` no se encuentra al importar PySpice, cree un enlace y ajuste la ruta de busqueda:
```bash
mkdir -p ~/.local/lib
ln -s /usr/lib/x86_64-linux-gnu/libngspice.so.0 ~/.local/lib/libngspice.so
export LD_LIBRARY_PATH=$HOME/.local/lib:$LD_LIBRARY_PATH
```

### Paquetes de Python usados

| Paquete | Version | Se usa en |
|---------|---------|-----------|
| `scikit-rf` | 2.1.0 | carta de Smith y parametros S (`ejemplo_adaptacion_antena.py`) |
| `pynec` | 2.3.4 | NEC2 (metodo de momentos) (`ejercicio_dipolo_pynec.py`) |
| `pyspice` | 1.5 | interfaz Python para ngspice (`ejercicio_swr_ngspice.py`) |
| `numpy` | 2.3.5 | calculo numerico (todos los scripts) |
| `scipy` | 1.16.3 | calculo y analisis (onda plana, dipolo) |
| `matplotlib` | 3.10.7 | graficacion (todos los scripts) |

Verificarlas con:
```bash
python3 -c "import skrf, pynec, PySpice, numpy, scipy, matplotlib; \
print(skrf.__version__, PySpice.__version__)"
```

> Nota: `pynec` se importa como `PyNEC` (con mayusculas); la biblioteca de
> ngspice se carga como `libngspice` (paquete `libngspice0` en Debian).

### Tutoriales recomendados (herramientas de codigo abierto)

- **scikit-rf** (parametros S y carta de Smith en Python)
  - Documentacion: <https://scikit-rf.readthedocs.io>
  - Ejemplos: <https://scikit-rf.readthedocs.io/en/latest/examples/index.html>
  - Carta de Smith: <https://scikit-rf.readthedocs.io/en/latest/api/generated/skrf.plotting.plot_smith.html>
- **PyNEC / NEC2** (antenas por metodo de momentos)
  - Repositorio y ejemplos: <https://github.com/tmolteno/python-necpp>
  - Guia rapida (dipolo, monopolo, patron): <https://github.com/tmolteno/python-necpp/tree/master/PyNEC/example>
  - xnec2c (GUI Linux, compatible con el `.nec` generado): <http://www.xnec2c.org>
  - 4nec2 (GUI Windows): <https://www.qsl.net/4nec2>
- **ngspice / PySpice** (SPICE)
  - Documentacion de ngspice: <https://ngspice.sourceforge.io>
  - Manual (cap. de lineas de transmision): <https://ngspice.sourceforge.io/docs.html>
  - PySpice: <https://pyspice.fabrice-salvaire.fr>
  - Tutorial PySpice (instalacion y primeros circuitos): <https://pyspice.fabrice-salvaire.fr/releases/v1.5/installation.html>
- **numpy / scipy / matplotlib**
  - numpy: <https://numpy.org/doc/stable>
  - scipy: <https://docs.scipy.org/doc/scipy>
  - matplotlib: <https://matplotlib.org/stable/tutorials/index.html>
- **Octave** (version equivalente de la onda plana)
  - Documentacion: <https://octave.org/doc/latest/>
  - Wiki/tutoriales: <https://wiki.octave.org>

### 2. Ejecutar cada script

```bash
# Ejemplo de adaptacion de antena (carta de Smith con scikit-rf)
python3 ejemplo_adaptacion_antena.py
```

Sin pantalla (servidor/SSH) use el backend sin interfaz:
```bash
MPLBACKEND=Agg python3 ejemplo_adaptacion_antena.py
```

Para ver las graficas en pantalla (ventanas interactivas) en lugar de
guardarlas en archivos, agregue `--show` a cualquiera de los scripts:
```bash
python3 ejemplo_adaptacion_antena.py --show
```

## Resultados esperados (resumen)

- **Adaptacion**: `Gamma = -0.176 + j0.294`, `|Gamma| = 0.343`, `VSWR = 2.04`, `C = 79.6 pF`, `Z_t = 38.7 ohm`; tras adaptar, `|S11| ~ 1e-16` (adaptado).

## Ejercicios propuestos (breve guia)

1. Repita el ejemplo de adaptacion con `Z_L = 60 - j30 ohm`.
