#!/usr/bin/env python3
"""13_fft_basico.py

Tema 3 - Uso basico de la FFT.
Ejecutar:  python3 13_fft_basico.py

Referencias a las laminas del Tema 3:
  - "DFT: definicion y propiedades"
  - "Interpretacion de las frecuencias (bins)": f_k = k*f_s/N
"""

import matplotlib.pyplot as plt
import numpy as np

fs = 8000.0          # frecuencia de muestreo [Hz]
f0 = 1000.0          # frecuencia del seno [Hz]
N = 1024             # numero de muestras (potencia de 2)
n = np.arange(N)
x = np.sin(2*np.pi*f0*n/fs)   # seno muestreado

X = np.fft.fft(x)
f = np.arange(N)*fs/N         # eje de frecuencia [Hz] (rango completo)

print("="*58)
print("USO BASICO DE LA FFT")
print("="*58)
print("fs = %.0f Hz, f0 = %.0f Hz, N = %d" % (fs, f0, N))
kmax = np.argmax(np.abs(X))
print("pico en el bin %d -> %.0f Hz (esperado %.0f Hz)" % (kmax, f[kmax], f0))
print("energia (Parseval): tiempo %.3f vs. frecuencia %.3f"
      % (np.sum(x**2), np.sum(np.abs(X)**2)/N))

plt.figure(figsize=(10, 6))

plt.subplot(2, 2, 1)
plt.stem(n, x, basefmt=" ")
plt.title('x[n] = seno de 1 kHz')
plt.xlabel('n')
plt.grid(True)

plt.subplot(2, 2, 2)
plt.stem(f, np.abs(X)*2/N, basefmt=" ")
plt.title('Espectro de magnitud (rango completo)')
plt.xlabel('f [Hz]')
plt.grid(True)

plt.subplot(2, 2, 3)
plt.stem(f, np.real(X)*2/N, basefmt=" ")
plt.title('Parte real de X[k]')
plt.xlabel('f [Hz]')
plt.grid(True)

plt.subplot(2, 2, 4)
plt.stem(f, np.imag(X)*2/N, basefmt=" ")
plt.title('Parte imaginaria de X[k]')
plt.xlabel('f [Hz]')
plt.grid(True)

plt.tight_layout()
plt.show()
