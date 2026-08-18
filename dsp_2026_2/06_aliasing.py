#!/usr/bin/env python3
"""06_aliasing.py

Tema 1 - Aliasing: muestreo por debajo de Nyquist (fs < 2 f0).
Ejecutar:  python3 06_aliasing.py

Uso de SciPy: scipy.fft.fft para ver el alias en el espectro muestreado.
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq

f0 = 100.0
t = np.arange(0, 0.1, 1e-5)

# --- Caso 1: muestreo insuficiente (fs < 2 f0) ---
fs = 70.0                     # 70 < 200 Hz -> hay aliasing
Ts = 1.0 / fs
n = np.arange(0, int(0.1 / Ts) + 1)
tn = n * Ts

xt = np.cos(2 * np.pi * f0 * t)
xn = np.cos(2 * np.pi * f0 * tn)
fa = abs(f0 - fs)             # primer alias

fig, ax = plt.subplots()
ax.plot(t, xt, "b")
ax.stem(tn, xn, "r", basefmt=" ")
ax.plot(t, np.cos(2 * np.pi * fa * t), "g--", linewidth=1.5)
ax.set_title(f"Muestreo insuficiente: fs = {fs:.0f} Hz < 2 f0 = {2 * f0:.0f} Hz")
ax.set_xlabel("t [s]")
ax.set_ylabel("Amplitud")
ax.legend([r"$x(t)=\cos(2\pi\,100 t)$", f"Muestras fs = {fs:.0f} Hz",
           f"Alias {fa:.0f} Hz"])
ax.set_ylim(-1.3, 1.3)
plt.tight_layout()

print(f"fs = {fs:.0f} Hz < 2*f0 = {2 * f0:.0f} Hz: aparece un alias en {fa:.0f} Hz.")

# Espectro de las muestras (el alias se ve como un pico en fa)
Xk = fft(xn)
freq = fftfreq(len(xn), Ts)
fig2, ax2 = plt.subplots()
ax2.plot(freq[: len(xn) // 2], np.abs(Xk[: len(xn) // 2]))
ax2.set_title("Espectro de las muestras (fs = 70 Hz)")
ax2.set_xlabel("Frecuencia [Hz]")
ax2.set_xlim(0, 120)
plt.tight_layout()

# --- Caso 2: muestreo correcto (fs > 2 f0) ---
fs2 = 250.0
Ts2 = 1.0 / fs2
n2 = np.arange(0, int(0.1 / Ts2) + 1)
tn2 = n2 * Ts2
xn2 = np.cos(2 * np.pi * f0 * tn2)

fig3, ax3 = plt.subplots()
ax3.plot(t, xt, "b")
ax3.stem(tn2, xn2, "r", basefmt=" ")
ax3.set_title(f"Muestreo correcto: fs = {fs2:.0f} Hz > 2 f0 = {2 * f0:.0f} Hz")
ax3.set_xlabel("t [s]")
ax3.set_ylabel("Amplitud")
ax3.legend([r"$x(t)=\cos(2\pi\,100 t)$", f"Muestras fs = {fs2:.0f} Hz"])
ax3.set_ylim(-1.3, 1.3)
plt.tight_layout()

# Ejercicio 1: para f0 = 100 Hz pruebe fs = 80, 90, 150, 180 y calcule
# fa = abs(f0 - fs) en cada caso; compruebe que las muestras "caminan" sobre
# la coseno de frecuencia fa.
# Ejercicio 2 (propuesto): un audio con fmax = 20 kHz muestreado a
# fs = 44.1 kHz cumple fs > 2*fmax. Repita con fs = 32 kHz y explique por qué
# el resultado cambia.

plt.show()
