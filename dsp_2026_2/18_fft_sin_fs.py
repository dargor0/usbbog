#!/usr/bin/env python3
"""18_fft_sin_fs.py

Tema 3 - FFT con y sin frecuencia de muestreo.
Ejecutar:  python3 18_fft_sin_fs.py

Referencias a las laminas del Tema 3:
  - "Interpretacion de las frecuencias (bins)":
        sin fs: bins k=0..N-1 (o omega_k = 2*pi*k/N);
        con fs: f_k = k*fs/N (Hz).
"""

import matplotlib.pyplot as plt
import numpy as np

fs = 8000.0
f0 = 1000.0
N = 64
n = np.arange(N)
x = np.sin(2*np.pi*f0*n/fs)

X = np.fft.fft(x)

k = np.arange(N)                 # bins (sin fs)
f = k*fs/N                       # frecuencias reales (con fs)
w = 2*np.pi*k/N                  # frecuencias normalizadas (rad/muestra)

kmax = np.argmax(np.abs(X[:N//2]))
print("="*58)
print("FFT CON Y SIN FRECUENCIA DE MUESTREO")
print("="*58)
print("pico en el bin k = %d" % kmax)
print("sin fs:  omega = %.3f rad/muestra  (o bin %d)" % (w[kmax], kmax))
print("con fs:  f = %.1f Hz  (esperado %.0f Hz)" % (f[kmax], f0))

plt.figure(figsize=(10, 8))
plt.subplot(3,1,1); plt.stem(k, np.abs(X), basefmt=" ")
plt.title('Eje en bins k (sin fs): 0..N-1'); plt.xlabel('k'); plt.grid()
plt.subplot(3,1,2); plt.stem(w, np.abs(X), basefmt=" ")
plt.title(r'Eje en $\omega$ (rad/muestra): $\omega_k = 2\pi k/N$'); plt.xlabel(r'$\omega$ [rad/muestra]'); plt.grid()
plt.subplot(3,1,3); plt.stem(f, np.abs(X), basefmt=" ")
plt.title('Eje en Hz (con fs): $f_k = k\\cdot f_s/N$'); plt.xlabel('f [Hz]'); plt.grid()
plt.tight_layout(); plt.show()
