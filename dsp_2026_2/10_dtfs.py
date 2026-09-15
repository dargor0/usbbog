#!/usr/bin/env python3
"""10_dtfs.py

Tema 2 - Series de Fourier discretas (DTFS).
Ejecutar:  python3 10_dtfs.py

Referencias a las láminas del Tema 2:
  - "Señales discretas: la DTFS en detalle":
        síntesis:  x[n] = sum_{k=0}^{N-1} c_k e^{j2pi k n / N}
        análisis:  c_k = (1/N) sum_{n=0}^{N-1} x[n] e^{-j2pi k n / N}
  - "Ejemplo: DTFS de una señal discreta": x[n]=[1,2,1,2] (N=4) ->
        c0=1.5, c1=0, c2=-0.5, c3=0.
"""

import matplotlib.pyplot as plt
import numpy as np

N = 4
x = np.array([1.0, 2.0, 1.0, 2.0])   # un periodo


def dtfs_analisis(xn):
    """Coeficientes c_k = (1/N) sum x[n] e^{-j2pi k n / N}."""
    Nn = len(xn)
    k = np.arange(Nn)
    n = np.arange(Nn)
    # matriz exp(-j2pi kn/N), luego promedio sobre n
    W = np.exp(-1j * 2 * np.pi * np.outer(k, n) / Nn)
    return W @ xn / Nn


def dtfs_sintesis(ck, nn):
    """Reconstruye x[n] = sum c_k e^{j2pi k n / N}."""
    Nn = len(ck)
    k = np.arange(Nn)
    return np.sum(ck[:, None] * np.exp(1j * 2 * np.pi * np.outer(k, nn) / Nn),
                  axis=0)


print("=" * 58)
print("SERIES DE FOURIER DISCRETAS (DTFS)")
print("=" * 58)

ck = dtfs_analisis(x)

print(f"\n[1] x[n] = {x.tolist()}  (periodo N = {N})")
print("\n    k |  c_k")
for k in range(N):
    print(f"    {k} | {ck[k].real:.3f}{ck[k].imag:+.3f}j")

print("\n[2] Verificaciones:")
print(f"    c_0 = {ck[0].real:.2f} (valor medio, debe ser 1.5)")
print(f"    |c_2| = {abs(ck[2]):.2f} (debe ser 0.5)")
print(f"    c_1 = {abs(ck[1]):.2f}, c_3 = {abs(ck[3]):.2f} (deben ser 0)")

# Sintesis: reconstruir y verificar
n = np.arange(N)
x_rec = dtfs_sintesis(ck, n)
print(f"\n[3] Sintesis: x_rec = {np.round(x_rec.real, 6).tolist()}")
print(f"    Error de reconstruccion = {np.max(np.abs(x_rec - x)):.2e}")

# Periodicidad del espectro: c_{k+N} = c_k (misma senal de periodo N=4)
def ck_k(k, xn):
    """Coeficiente c_k con el analisis DTFS para cualquier k entero."""
    Nn = len(xn)
    n = np.arange(Nn)
    return np.sum(xn * np.exp(-1j * 2 * np.pi * k * n / Nn)) / Nn

ck_ext = np.array([ck_k(k, x) for k in range(8)])
print(f"\n[4] Periodicidad (misma senal N=4, k = 0..7):")
for k in range(4):
    print(f"    c_{k+4} = {ck_ext[k+4].real:+.3f}{ck_ext[k+4].imag:+.3f}j "
          f"vs c_{k} = {ck[k].real:+.3f}{ck[k].imag:+.3f}j")
print(f"    (c_{k+4} debe repetir c_{k})")

# Graficas: magnitud y fase de un periodo
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
ax1.stem(np.arange(N), np.abs(ck), basefmt=" ")
ax1.set_title("DTFS de x[n]=[1,2,1,2]: |c_k|")
ax1.set_xlabel("k"); ax1.set_ylabel("|c_k|"); ax1.grid(alpha=0.3)
ax2.stem(np.arange(N), np.angle(ck), basefmt=" ")
ax2.set_title("DTFS: fase ang(c_k)")
ax2.set_xlabel("k"); ax2.set_ylabel("ang(c_k) [rad]"); ax2.grid(alpha=0.3)
fig.tight_layout()

# ---------------------------------------------------------------------------
# Ejercicios propuestos
# ---------------------------------------------------------------------------
print("\n[ejercicios propuestos]")
print("  E1. Use x[n] = [1, 0, -1, 0] (N=4): calcule c_k y observe que solo")
print("      sobrevive la frecuencia k=1 (un tono).")
print("  E2. Verifique el teorema de Parseval discreto: sum |c_k|^2 =")
print("      (1/N) sum |x[n]|^2.")
print("  E3. Cambie N (p. ej., N=8 con una onda discreta) y compruebe que")
print("      hay exactamente N coeficientes independientes.")
print("  E4. Grafique el espectro en k = -N/2 .. N/2 (simetria hermitiana)")
print("      para una x[n] real.")

plt.show()
