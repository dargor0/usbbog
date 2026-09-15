#!/usr/bin/env python3
"""17_fft_no_potencia2.py

Tema 3 - FFT con N que NO es potencia de 2.
Ejecutar:  python3 17_fft_no_potencia2.py

Referencias a las laminas del Tema 3:
  - La FFT puede calcular N arbitrario (los algoritmos mas rapidos usan
    potencias de 2, pero numpy/scipy manejan cualquier N).
  - Se compara con relleno de ceros (zero-padding) a la siguiente potencia de 2.
"""

import matplotlib.pyplot as plt
import numpy as np

fs = 8000.0
f0 = 1000.0
N = 1000            # NO es potencia de 2
n = np.arange(N)
x = np.sin(2*np.pi*f0*n/fs)

X = np.fft.fft(x)          # funciona con N=1000
N2 = 1 << int(np.ceil(np.log2(N)))   # siguiente potencia de 2 (1024)
X2 = np.fft.fft(x, N2)     # relleno con ceros

f1 = np.arange(N)*fs/N
f2 = np.arange(N2)*fs/N2

print("="*58)
print("FFT CON N NO POTENCIA DE 2")
print("="*58)
print("N = %d (no potencia de 2); siguiente potencia = %d" % (N, N2))
print("resolucion sin padding: df = %.2f Hz" % (fs/N))
print("resolucion con padding: df = %.2f Hz" % (fs/N2))

# Indices para el rango 975–1025 Hz
idx1 = np.where((f1 >= 975) & (f1 <= 1025))[0]
idx2 = np.where((f2 >= 975) & (f2 <= 1025))[0]

plt.figure()
plt.subplot(2,1,1); plt.plot(f1[idx1], np.abs(X[idx1])*2/N)
plt.title('fft(x) con N=%d' % N); plt.xlabel('f [Hz]'); plt.xlim(975, 1025); plt.grid()
plt.subplot(2,1,2); plt.plot(f2[idx2], np.abs(X2[idx2])*2/N)
plt.title('fft(x, N2=%d) con zero-padding' % N2); plt.xlabel('f [Hz]'); plt.xlim(975, 1025); plt.grid()
plt.tight_layout(); plt.show()
