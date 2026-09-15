#!/usr/bin/env python3
"""14_fft_vs_fftshift.py

Tema 3 - FFT vs. fftshift (espectro de 0..fs vs. centrado en 0).
Ejecutar:  python3 14_fft_vs_fftshift.py

Referencias a las laminas del Tema 3:
  - "Espectro simetrico: centrado en 0 vs. 0-N"
  - La segunda mitad de la FFT corresponde a frecuencias negativas.
"""

import matplotlib.pyplot as plt
import numpy as np

fs = 8000.0
f0 = 1000.0
N = 1024
n = np.arange(N)
x = np.sin(2*np.pi*f0*n/fs)

X = np.fft.fft(x)
Xc = np.fft.fftshift(X)

f1 = np.arange(N)*fs/N            # 0 .. fs
f2 = (np.arange(N) - N//2)*fs/N   # -fs/2 .. fs/2 (centrado)

print("="*58)
print("FFT vs. FFT-SHIFT")
print("="*58)
k1 = np.argmax(np.abs(X));        print("fft:      pico en bin %3d -> %7.1f Hz" % (k1, f1[k1]))
k2 = np.argmax(np.abs(Xc));       print("fftshift: pico en bin %3d -> %7.1f Hz" % (k2, f2[k2]))

plt.figure()
plt.subplot(2,1,1); plt.plot(f1, np.abs(X))
plt.title('fft(x): bins 0..N-1 (frecuencias 0..fs)'); plt.xlabel('f [Hz]'); plt.grid()
plt.subplot(2,1,2); plt.plot(f2, np.abs(Xc))
plt.title('fftshift(fft(x)): centrado en 0 (frecuencias -fs/2..fs/2)')
plt.xlabel('f [Hz]'); plt.grid()
plt.tight_layout(); plt.show()
