#!/usr/bin/env python3
"""07_ejercicios.py

Tema 1 - Ejercicios de repaso (enunciados detallados, SIN solución).
Ejecutar:  python3 07_ejercicios.py

Cada ejercicio indica su objetivo, los datos dados y el procedimiento
esperado. Complete cada sección marcada con #### SOLUCION ####.
La versión resuelta está en 07_ejercicios_solved.py.

"""

import numpy as np

# ======================================================================
# Ejercicio 1: Resolución de un ADC
# ======================================================================
# Objetivo:      calcular el número de niveles y la resolución (paso de
#                cuantización) de un convertidor analógico-digital.
# Concepto:      niveles = 2^b,  Delta = (Vmax - Vmin) / 2^b.
# Datos:         b = 12 bits, rango Vmin = 0 V, Vmax = 5 V.
# Procedimiento: 1) número de niveles = 2^b.
#                2) Delta en voltios y en milivoltios.
# Verificar:     Delta ~ 1.22 mV (12 bits sobre 5 V).
#
# Extra:  ¿Cuál es la máxima amplitud (pico) sin recorte si la señal de
#         entrada debe quedar a 90 % de la escala? (piense en 0.9*5 V).

#### SOLUCION ####

# ======================================================================
# Ejercicio 2: SQNR de un seno a plena escala
# ======================================================================
# Objetivo:      estimar la relación señal-ruido de cuantización (SQNR)
#                para un seno a plena escala.
# Concepto:      SQNR ~= 6.02*b + 1.76 dB.
# Datos:         b = 8, 10 y 16 bits.
# Procedimiento: aplique la fórmula para cada b y compare los valores.
# Verificar:     - 8 bits  -> ~49.9 dB (voz/PCM).
#                - 16 bits -> ~98.1 dB (audio de CD).

#### SOLUCION ####

# ======================================================================
# Ejercicio 3: Frecuencia normalizada
# ======================================================================
# Objetivo:      pasar de frecuencia física (Hz) a frecuencia digital
#                normalizada (rad/muestra).
# Concepto:      w0 = 2*pi*f0 / fs.
# Datos:         a) f0 = 1 kHz, fs = 8 kHz.
#                b) f0 = 5 kHz, fs = 8 kHz.
# Procedimiento: calcule w0 en ambos casos.
# Verificar:     - caso a -> w0 = pi/4 = 0.7854 rad/muestra.
#                - caso b -> w0 = 1.25*pi = 3.9270 rad/muestra
#                  (observe que la señal ya no cabe en la banda base:
#                   w0 > pi significa que f0 > fs/2 -> aliasing).

#### SOLUCION ####

# ======================================================================
# Ejercicio 4: Nyquist y aliasing en audio
# ======================================================================
# Objetivo:      decidir si una tasa de muestreo cumple el criterio de
#                Nyquist y, si no, calcular la frecuencia del alias.
# Concepto:      sin aliasing si fs >= 2*fmax; el primer alias de una
#                componente a f0 aparece en fa = |f0 - k*fs|.
# Datos:         audio con fmax = 20 kHz, tonal a f0 = 20 kHz.
#                a) fs = 44.1 kHz (CD).
#                b) fs = 32 kHz (radio digital).
# Procedimiento: 1) compare fs con 2*fmax en cada caso.
#                2) en el caso que falle, calcule fa = |f0 - fs|.
# Verificar:     - 44.1 kHz cumple (44.1 > 40 kHz) -> sin aliasing.
#                - 32 kHz NO cumple (32 < 40 kHz); la tonal de 20 kHz
#                  se "dobla" y aparece como fa = |20 - 32| = 12 kHz.

#### SOLUCION ####

# ======================================================================
# Ejercicio 5: Mejora por bit y bits necesarios
# ======================================================================
# Objetivo:      a) verificar la regla "cada bit extra ~ 6 dB".
#                b) dimensionar el ADC para una SQNR objetivo.
# Concepto:      SQNR(b) - SQNR(b-1) = 6.02 dB (exacto para un seno);
#                b = ceil((SQNR_objetivo - 1.76) / 6.02).
# Datos:         a) b = 3..12.
#                b) SQNR objetivo = 90 dB (grabación profesional).
# Procedimiento: a) calcule SQNR(b) - SQNR(b-1) y compruebe que da 6.02.
#                b) despeje b de la fórmula y redondee hacia arriba.
# Verificar:     - la diferencia es siempre 6.02 dB.
#                - b = ceil((90 - 1.76)/6.02) = 15 bits.

#### SOLUCION ####

# ======================================================================
# Ejercicio 6: RMS del error de cuantización
# ======================================================================
# Objetivo:      verificar que el error de cuantización se comporta como
#                ruido uniforme con RMS ~= Delta/sqrt(12).
# Concepto:      e[n] = x[n] - xq[n] en [-Delta/2, Delta/2];
#                RMS = sqrt(mean(e.^2)) ~= Delta/sqrt(12).
# Datos:         señal uniforme x en [-0.9, 0.9]; b = 4 bits con
#                Vmin = -1, Vmax = 1 (Delta = 2/16 = 0.125).
# Procedimiento: 1) cuantice: xq = Delta*round(x/Delta).
#                2) error e = x - xq; RMS empírico.
#                3) compare con Delta/sqrt(12).
#                4) verifique que |e| nunca supera Delta/2.
# Verificar:     RMS empírico ~= 0.0361 (igual al teórico).

#### SOLUCION ####

# ======================================================================
# Ejercicio 7: Descomposición de una secuencia en impulsos
# ======================================================================
# Objetivo:      expresar cualquier secuencia como suma de impulsos
#                escalados y desplazados: x[n] = sum_k x[k] delta[n-k].
# Datos:         x = [3, 1, 4] definida en n = 0, 1, 2.
# Procedimiento: 1) para cada k = 0, 1, 2 construya delta[n-k] en el rango
#                   nsup = -3..5 y sume x[k]*delta[n-k].
#                2) grafique los impulsos ponderados.
#                3) verifique que la reconstrucción coincide con x en n=0..2.
# Verificar:     valores reconstruidos = [3, 1, 4].

#### SOLUCION ####

# ======================================================================
# Ejercicio 8 (avanzado): seno a plena escala, SQNR empírica
# ======================================================================
# Objetivo:      medir la SQNR empírica de un ADC con simulación y
#                compararla con la fórmula teórica.
# Concepto:      Px = mean(x.^2), Pe = mean((x-xq).^2),
#                SQNR = 10*log10(Px/Pe).
# Datos:         seno a plena escala x = cos(2*pi*3*t) con t = (0:N-1)/N
#                (N = 2^16, periodos enteros para evitar fuga), b = 8 bits,
#                Vmin = -1, Vmax = 1.
# Procedimiento: 1) cuantice y calcule Px, Pe y SQNR.
#                2) compare con 6.02*8 + 1.76 = 49.92 dB.
# Verificar:     la SQNR simulada queda cerca de la teórica (50.0 dB).
#
# (Sugerencia: reutilice el código de 05_sqnr_bits.py con b = 8.)

#### SOLUCION ####
