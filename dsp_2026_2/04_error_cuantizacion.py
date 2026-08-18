#!/usr/bin/env python3
"""04_error_cuantizacion.py

Tema 1 - Error de cuantización: modelo de ruido uniforme.
Ejecutar:  python3 04_error_cuantizacion.py

Uso de SciPy: scipy.stats.uniform para comparar con la distribución teórica.
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import uniform

Vmax, Vmin = 1.0, -1.0
b = 8
Delta = (Vmax - Vmin) / (2**b)

rng = np.random.default_rng(0)
N = 20000
x = 0.9 * (2 * rng.random(N) - 1)       # señal uniforme en [-0.9, 0.9]
xq = Delta * np.round(x / Delta)
e = x - xq

fig, ax = plt.subplots()
ax.hist(e, bins=50, density=True, alpha=0.7, label="Error empírico")
xpdf = np.linspace(-Delta, Delta, 200)
ax.plot(xpdf, uniform.pdf(xpdf, loc=-Delta / 2, scale=Delta), "r--",
        label=r"Uniforme en $[-\Delta/2, \Delta/2]$")
ax.set_title("Histograma del error de cuantización")
ax.set_xlabel("e[n]")
ax.set_ylabel("Densidad")
ax.legend()
plt.tight_layout()

rms_e = np.sqrt(np.mean(e**2))
print(f"b = {b} bits, Delta = {Delta:.5f}")
print(f"RMS empírico del error: {rms_e:.6f}")
print(f"Teórico Delta/sqrt(12): {Delta / np.sqrt(12):.6f}")

# Ejercicio 1: repita con b = 4 y b = 12; compare el RMS empírico con
# Delta/sqrt(12) y verifique que el error queda acotado entre -Delta/2 y
# Delta/2.
# Ejercicio 2 (propuesto): use un seno a plena escala (x = 0.9*cos(2*pi*2*t))
# en vez de uniforme. El histograma del error deja de ser plano: explique por
# qué (la densidad de muestras no es uniforme cerca de los extremos del seno).

plt.show()
