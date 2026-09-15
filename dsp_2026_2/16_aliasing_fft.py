#!/usr/bin/env python3
"""16_aliasing_fft.py

Tema 3 - Aliasing observado con la FFT.
Compara la misma señal muestreada por debajo y por encima de Nyquist.
Ejecutar:  python3 16_aliasing_fft.py

Referencias:
  - Tema 1: muestreo y Nyquist (fs >= 2*fmax).
"""

import matplotlib.pyplot as plt
import numpy as np

f0 = 700.0        # frecuencia del seno [Hz]
fs_low = 1000.0   # baja fs: f0 > fs/2 -> aliasing
fs_high = 2000.0  # alta fs: f0 < fs/2 -> sin aliasing
N = 512

# ---------- Muestras con fs baja (aliasing) ----------
n_low = np.arange(N)
t_low = n_low / fs_low
x_low = np.sin(2 * np.pi * f0 * t_low)

# ---------- Muestras con fs alta (sin aliasing) ----------
n_high = np.arange(N)
t_high = n_high / fs_high
x_high = np.sin(2 * np.pi * f0 * t_high)

# ---------- FFTs (rango completo) ----------
X_low = np.fft.fft(x_low)
X_high = np.fft.fft(x_high)
f_low = np.arange(N) * fs_low / N
f_high = np.arange(N) * fs_high / N

falias = abs(f0 - fs_low)

print("=" * 60)
print("ALIASING: COMPARACION EN TIEMPO Y FRECUENCIA")
print("=" * 60)
print("f0 = %.0f Hz" % f0)
print("fs_baja = %.0f Hz (fs/2 = %.0f) -> f0 > fs/2  =>  ALIASING"
      % (fs_low, fs_low / 2))
print("fs_alta = %.0f Hz (fs/2 = %.0f) -> f0 < fs/2  =>  SIN ALIASING"
      % (fs_high, fs_high / 2))
print("alias esperado: |f0 - fs_baja| = %.0f Hz" % falias)

kmax_low = np.argmax(np.abs(X_low))
kmax_high = np.argmax(np.abs(X_high))
print("pico con fs_baja en %.0f Hz" % f_low[kmax_low])
print("pico con fs_alta en %.0f Hz" % f_high[kmax_high])

# ---------- Señal continua de referencia (fs = 10 kHz) ----------
fs_ref = 10000.0
t_ref = np.arange(0, max(t_low[-1], t_high[-1]) + 1/fs_ref, 1/fs_ref)
x_ref = np.sin(2 * np.pi * f0 * t_ref)
x_alias = -np.sin(2 * np.pi * falias * t_ref)  # fase invertida 180° para alinear con las muestras

# ---------- Graficas ----------
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Tiempo: fs baja
ax = axes[0, 0]
ax.plot(t_ref, x_ref, color='gray', alpha=0.5, label='continua (fs = 10 kHz)')
ax.plot(t_ref, x_alias, color='orange', alpha=0.5, label='alias (%.0f Hz)' % falias)
ax.stem(t_low, x_low, basefmt=" ", linefmt='C0-', markerfmt='C0o')
ax.set_title('Tiempo: fs = %.0f Hz (ALIASING)' % fs_low)
ax.set_xlabel('t [s]')
ax.set_xlim(0, 0.01)
ax.legend()
ax.grid(True)

# Tiempo: fs alta
ax = axes[0, 1]
ax.plot(t_ref, x_ref, color='gray', alpha=0.5, label='continua (fs = 10 kHz)')
ax.stem(t_high, x_high, basefmt=" ", linefmt='C1-', markerfmt='C1o')
ax.set_title('Tiempo: fs = %.0f Hz (sin aliasing)' % fs_high)
ax.set_xlabel('t [s]')
ax.set_xlim(0, 0.01)
ax.legend()
ax.grid(True)

# Frecuencia: fs baja
ax = axes[1, 0]
ax.stem(f_low, np.abs(X_low) * 2 / N, basefmt=" ")
ax.axvline(f0, color='r', ls='--', label='f0 real = %.0f Hz' % f0)
ax.axvline(falias, color='g', ls=':', label='alias = %.0f Hz' % falias)
ax.set_title('Espectro: fs = %.0f Hz' % fs_low)
ax.set_xlabel('f [Hz]')
ax.legend()
ax.grid(True)

# Frecuencia: fs alta
ax = axes[1, 1]
ax.stem(f_high, np.abs(X_high) * 2 / N, basefmt=" ")
ax.axvline(f0, color='r', ls='--', label='f0 = %.0f Hz' % f0)
ax.set_title('Espectro: fs = %.0f Hz' % fs_high)
ax.set_xlabel('f [Hz]')
ax.legend()
ax.grid(True)

plt.tight_layout()
plt.show()
