#!/usr/bin/env python3
"""01_presupuesto_enlace.py

Tema 1 - Presupuesto de enlace (laminas "Presupuesto de enlace",
"Parametros del presupuesto de enlace", "EIRP y perdidas adicionales" y
"Ejemplo: enlace a 5.8 GHz").

Recrea el ejemplo de las diapositivas y permite variar parametros:

    Enlace a 5.8 GHz:  P_t = 20 dBm, G_t = 15 dBi, G_r = 12 dBi,
    cables de 2 dB c/u, d = 5 km, f = 5.8 GHz.

Formulas (en dB):
    L_esp = 92.45 + 20*log10(f_GHz) + 20*log10(d_km)
    EIRP  = P_t + G_t - L_cable_TX
    P_r   = P_t + G_t + G_r - L_esp - L_cables - L_otros - M
    margen = P_r - P_min        (P_min = sensibilidad)

Ejecutar (con pantalla):
    python3 01_presupuesto_enlace.py

Mostrar las graficas en pantalla:
    python3 01_presupuesto_enlace.py --show

Dependencias: python3 -m pip install --user numpy matplotlib
"""

import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def loss_espacio_libre(f_ghz, d_km):
    """Perdida en espacio libre en dB (lamina: L_esp = 92.45 + ...)."""
    return 92.45 + 20 * np.log10(f_ghz) + 20 * np.log10(d_km)


def potencia_recibida(Pt, Gt, Gr, L_esp, L_cables, L_otros=0.0, M=0.0):
    """Potencia recibida en dBm (lamina: P_r = P_t + G_t + G_r - ...)."""
    return Pt + Gt + Gr - L_esp - L_cables - L_otros - M


def main(show=False):
    print("=" * 64)
    print("PRESUPUESTO DE ENLACE  (ejemplo de la lamina: 5.8 GHz)")
    print("=" * 64)

    # ------------------------------------------------------------------
    # 1) Ejemplo de la lamina (verificar cada paso)
    # ------------------------------------------------------------------
    Pt, Gt, Gr = 20.0, 15.0, 12.0       # dBm, dBi, dBi
    L_cable_tx, L_cable_rx = 2.0, 2.0   # dB (cada uno)
    L_cables = L_cable_tx + L_cable_rx  # total de cables (dB)
    d_km, f_ghz = 5.0, 5.8
    Pmin = -90.0                        # sensibilidad (dBm)

    L_esp = loss_espacio_libre(f_ghz, d_km)
    EIRP = Pt + Gt - L_cable_tx
    Pr = potencia_recibida(Pt, Gt, Gr, L_esp, L_cables)
    margen = Pr - Pmin

    print(f"\n[1] Ejemplo a {f_ghz} GHz, d = {d_km} km:")
    print(f"    EIRP = P_t + G_t - L_cable = {EIRP:.1f} dBm")
    print(f"    L_esp = 92.45 + 20log10({f_ghz}) + 20log10({d_km}) "
          f"= {L_esp:.1f} dB   (la lamina: 121.7)")
    print(f"    P_r = {Pt} + {Gt} + {Gr} - 2 - 2 - {L_esp:.1f} "
          f"= {Pr:.1f} dBm  (la lamina: -78.7)")
    print(f"    Margen = P_r - P_min = {Pr:.1f} - ({Pmin}) = {margen:.1f} dB")

    # ------------------------------------------------------------------
    # 2) Sensibilidad del margen a la distancia y la frecuencia
    # ------------------------------------------------------------------
    print("\n[2] Variar d y f:  L_esp y P_r")
    print("    d[km] | f=2.4  f=5.8  f=10  f=24  (P_r en dBm)")
    for d in [1.0, 2.0, 5.0, 10.0, 20.0]:
        fila = []
        for f in [2.4, 5.8, 10.0, 24.0]:
            Le = loss_espacio_libre(f, d)
            fila.append(potencia_recibida(Pt, Gt, Gr, Le, L_cables))
        print(f"    {d:5.1f} | " + " ".join(f"{p:7.1f}" for p in fila))

    # ------------------------------------------------------------------
    # 3) Grafica: P_r vs d para varias frecuencias y la sensibilidad
    # ------------------------------------------------------------------
    ds = np.linspace(0.5, 25.0, 200)
    fig, ax = plt.subplots(figsize=(9, 5))
    for f in [2.4, 5.8, 10.0, 24.0]:
        Le = loss_espacio_libre(f, ds)
        ax.plot(ds, potencia_recibida(Pt, Gt, Gr, Le, L_cables),
                label=f"f = {f} GHz")
    ax.axhline(Pmin, color='r', ls='--', lw=1.2,
               label=f"Sensibilidad {Pmin:.0f} dBm")
    ax.set_xlabel("Distancia [km]")
    ax.set_ylabel("P_r [dBm]")
    ax.set_title("Presupuesto de enlace: potencia recibida vs distancia")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    if not show:
        fig.savefig("presupuesto_enlace.png", dpi=150)
        print("\n[figura] Guardada en 'presupuesto_enlace.png'")
    else:
        print("\n[figura] Mostrando en pantalla...")
        plt.show()

    # ------------------------------------------------------------------
    # 4) Alcance maximo (d para margen >= 0) y efecto del margen de fading
    # ------------------------------------------------------------------
    dmax = 10 ** ((Pt + Gt + Gr - L_cables - Pmin - 92.45
                   - 20 * np.log10(f_ghz)) / 20.0)
    print(f"\n[4] Alcance maximo a {f_ghz} GHz (P_r = sensibilidad): "
          f"{dmax:.2f} km")

    M_fade = 10.0
    dmax_fade = 10 ** ((Pt + Gt + Gr - L_cables - M_fade - Pmin - 92.45
                        - 20 * np.log10(f_ghz)) / 20.0)
    print(f"    Con margen de desvanecimiento M = {M_fade:.0f} dB: "
          f"alcance = {dmax_fade:.2f} km")

    # ------------------------------------------------------------------
    # 5) Ejercicios propuestos
    # ------------------------------------------------------------------
    print("\n[ejercicios propuestos]")
    print("  E1. Cambie la sensibilidad a -85 dBm: calcule el nuevo margen")
    print("      y el nuevo alcance maximo.")
    print("  E2. Agregue 3 dB de perdidas por lluvia (L_otros) y verifique")
    print("      como cae el margen.")
    print("  E3. Para un enlace satelital (f = 12 GHz, d = 36000 km)")
    print("      calcule L_esp; explique por que se usan antenas de alta")
    print("      ganancia.")
    print("  E4. Duplique la distancia (10 km): verifique que P_r cae 6 dB")
    print("      (regla 20*log10).")

    if not show and not matplotlib.is_interactive():
        plt.close('all')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Presupuesto de enlace (ejemplo 5.8 GHz).")
    parser.add_argument('--show', action='store_true',
                        help='mostrar las graficas en pantalla en lugar de '
                             'guardarlas en archivos PNG')
    args = parser.parse_args()
    main(show=args.show)
