#!/usr/bin/env python3
"""20_ruido_blanco.py

Tema 3 - Espectro del ruido blanco.
Ejecutar:  python3 20_ruido_blanco.py

Referencias a las laminas del Tema 3:
  - "DTFT" y "DFT": la densidad espectral de potencia; el ruido blanco tiene
    un espectro aproximadamente plano (todas las frecuencias con igual
    potencia media).
"""

import matplotlib.pyplot as plt
import numpy as np

np.random.seed(0)
N = 4096
x = np.random.randn(N)          # ruido blanco (media 0, varianza 1)

X = np.fft.fft(x)
P = np.abs(X)**2 / N            # densidad espectral de potencia
f = np.arange(N)*2/N - 1        # frecuencia normalizada en [-1, 1)

print("="*58)
print("ESPECTRO DEL RUIDO BLANCO")
print("="*58)
print("potencia media (esperada ~1) = %.3f" % np.mean(x**2))
print("media del espectro de potencia = %.3f" % np.mean(P))

plt.figure()
plt.subplot(2,1,1); plt.plot(x[:512]); plt.title('Ruido blanco (temporal)'); plt.grid()
plt.subplot(2,1,2); plt.plot(f, P)
plt.title('Densidad espectral de potencia (aprox. plana)')
plt.xlabel('f normalizada'); plt.ylim(0, 6); plt.grid()
plt.tight_layout(); plt.show()
