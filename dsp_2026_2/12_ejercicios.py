#!/usr/bin/env python3
"""12_ejercicios.py

Tema 2 - Ejercicios de repaso (enunciados detallados, SIN solucion).
Ejecutar:  python3 12_ejercicios.py

Complete cada seccion marcada con #### SOLUCION ####.
La version resuelta esta en 12_ejercicios_solved.py.

Cubre las laminas: formulaciones (trigonometrica/exponencial), calculo de
coeficientes, espectro (magnitud/fase), frecuencias negativas y DTFS.
"""

import numpy as np

# ======================================================================
# Ejercicio 1: coeficientes de una onda cuadrada
# ======================================================================
# Objetivo:      calcular los coeficientes de Fourier de una onda cuadrada.
# Concepto:      b_k = 4A/(pi k) (impares); |c_k| = 2A/(pi|k|); a_k = 0.
# Datos:         A = 2, T = 1 s (f0 = 1 Hz).
# Procedimiento: 1) b_1, b_3 y b_5 (impares).
#                2) |c_1|, |c_3| y |c_5|.
#                3) fase de c_1 (k>0) y de c_-1 (k<0).
# Verificar:     |c_1| = 4/pi ~ 1.273; fase c_1 = -pi/2.

#### SOLUCION ####

# ======================================================================
# Ejercicio 2: reconstruccion y fenomeno de Gibbs
# ======================================================================
# Objetivo:      verificar la convergencia y el sobrepaso de Gibbs.
# Concepto:      x(t) = (4A/pi)[sen(w0 t)+(1/3)sen(3 w0 t)+(1/5)sen(5 w0 t)+...].
# Datos:         A = 1, T = 1 s; sumar N = 3 y N = 101 armonicos.
# Procedimiento: 1) construya la suma parcial.
#                2) calcule el pico maximo en cada caso.
#                3) compare con el limite de Gibbs (~1.179 A).
# Verificar:     el pico no baja de ~1.179 A aunque N crezca.

#### SOLUCION ####

# ======================================================================
# Ejercicio 3: DTFS de x[n] = [1, 0, -1, 0]
# ======================================================================
# Objetivo:      calcular los coeficientes DTFS de una senal discreta.
# Concepto:      c_k = (1/N) sum_n x[n] e^{-j2pi k n/N}.
# Datos:         x[n] = [1, 0, -1, 0], N = 4.
# Procedimiento: 1) calcule c_0, c_1, c_2 y c_3 con la sumatoria.
#                2) interprete: que frecuencias sobreviven?
# Verificar:     c_1 = c_3 = 1/2 (equivale a cos(pi n/2)); c_0 = c_2 = 0.

#### SOLUCION ####

# ======================================================================
# Ejercicio 4: teorema de Parseval
# ======================================================================
# Objetivo:      verificar la conservacion de la potencia.
# Concepto:      P = sum_k |c_k|^2 = (1/T) int_T |x(t)|^2 dt (CTFS);
#                sum_k |c_k|^2 = (1/N) sum_n |x[n]|^2 (DTFS).
# Datos:         onda cuadrada A = 1 (CTFS); x[n]=[1,2,1,2] (DTFS).
# Procedimiento: 1) sume |c_k|^2 (k = -9..9) para la onda cuadrada.
#                2) calcule el valor medio cuadratico de x(t).
#                3) repita para la DTFS.
# Verificar:     ambas potencias coinciden.

#### SOLUCION ####

# ======================================================================
# Ejercicio 5: real vs compleja (simetria del espectro)
# ======================================================================
# Objetivo:      decidir si una senal en el tiempo es real o compleja a
#                partir de su espectro.
# Concepto:      senal real -> |c_-k| = |c_k| y fase impar; asimetria
#                -> senal compleja.
# Datos:         a) c_k de una onda cuadrada.
#                b) c_1 = 1 (solo frecuencia positiva).
# Procedimiento: 1) verifique la simetria en el caso (a).
#                2) clasifique cada caso como real o complejo.
# Verificar:     (a) real; (b) compleja.

#### SOLUCION ####

# ======================================================================
# Ejercicio 6 (avanzado): sintesis y error
# ======================================================================
# Objetivo:      medir numericamente la mejora al aumentar N.
# Concepto:      error RMS entre la suma parcial y la senal ideal.
# Datos:         onda cuadrada A = 1, T = 1 s; N = 1, 3, 9, 101.
# Procedimiento: 1) calcule el error RMS para cada N.
#                2) grafique el error vs N (escala log).
# Verificar:     el error decrece a medida que N crece (pero el pico de
#                Gibbs permanece).

#### SOLUCION ####
