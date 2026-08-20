# Ejercicios Tema 1 - Aplicaciones de Telecomunicaciones

Ejemplos y ejercicios para el Tema 1 (*Diseno y evaluacion de enlaces de telecomunicaciones*).

## Sugerencia de Herramientas

| Necesidad | Herramienta mas adecuada |
|---|---|
| Calculo de presupuesto/cobertura/capacidad | **Python/Octave** (este set) |
| Simulacion de *forma de onda* / BER de un sistema completo | **GNU Radio** (bloques en flujograma) o **MATLAB Communications Toolbox** |
| Simulacion de enlace nivel fisico 5G (Rayleigh/MIMO) | **Sionna** (NVIDIA, Python/TensorFlow) |
| Modelos de propagacion ITU-R (lluvia, atmosfera) | `itu-p1234`, `pycraf` (Python) |
| Parametros S / RF de componentes (no es presupuesto de enlace) | `scikit-rf` |
| Verificacion rapida sin programar | Calculadoras de enlace en linea |

## Archivos

| Archivo | Lamina(s) | Contenido |
|---------|-----------|-----------|
| `01_presupuesto_enlace.py` / `.m` | Presupuesto de enlace; Parametros; EIRP; Ejemplo 5.8 GHz | Recrea el ejemplo (L_esp=121.7 dB, P_r=-78.7 dBm, margen 11.3 dB); varia d y f; alcance maximo y margen de fading |
| `02_ruido_sensibilidad.py` | Ruido y sensibilidad (1/2, 2/2) | Piso de ruido `N = -174+10log10(B)+NF`; sensibilidad `P_min=N+SNR_min`; SNR y margen; efecto de NF y B |
| `03_capacidad_shannon.py` | Capacidad de canal; Ejemplo y limite | `C = B log2(1+SNR)` (133 Mbps); eficiencia espectral y regla de los 3 dB |
| `04_cobertura.py` | Cobertura | Radio de cobertura (18.37 km); modelo log-distance (n=2,3,4); curva P_r vs d |
| `05_desvanecimiento.py` | Desvanecimiento (1/3..3/3) | Rayleigh/Rician (PDFs), sombras log-normal, probabilidad de desvanecimiento profundo y margen |

Cada script incluye un **ejemplo resuelto** y **ejercicios propuestos** (marcados `[ejercicios propuestos]`) con indicaciones para modificarlos y verificarlos.

## Paquetes de Python usados

### Paquetes generales

| Paquete | Version | Uso en este set |
|---------|---------|-----------------|
| `numpy` | 2.3.5 | Calculo numerico: formulas en dB, logaritmos, arrays, `linspace`/`logspace` para curvas |
| `matplotlib` | 3.10.7 | Graficas: `semilogx`/`loglog`, histogramas, figuras PNG o en pantalla (`--show`) |
| `scipy` | 1.16.3 | Solo en `05`: distribuciones (`stats.norm`), funcion de Bessel modificada (`ive`) para la PDF de Rician |
| (Octave) | 11.1 | Version equivalente de `01` sin instalar nada adicional |

Instalar y verificar:
```bash
python3 -m pip install --user numpy scipy matplotlib
python3 -c "import numpy, scipy, matplotlib; print(numpy.__version__, scipy.__version__, matplotlib.__version__)"
```

## Como ejecutar

```bash
# Python (instalar dependencias la primera vez)
python3 -m pip install --user numpy scipy matplotlib

python3 01_presupuesto_enlace.py
python3 02_ruido_sensibilidad.py
python3 03_capacidad_shannon.py
python3 04_cobertura.py
python3 05_desvanecimiento.py

# Version Octave del presupuesto de enlace
octave-cli 01_presupuesto_enlace.m

# Ver las graficas en pantalla (ventanas interactivas)
python3 01_presupuesto_enlace.py --show

# Sin pantalla (servidor/SSH), guarda los PNG
MPLBACKEND=Agg python3 01_presupuesto_enlace.py
```

## Resultados esperados (resumen)

- **Presupuesto**: `EIRP=33 dBm`, `L_esp=121.7 dB`, `P_r=-78.7 dBm`, margen `11.3 dB`; alcance maximo `18.37 km` a 5.8 GHz.
- **Ruido**: `N=-98 dBm` (B=20 MHz, NF=3 dB); con SNR_min=12 dB, `P_min=-86 dBm` y margen `7.3 dB` (SNR en RX = 19.3 dB).
- **Capacidad**: `C=133 Mbps` (B=20 MHz, SNR=20 dB); cada 3 dB de SNR suma ~1 bit/s/Hz.
- **Cobertura**: `d_max=18.37 km` (espacio libre); `3.23 km` con n=3 (urbano) y `1.36 km` con n=4.
- **Desvanecimiento**: Rayleigh mediana ~0.83 (Rician mayor con LOS); ~2% de probabilidad de caer 20 dB bajo la media en Rayleigh.

## Ejercicios propuestos

1. Cambie la sensibilidad a -85 dBm y recalcule margen y alcance.
2. Agregue perdidas por lluvia (3 dB) al presupuesto y verifique el margen.
3. Calcule la capacidad para B=10 MHz y SNR=10 dB (~35 Mbps).
4. Compare cobertura en espacio libre vs modelo urbano (n=3).
5. Cambie el factor K de Rician y observe la PDF del desvanecimiento.
