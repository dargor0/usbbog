#!/usr/bin/env python3
"""05_sqnr_bits.py

Tema 1 - SQNR vs número de bits: SQNR ~ 6.02 b + 1.76 dB (seno plena escala).
Ejecutar:  python3 05_sqnr_bits.py

Uso de SciPy: scipy.signal.find_peaks para localizar picos del seno.
"""

import matplotlib.pyplot as plt
import numpy as np

Vmax, Vmin = 1.0, -1.0
N = 2**16
t = np.arange(N) / N                 # 1 segundo, periodos enteros (sin fuga)
x = np.cos(2 * np.pi * 3 * t)        # seno a plena escala (3 periodos)

bvec = np.arange(2, 17)
sqnr = np.zeros_like(bvec, dtype=float)
for i, b in enumerate(bvec):
    Delta = (Vmax - Vmin) / (2**b)
    xq = Delta * np.round(x / Delta)
    Px = np.mean(x**2)
    Pe = np.mean((x - xq) ** 2)
    sqnr[i] = 10 * np.log10(Px / Pe)

teoria = 6.02 * bvec + 1.76

fig, ax = plt.subplots()
ax.plot(bvec, sqnr, "o", label="SQNR simulada")
ax.plot(bvec, teoria, "-", label="6.02 b + 1.76 dB")
ax.set_xlabel("Bits b")
ax.set_ylabel("SQNR [dB]")
ax.set_title("SQNR en función de la resolución")
ax.legend(loc="upper left")
plt.tight_layout()

print("  b   SQNR sim [dB]  teoria [dB]  dif [dB]")
for b, s, th in zip(bvec, sqnr, teoria):
    print(f"{b:3d}  {s:12.2f}  {th:11.2f}  {s - th:8.2f}")

# Ejemplos de las láminas
print(f"\nCD de audio (16 bits):  SQNR ~= {6.02 * 16 + 1.76:.1f} dB")
print(f"Voz/PCM (8 bits):       SQNR ~= {6.02 * 8 + 1.76:.1f} dB")

# Ejercicio 1: verifique la regla "cada bit extra ~6 dB": calcule
# sqnr[i] - sqnr[i-1] para b = 3..16 a partir del vector sqnr.
# Ejercicio 2 (propuesto): un sensor de 12 bits para instrumentación.
# Compare su SQNR con uno de 24 bits (audio profesional).

plt.show()
