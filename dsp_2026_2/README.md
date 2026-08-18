# Ejercicios Tema 1 - Procesamiento Digital de Señal

Scripts de ejemplo y ejercicios para el Tema 1 (*Repaso de señales continuas
y discretas*). Cada tema tiene dos versiones equivalentes: **Octave/Matlab** (`.m`) y
**Python/SciPy** (`.py`).

## Requisitos

- **Octave**: `sudo apt install octave` (o usar MATLAB).
- **Python**: `python3 -m pip install numpy scipy matplotlib`.

## Archivos

| Archivo | Tema de las láminas | Contenido |
|---------|---------------------|-----------|
| `01_senales_elementales` | Señales elementales | impulso, escalón, exponencial y seno; descomposición en impulsos |
| `02_muestreo` | Muestreo | `x[n]=x(nT_s)`, `f_s=1/T_s`, frecuencia normalizada, Nyquist |
| `03_cuantizacion` | Cuantización | resolución `delta=(V_max−V_min)/2^b`, señal en escalera |
| `04_error_cuantizacion` | Error de cuantización | `e[n]`, distribución uniforme, RMS `~ delta/sqrt(12)` |
| `05_sqnr_bits` | Error de cuantización | `SQNR ~ 6.02 b + 1.76` dB, ~6 dB por bit extra |
| `06_aliasing` | Muestreo / Nyquist | alias a `|f_0−f_s|` cuando `f_s < 2 f_0` |
| `07_ejercicios` | Repaso | ejercicios con enunciado detallado (sin solución, para completar) |
| `07_ejercicios_solved` | Repaso | los mismos ejercicios con su solución (no publicado aún) |

Cada script incluye un **ejemplo** resuelto y **ejercicios** (marcados
`%% Ejercicio` en Octave / `# Ejercicio` en Python) para que el estudiante
modifique parámetros y verifique los conceptos.

Los archivos `07_ejercicios` plantean cada problema con objetivo, datos,
procedimiento y verificación, dejando el código en `%%% SOLUCION %%%`
(Octave) o `#### SOLUCION ####` (Python) para que lo complete el
estudiante.

## Cómo ejecutar

```bash
# Octave
octave-cli 01_senales_elementales.m

# Python
python3 01_senales_elementales.py
```

Los scripts generan figuras; si no hay pantalla (SSH/servidor) use en Python:

```bash
MPLBACKEND=Agg python3 01_senales_elementales.py
```

## Resumen de resultados esperados

- `02_muestreo`: para `f_0=2` Hz y `f_s=20` Hz, `omega_0 = 2*PI*2/20 = PI/5`.
- `04_error_cuantizacion`: RMS empírico del error ~ `delta/sqrt(12)`.
- `05_sqnr_bits`: la curva simulada coincide con `6.02 b + 1.76` dB.
- `06_aliasing`: con `f_0=100` Hz y `f_s=70` Hz aparece un alias en 30 Hz.
- `07_ejercicios`: ADC 12 bits/5 V → delta ~ 1.22 mV; SQNR 16 bits ~ 98 dB.
