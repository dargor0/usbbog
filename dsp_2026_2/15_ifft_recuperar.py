#!/usr/bin/env python3
"""15_ifft_recuperar.py

Tema 3 - Recuperar la senal original con la IFFT.
Ejecutar:  python3 15_ifft_recuperar.py

Referencias a las laminas del Tema 3:
  - "DFT: definicion y propiedades": la DFT es una transformada invertible
    (analisis y sintesis).
"""

import matplotlib.pyplot as plt
import numpy as np

N = 256
n = np.arange(N)
x = np.cos(2*np.pi*3*n/N) + 0.5*np.sin(2*np.pi*10*n/N)

X = np.fft.fft(x)
x2 = np.fft.ifft(X)

err = np.max(np.abs(x - x2))
print("="*58)
print("RECUPERAR LA SENAL CON LA IFFT")
print("="*58)
print("error maximo |x[n] - ifft(fft(x))| = %.3e" % err)
print("la parte imaginaria de la recuperacion es ~0: %.3e"
      % np.max(np.abs(np.imag(x2))))

plt.figure()
plt.plot(n, x, 'b-', label='original')
plt.plot(n, np.real(x2), 'r--', label='ifft(fft(x))')
plt.legend(); plt.title('Original y recuperada (se superponen)'); plt.grid()
plt.tight_layout(); plt.show()
