#!/usr/bin/env python3
"""21_dtmf.py

Tema 3 - Identificacion de tonos DTMF con la FFT.
Ejecutar:  python3 21_dtmf.py

Referencias a las laminas del Tema 3:
  - La FFT permite identificar las dos frecuencias de un tono DTMF.
  - Tabla DTMF: filas 697,770,852,941 Hz; columnas 1209,1336,1477,1633 Hz.
"""

import matplotlib.pyplot as plt
import numpy as np

fs = 8000.0
N = 800
t = np.arange(N)/fs

fila = 770.0      # tono '5': fila 770 Hz
columna = 1336.0  # tono '5': columna 1336 Hz
x = np.sin(2*np.pi*fila*t) + np.sin(2*np.pi*columna*t)

X = np.fft.fft(x)
f = np.arange(N)*fs/N
Xm = np.abs(X[:N//2])

# las dos frecuencias mas grandes
idx = np.argsort(Xm)[-2:][::-1]
frecs = np.sort(f[idx])
print("="*58)
print("IDENTIFICACION DE TONOS DTMF")
print("="*58)
print("tono generado: fila %.0f + columna %.0f Hz" % (fila, columna))
print("frecuencias detectadas: %.0f y %.0f Hz" % (frecs[0], frecs[1]))

filas = [697, 770, 852, 941]
cols  = [1209, 1336, 1477, 1633]
teclas = [['1','2','3'], ['4','5','6'], ['7','8','9'], ['*','0','#']]
def cerca(a, lista):
    return min(lista, key=lambda v: abs(v-a))
fr = cerca(frecs[0], filas) if any(abs(frecs[0]-f)<50 for f in filas) else None
co = cerca(frecs[1], cols) if any(abs(frecs[1]-c)<50 for c in cols) else None
if fr is not None and co is not None:
    print("tecla detectada: %s" % teclas[filas.index(fr)][cols.index(co)])
else:
    print("no se pudo mapear a una tecla (revise el umbral)")

plt.figure()
plt.plot(f[:N//2], Xm)
plt.axvline(fila, color='r', ls='--'); plt.axvline(columna, color='g', ls='--')
plt.title('Espectro del tono DTMF (dos picos)'); plt.xlabel('f [Hz]'); plt.grid()
plt.tight_layout(); plt.show()
