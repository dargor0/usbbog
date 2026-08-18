#!/usr/bin/env python3
"""03_cuantizacion.py

Tema 1 - Cuantización uniforme (conversión analógico-digital).
Ejecutar:  python3 03_cuantizacion.py

Uso de SciPy: scipy.signal.sawtooth() para una rampa y ver la escalera.
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import sawtooth

Vmax, Vmin = 1.0, -1.0
b = 4                                        # bits por muestra
Delta = (Vmax - Vmin) / (2**b)
print(f"b = {b} bits -> 2^b = {2**b} niveles, Delta = {Delta:.4f}")

fs, f0 = 100, 2
t = np.arange(fs) / fs
x = 0.9 * np.cos(2 * np.pi * f0 * t)         # señal de entrada (0.9 de escala)

xq = Delta * np.round(x / Delta)             # cuantizador uniforme por redondeo

fig, ax = plt.subplots()
ax.plot(t, x, "b", label="Original x[n]")
ax.step(t, xq, "r", where="post", linewidth=1.5, label=r"Cuantizada $x_q[n]$")
ax.set_title(f"Cuantización uniforme, b = {b} bits")
ax.set_xlabel("t [s]")
ax.set_ylabel("Amplitud")
ax.legend()
ax.set_ylim(-1.1, 1.1)
plt.tight_layout()

# Ejercicio 1: repita la gráfica para b = 1, 3, 8 y 16. Con b = 1 solo hay
# 2 niveles (escalera gruesa); al crecer b la escalera se acerca a la señal.
# Calcule Delta en cada caso.
# Ejercicio 2 (propuesto): un ADC de 12 bits con Vmin = 0 V y Vmax = 5 V.
# Calcule Delta (mV) y el número de niveles. Verifique Delta = 5/4096 ~ 1.22 mV.

# Extra: escalera sobre una rampa (señal triangular), útil para apreciar los
# niveles de cuantización.
t2 = np.arange(200) / 200
ramp = sawtooth(2 * np.pi * 2 * t2, width=0.5)
fig2, ax2 = plt.subplots()
ax2.plot(t2, ramp, "b", lw=0.8)
ax2.step(t2, Delta * np.round(ramp / Delta), "r", where="post", lw=1.2)
ax2.set_title(f"Escalera de cuantización sobre rampa, b = {b} bits")
ax2.set_xlabel("t [s]")
ax2.set_ylabel("Amplitud")
plt.tight_layout()

plt.show()
