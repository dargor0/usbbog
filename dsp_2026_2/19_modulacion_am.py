#!/usr/bin/env python3
"""19_modulacion_am.py

Tema 3 - Modulacion y demodulacion AM.
Ejecutar:  python3 19_modulacion_am.py

Referencias a las laminas del Tema 3:
  - El espectro de la senal AM muestra portadora (fc) y bandas laterales
    (fc +/- fm).
  - Demodulacion coherente: multiplicar por la portadora y filtrar el paso
    bajo para recuperar la senal modulante.

Senal AM:  x(t) = (1 + mu*cos(2*pi*fm*t))*cos(2*pi*fc*t).
"""

import matplotlib.pyplot as plt
import numpy as np

fc = 100e3     # portadora [Hz]
fm = 1e3       # modulante [Hz]
fs = 400e3     # frecuencia de muestreo [Hz]
N = 4000       # N tal que fc y fm caen en bins exactos
mu = 0.5       # indice de modulacion
t = np.arange(N)/fs

# ------------------- modulacion -------------------
m = np.cos(2*np.pi*fm*t)                     # senal modulante
x = (1 + mu*m) * np.cos(2*np.pi*fc*t)        # senal AM

X = np.fft.fft(x)
f = np.arange(N)*fs/N
Xm = np.abs(X)*2/N

print("="*58)
print("MODULACION AM")
print("="*58)
print("fc = %.0f Hz, fm = %.0f Hz, mu = %.1f" % (fc, fm, mu))
print("espectro: picos en fc, fc-fm y fc+fm (%.0f, %.0f, %.0f Hz)"
      % (fc, fc-fm, fc+fm))

# ------------------- demodulacion (simple) -------------------
xr = x * np.cos(2*np.pi*fc*t)          # mezcla con la portadora
Xr = np.fft.fft(xr)
Xrm = np.abs(Xr)*2/N                   # espectro desplazado

print("\nDEMODULACION (simple): ESPECTRO DESPLAZADO")
print("="*58)
print("tras mezclar con la portadora, el espectro se desplaza a banda base")
print("(picos en 0 y +/-fm) y a 2fc (2fc +/- fm).")

# ---------- Una sola figura con los 3 plots ----------
plt.figure(figsize=(10, 10))

# 1) AM en tiempo (primeros 3 ms)
plt.subplot(3, 1, 1)
idx = t <= 3e-3
plt.plot(t[idx]*1e3, x[idx])
plt.title('Señal AM (temporal)'); plt.xlabel('t [ms]'); plt.grid()

# 2) AM en frecuencia [0, fs/2]
plt.subplot(3, 1, 2)
plt.plot(f[:N//2 + 1]/1e3, Xm[:N//2 + 1])
plt.title('Espectro AM (portadora + bandas laterales)')
plt.xlabel('f [kHz]'); plt.grid()
plt.axvline(fc/1e3, color='r', ls='--', alpha=0.5, label='fc')
plt.axvline((fc-fm)/1e3, color='g', ls=':', alpha=0.5, label='fc±fm')
plt.axvline((fc+fm)/1e3, color='g', ls=':', alpha=0.5)
plt.legend()

# 3) Demodulacion en frecuencia [0, fs), incluye 2fc
plt.subplot(3, 1, 3)
plt.plot(f/1e3, Xrm)
plt.title('Espectro tras mezclar: baseband, 2fc y espejo')
plt.xlabel('f [kHz]'); plt.grid()
plt.axvline(0, color='b', ls='--', alpha=0.3)
plt.axvline(fm/1e3, color='b', ls=':', alpha=0.3)
plt.axvline(2*fc/1e3, color='r', ls='--', alpha=0.5, label='2fc')
plt.axvline((2*fc-fm)/1e3, color='g', ls=':', alpha=0.5, label='2fc±fm')
plt.axvline((2*fc+fm)/1e3, color='g', ls=':', alpha=0.5)
plt.axvline(fs/1e3, color='k', ls='-', alpha=0.2)
plt.text(fs/2/1e3, plt.ylim()[1]*0.9, 'fs/2', ha='center', fontsize=8, color='k', alpha=0.4)
plt.legend()

plt.tight_layout(); plt.show()
