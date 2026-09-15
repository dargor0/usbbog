#!/usr/bin/env python3
"""11_espectro_bilateral.py

Tema 2 - Espectro bilateral, frecuencias negativas y simetria hermitiana.
Ejecutar:  python3 11_espectro_bilateral.py

Referencias a las láminas del Tema 2:
  - "El espectro de magnitud y de fase" (espectro bilateral).
  - "¿Por qué existen frecuencias negativas?": para senales reales hay
    simetria hermitiana (|c_-k| = |c_k|, fase impar); cualquier asimetria
    implica que la senal en el tiempo es compleja.

Uso de SciPy: scipy.integrate.quad para los coeficientes de la onda cuadrada.
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad

A, T, f0 = 1.0, 1.0, 1.0


def x_cuadrada(t):
    return np.where(np.mod(t, T) < T / 2, A, -A)


def ck_cuadrada(k):
    """c_k de la onda cuadrada (real): 2A/(j pi k) impares, 0 pares."""
    if k == 0 or k % 2 == 0:
        return 0.0
    return 2 * A / (1j * np.pi * k)


print("=" * 62)
print("ESPECTRO BILATERAL Y SIMETRIA HERMITIANA")
print("=" * 62)

# --------------------------------------------------------------------------
# 1) Senal REAL (onda cuadrada): espectro simetrico
# --------------------------------------------------------------------------
k = np.arange(-12, 13)
c_real = np.array([ck_cuadrada(kk) for kk in k])

print("\n[1] Senal real (onda cuadrada): espectro SIMETRICO")
print(f"    |c_1| = {abs(c_real[13]):.4f}  |c_-1| = {abs(c_real[11]):.4f}")
print(f"    fase c_1 = {np.angle(c_real[13]):+.4f}  "
      f"fase c_-1 = {np.angle(c_real[11]):+.4f} (opuestas)")
print("    -> |c_-k| = |c_k|  y  fase impar  (simetria hermitiana)")

# --------------------------------------------------------------------------
# 2) Senal COMPLEJA: espectro asimetrico
# --------------------------------------------------------------------------
# x(t) = e^{j2pi f0 t}: solo el coeficiente c_1 = 1 (rotacion unica)
print("\n[2] Senal compleja x(t) = e^{j2pi f0 t}: espectro ASIMETRICO")
print("    c_1 = 1 (solo frecuencia positiva); c_-1 = 0")
print("    -> la asimetria del espectro indica que la senal es compleja")

# --------------------------------------------------------------------------
# 3) Graficas comparativas
# --------------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(10, 6))

axes[0, 0].stem(k, np.abs(c_real), basefmt=" ")
axes[0, 0].set_title("Real: |c_k| (simetrico)")
axes[0, 0].set_xlabel("k"); axes[0, 0].grid(alpha=0.3)

axes[0, 1].stem(k, np.angle(c_real), basefmt=" ")
axes[0, 1].set_title("Real: fase (impar)")
axes[0, 1].set_xlabel("k"); axes[0, 1].set_ylim(-3, 3)
axes[0, 1].grid(alpha=0.3)

c_comp = np.where(k == 1, 1.0, 0.0)
axes[1, 0].stem(k, np.abs(c_comp), basefmt=" ")
axes[1, 0].set_title("Compleja: |c_k| (asimetrico)")
axes[1, 0].set_xlabel("k"); axes[1, 0].grid(alpha=0.3)

axes[1, 1].stem(k, np.angle(np.where(c_comp != 0, c_comp, np.nan)),
                basefmt=" ")
axes[1, 1].set_title("Compleja: fase")
axes[1, 1].set_xlabel("k"); axes[1, 1].grid(alpha=0.3)
fig.tight_layout()

# --------------------------------------------------------------------------
# 4) Espectro unilateral (solo frecuencias positivas) para la senal real
# --------------------------------------------------------------------------
print("\n[3] Espectro unilateral (solo frecuencias positivas, senal real):")
print("    se duplica la amplitud de cada |c_k| (k>0); la potencia se")
print("    conserva: P = |c_0|^2 + 2*sum_{k>0}|c_k|^2")

k_pos = np.arange(1, 7)
mag_pos = 2 * np.abs(np.array([ck_cuadrada(kk) for kk in k_pos]))
for kk, m in zip(k_pos, mag_pos):
    print(f"    |c_{kk}| unilateral = {m:.4f}")

# ---------------------------------------------------------------------------
# Ejercicios propuestos
# ---------------------------------------------------------------------------
print("\n[ejercicios propuestos]")
print("  E1. Verifique la potencia: sum |c_k|^2 (bilateral) debe ser igual")
print("      a |c_0|^2 + 2 sum_{k>0} |c_k|^2 (unilateral).")
print("  E2. Genere x(t) = cos(2pi f0 t) y muestre que su espectro tiene")
print("      dos lineas iguales en +f0 y -f0 (amplitud 1/2).")
print("  E3. Explique por que las frecuencias negativas no son fisicas pero")
print("      simplifican el calculo (formulacion exponencial).")
print("  E4. Para una senal compleja x(t)=e^{j2pi f1 t}+e^{j2pi f2 t},")
print("      grafique el espectro y observe que NO hay simetria.")

plt.show()
