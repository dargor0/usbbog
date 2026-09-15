#!/usr/bin/env python3
"""09_reconstruccion_gibbs.py

Tema 2 - Reconstruccion (sintesis) de la onda cuadrada y fenomeno de Gibbs.
Ejecutar:  python3 09_reconstruccion_gibbs.py

Referencias a las laminas del Tema 2:
  - "La idea base (2/3): del tiempo a la frecuencia": sumar armonicos aproxima
    la onda cuadrada (N = 1, 3, 5...).
  - "Ejemplo: coeficientes de la onda cuadrada":
        x(t) = (4A/pi)[ sin(w0 t) + (1/3) sin(3 w0 t) + (1/5) sin(5 w0 t) + ... ]
  - Fenomeno de Gibbs: sobrepaso de ~9% en los bordes, que no desaparece
    al aumentar N.
"""

import matplotlib.pyplot as plt
import numpy as np

A = 1.0
T = 1.0
w0 = 2 * np.pi / T

# eje temporal: un periodo y un poco mas para ver los bordes
t = np.linspace(0, 2 * T, 4000)

# onda cuadrada ideal
x_ideal = np.where(np.mod(t, T) < T / 2, A, -A)


def reconstruccion(N):
    """Suma de los N primeros armonicos impares de la onda cuadrada."""
    x = np.zeros_like(t)
    for k in range(1, N + 1, 2):          # k = 1, 3, 5, ...
        x += np.sin(k * w0 * t) / k
    return (4 * A / np.pi) * x


print("=" * 60)
print("RECONSTRUCCION DE LA ONDA CUADRADA Y FENOMENO DE GIBBS")
print("=" * 60)

for N in [1, 3, 5, 9, 21, 101]:
    xN = reconstruccion(N)
    rms = np.sqrt(np.mean((xN - x_ideal) ** 2))
    print(f"\n[1] N = {N:3d} armonicos:")
    print(f"    error RMS = {rms:.4f}  (A = {A})")

# sobrepaso de Gibbs: maximo de la suma cerca del borde
xN = reconstruccion(501)
sobrepaso = (xN.max() - A) / A * 100
print(f"\n[2] Sobrepaso de Gibbs con N = 501: {sobrepaso:.2f}%")
print("    (sobrepaso ~9% del salto 2A, es decir ~17.9% de A; pico ~1.179 A)")

# grafica de las aproximaciones
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(t, x_ideal, 'k--', lw=1.5, label="Onda cuadrada ideal")
for N, c, ls in [(1, 'b', '-'), (3, 'g', '-'), (9, 'r', '-'), (101, 'm', '-')]:
    ax.plot(t, reconstruccion(N), c, ls, lw=1.2, label=f"N = {N}")
ax.set_xlim(0, T)
ax.set_xlabel("t [s]")
ax.set_ylabel("x(t)")
ax.set_title("Aproximacion de la onda cuadrada con N armonicos")
ax.legend(fontsize=8)
ax.grid(alpha=0.3)
fig.tight_layout()

# grafica del sobrepaso vs N (convergencia)
Ns = [1, 3, 5, 9, 21, 51, 101, 501]
maxs = [np.max(np.abs(reconstruccion(n))) for n in Ns]
fig2, ax2 = plt.subplots(figsize=(9, 4))
ax2.semilogx(Ns, maxs, 'o-')
ax2.axhline(A * 1.17896, color='r', ls='--',
            label="Limite de Gibbs: ~1.179 A")
ax2.set_xlabel("Numero de armonicos N")
ax2.set_ylabel("Pico de la aproximacion")
ax2.set_title("Convergencia del maximo (fenomeno de Gibbs)")
ax2.legend(fontsize=8)
ax2.grid(alpha=0.3, which='both')
fig2.tight_layout()

# ---------------------------------------------------------------------------
# Ejercicios propuestos
# ---------------------------------------------------------------------------
print("\n[ejercicios propuestos]")
print("  E1. Aumente N a 1001 y verifique que el sobrepaso sigue en ~9%")
print("      (el pico no desaparece; solo se estrecha).")
print("  E2. Aplique una ventana (p. ej., multiplicar cada coeficiente por")
print("      una ventana de Lanczos/Hanning) y observe la reduccion del")
print("      sobrepaso a costa de bordes mas suaves.")
print("  E3. Cambie la amplitud a A = 2 y verifique que el sobrepaso es")
print("      proporcional (sigue siendo ~9% de A).")
print("  E4. Reconstruya una senal triangular (coeficientes ~1/k^2) y")
print("      compare la velocidad de convergencia con la onda cuadrada.")

plt.show()
