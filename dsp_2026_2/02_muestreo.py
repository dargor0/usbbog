#!/usr/bin/env python3
"""02_muestreo.py

Tema 1 - Muestreo de una señal continua.
Ejecutar:  python3 02_muestreo.py

Uso de SciPy: scipy.signal.resample() para reconstruir (ejercicio 3).
"""

import matplotlib.pyplot as plt
import numpy as np

f0 = 2.0                 # frecuencia de la señal [Hz]
fs = 20.0                # tasa de muestreo [Hz], fs > 2*f0 = 4
Ts = 1.0 / fs

t = np.arange(0, 1, 1e-4)   # eje continuo (denso)
xt = np.cos(2 * np.pi * f0 * t)

n = np.arange(0, fs + 1)    # índices de las muestras
tn = n * Ts                  # instantes de muestreo
xn = np.cos(2 * np.pi * f0 * tn)

fig, ax = plt.subplots()
ax.plot(t, xt, "b", label=r"$x(t)=\cos(2\pi f_0 t)$")
ax.stem(tn, xn, "r", basefmt=" ")
ax.set_title("Muestreo de una señal continua")
ax.set_xlabel("t [s]")
ax.set_ylabel("Amplitud")
ax.legend()
ax.set_ylim(-1.3, 1.3)
plt.tight_layout()

# Frecuencia normalizada
w0 = 2 * np.pi * f0 / fs
print(f"f0 = {f0} Hz, fs = {fs} Hz, Ts = {Ts} s")
print(f"Frecuencia normalizada: w0 = 2*pi*f0/fs = {w0:.4f} rad/muestra")

# Ejercicio 1: comprobar Nyquist. Cambie fs a 2 (caso límite), 3, 4 y 40 y
# observe: fs < 2*f0 -> aliasing; fs >= 2*f0 -> las muestras describen bien
# la señal. Calcule w0 para cada caso.
# Ejercicio 2 (propuesto): muestree x(t) = cos(2*pi*1000*t) a fs = 8000 Hz
# (como en voz) y verifique que w0 = pi/4 rad/muestra.

plt.show()
