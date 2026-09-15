#!/usr/bin/env python3
"""08_coeficientes_fourier.py

Tema 2 - Coeficientes de las series de Fourier (CTFS) de una onda cuadrada.
Ejecutar:  python3 08_coeficientes_fourier.py

Referencias a las láminas del Tema 2:
  - "Cómo calcular los coeficientes (análisis)": c_k = (1/T) int_T x(t) e^{-j2pi k f0 t} dt
  - "Ejemplo: coeficientes de la onda cuadrada": solo armónicos impares,
    |c_k| = 2A/(pi |k|), fase -pi/2 (k>0) y +pi/2 (k<0).
  - "El espectro de magnitud y de fase" y "¿Por qué existen frecuencias negativas?".

La onda cuadrada impar de amplitud A:
    x(t) = +A  para 0 < t < T/2
    x(t) = -A  para T/2 < t < T

Uso de SciPy: scipy.integrate.quad para la integral de análisis (verificación numérica).
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad

A = 1.0       # amplitud de la onda
T = 1.0       # periodo [s]
f0 = 1.0 / T  # frecuencia fundamental [Hz]


def x_cuadrada(t):
    """Onda cuadrada impar de periodo T y amplitud A."""
    t_mod = np.mod(t, T)
    return np.where(t_mod < T / 2, A, -A)


def ck_analitico(k):
    """Coeficiente teorico: c_k = 2A/(j*pi*k) para k impar, 0 si k par."""
    if k == 0:
        return 0.0
    if k % 2 == 0:            # pares -> 0
        return 0.0
    return 2 * A / (1j * np.pi * k)


def ck_numerico(k):
    """Verificacion numerica de la integral de analisis."""
    real, _ = quad(lambda t: np.real(x_cuadrada(t) * np.exp(-1j * 2 * np.pi * k * f0 * t)),
                   0, T)
    imag, _ = quad(lambda t: np.imag(x_cuadrada(t) * np.exp(-1j * 2 * np.pi * k * f0 * t)),
                   0, T)
    return (real + 1j * imag) / T


print("=" * 62)
print("COEFICIENTES DE FOURIER DE LA ONDA CUADRADA")
print("=" * 62)

print(f"\n[1] Onda cuadrada: A = {A}, T = {T} s, f0 = {f0} Hz")
print("    (impar: solo senos, a_k = 0 y a_0 = 0)")

# Coeficientes para k = -9..9
k = np.arange(-9, 10)
c_ana = np.array([ck_analitico(kk) for kk in k])
c_num = np.array([ck_numerico(kk) for kk in k])

print("\n[2] Comparacion analitico vs numerico (integral):")
print("     k   | c_k analitico      | c_k numerico")
for kk, ca, cn in zip(k, c_ana, c_num):
    print(f"   {kk:3d} | {ca.real:+.4f}{ca.imag:+.4f}j | {cn.real:+.4f}{cn.imag:+.4f}j")

# Espectro de magnitud y fase (bilateral)
mag = np.abs(c_ana)
fase = np.angle(c_ana)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 7))
ax1.stem(k, mag, basefmt=" ")
ax1.set_title("Espectro de magnitud |c_k| (onda cuadrada)")
ax1.set_xlabel("k"); ax1.set_ylabel("|c_k|")
ax1.grid(alpha=0.3)
ax2.stem(k, fase, basefmt=" ")
ax2.set_title("Espectro de fase ang(c_k)")
ax2.set_xlabel("k"); ax2.set_ylabel("ang(c_k) [rad]")
ax2.set_ylim(-2, 2)
ax2.grid(alpha=0.3)
fig.tight_layout()

print("\n[3] Verificaciones:")
print(f"    |c_1| teorico = 2A/pi = {2*A/np.pi:.4f};  numerico = {abs(c_num[10]):.4f}")
print(f"    c_2 (par) = {abs(c_num[11]):.4f} (debe ser 0)")
print(f"    |c_-1| = |c_1| -> {abs(c_num[8]):.4f} vs {abs(c_num[10]):.4f} (simetria hermitiana)")

# ---------------------------------------------------------------------------
# Ejercicios propuestos
# ---------------------------------------------------------------------------
print("\n[ejercicios propuestos]")
print("  E1. Cambie la amplitud a A = 2 y verifique que |c_k| se duplica.")
print("  E2. Calcule la potencia: P = sum |c_k|^2 y compare con el valor")
print("      medio cuadratico de x(t) (teorema de Parseval).")
print("  E3. Use la formula trigonometrica b_k = 4A/(pi k) (impares) y")
print("      verifique que |c_k| = b_k/2.")
print("  E4. Cambie la onda a una con ciclo de trabajo diferente y observe")
print("      que aparecen armonicos pares.")

plt.show()
