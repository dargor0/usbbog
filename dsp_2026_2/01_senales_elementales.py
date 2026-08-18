#!/usr/bin/env python3
"""01_senales_elementales.py

Tema 1 - Señales elementales discretas: impulso, escalón, exponencial y seno.
Ejecutar:  python3 01_senales_elementales.py

Referencias a las láminas del Tema 1:
  - "Señales elementales": delta[n], u[n], a^n u[n], A cos(w0 n + phi)
  - "Importancia del impulso": x[n] = sum_k x[k] delta[n-k]

Uso de SciPy: unit_impulse() para el impulso y heaviside() para el escalón.
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import unit_impulse

n = np.arange(-5, 16)

# Impulso: delta[n] = 1 si n == 0
delta = unit_impulse(len(n), idx=5)  # idx=5 -> n == 0 en este rango

# Escalón: u[n] = 1 si n >= 0
u = np.heaviside(n, 0)

# Exponencial: a^n u[n]
a = 0.85
xexp = a**n * u

# Seno: A cos(w0 n + phi)
A, w0, phi = 1.0, 0.5 * np.pi, 0.0
xseno = A * np.cos(w0 * n + phi)

fig, axes = plt.subplots(2, 2)
fig.suptitle("Señales elementales discretas")
axes[0, 0].stem(n, delta)
axes[0, 0].set_title(r"Impulso $\delta[n]$")
axes[0, 1].stem(n, u)
axes[0, 1].set_title(r"Escalón $u[n]$")
axes[1, 0].stem(n, xexp)
axes[1, 0].set_title(rf"Exponencial $a^n u[n]$, a={a}")
axes[1, 1].stem(n, xseno)
axes[1, 1].set_title(r"Seno $A\cos(\omega_0 n + \phi)$")
for ax in axes.ravel():
    ax.set_xlabel("n")
plt.tight_layout()

# Ejercicio 1: descomposición en impulsos
# Dada la secuencia x = [1 2 3 4] definida para n = 0..3, exprésela como
# x[n] = sum_k x[k] delta[n-k] y grafique los impulsos ponderados.
x = np.array([1, 2, 3, 4])
nsup = np.arange(-5, 6)
xr = np.zeros_like(nsup, dtype=float)
for k, xk in enumerate(x):
    d = (nsup == k).astype(float)   # impulso desplazado delta[n-k]
    xr += xk * d                    # suma de impulsos escalados
plt.figure()
plt.stem(nsup, xr)
plt.title(r"$x[n] = \sum_k x[k]\,\delta[n-k]$")
plt.xlabel("n")
plt.tight_layout()

mask = (nsup >= 0) & (nsup <= 3)
print("x reconstruida en n=0..3:", xr[mask])

# Ejercicio 2 (propuesto): cambie a (0.5, 1.05, -0.8) y observe cómo cambia
# la exponencial: decrece, crece o alterna de signo.

plt.show()
