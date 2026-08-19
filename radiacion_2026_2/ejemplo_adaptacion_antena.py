#!/usr/bin/env python3
"""ejemplo_adaptacion_antena.py

Tema 1 - Ejemplo practico: adaptar una antena.

Este script hace:
  - calcula todo en forma analitica, paso a paso,
  - lo repite con scikit-rf (parmetros S / carta de Smith),
  - dibuja la trayectoria de adaptacion sobre la carta de Smith.

Paso a paso:

  1. Carga de antena  Z_L = 30 + j20 ohm a 100 MHz, linea de Z_0 = 50 ohm.
  2. Normalizacion   z_L = Z_L / Z_0 = 0.6 + j0.4.
  3. Coeficiente de reflexion
        Gamma = (z_L - 1) / (z_L + 1) = -0.176 + j0.294
        |Gamma| = 0.343  ->  VSWR = (1+|Gamma|)/(1-|Gamma|) ~= 2.04.
  4. Cancelar la reactancia con un capacitor serie de X_C = -20 ohm:
        C = 1/(2*pi*f*|X_C|) ~= 79.6 pF.
        Queda z' = 0.6 + j0  (R = 30 ohm).
  5. Adaptar R = 30 ohm con un transformador de cuarto de onda de
        Z_t = sqrt(30*50) ~= 38.7 ohm  ->  Gamma ~= 0 (adaptado).

Ejecutar (con una pantalla disponible):
    python3 ejemplo_adaptacion_antena.py

Mostrar las graficas en pantalla (ventanas interactivas) en lugar de
guardarlas en archivos:
    python3 ejemplo_adaptacion_antena.py --show

Sin pantalla (servidor / SSH), guarde las figuras a archivos:
    MPLBACKEND=Agg python3 ejemplo_adaptacion_antena.py

Dependencias:
    python3 -m pip install --user scikit-rf numpy matplotlib
"""

import numpy as np
import argparse
import matplotlib
import matplotlib.pyplot as plt
import skrf as rf
from skrf.media import DefinedGammaZ0

# ---- parametros del ejemplo ----
F0_HZ = 100.0e6          # frecuencia de trabajo 100 MHz
Z0 = 50.0                # impedancia caracteristica de la linea
ZL = 30 + 20j            # impedancia de la antena (30 + j20) ohm
C_LUZ = 299792458.0      # velocidad de la luz [m/s]


def gamma(z: complex, z0: float) -> complex:
    """Coeficiente de reflexion Gamma = (Z - Z0)/(Z + Z0)."""
    return (z - z0) / (z + z0)


def vswr(z: complex, z0: float) -> float:
    """VSWR = (1 + |Gamma|)/(1 - |Gamma|) para una impedancia z contra z0."""
    g = abs(gamma(z, z0))
    return (1 + g) / (1 - g)


def main(show: bool = False) -> None:
    print("=" * 62)
    print("EJEMPLO PRACTICO: ADAPTAR UNA ANTENA  (Z_L = 30 + j20, Z0 = 50)")
    print("=" * 62)

    # 1) Pasos analiticos
    z_norm = ZL / Z0                       # normalizar (paso 1)
    gam = gamma(ZL, Z0)                    # coeficiente de reflexion (paso 2)
    swr = vswr(ZL, Z0)                     # VSWR (paso 2)

    print(f"\n[1] Carga normalizada:  z_L = {z_norm.real:.2f} + j{z_norm.imag:.2f}")
    print(f"[2] Gamma  = ({gam.real:+.3f} {gam.imag:+.3f}j)")
    print(f"    |Gamma| = {abs(gam):.3f}")
    print(f"    VSWR   = {swr:.2f}   (la lamina da 1.343/0.657 ~= 2.04)")

    # Capacitor serie que cancela la reactancia inductiva +j20 (paso 3)
    XC = -20.0                             # reactancia del capacitor [ohm]
    C_farad = 1.0 / (2 * np.pi * F0_HZ * abs(XC))
    Z_despues_cap = ZL.real + 0j            # 30 + j20 - j20 = 30 ohm

    print(f"[3] Capacitor serie X_C = {XC:g} ohm:")
    print(f"    C = 1/(2*pi*f*|X_C|) = {C_farad*1e12:.1f} pF   (la lamina: 79.6 pF)")
    print(f"    Z' = Z_L + X_C = {Z_despues_cap.real:.0f} + j0 ohm  (R = 30 ohm)")

    # Transformador de cuarto de onda (paso 4)
    Zt = np.sqrt(ZL.real * Z0)             # Z_t = sqrt(30*50) = 38.7 ohm
    Z_final = Zt**2 / ZL.real              # Z_in = Z_t^2 / Z_L = 50 ohm
    print(f"[4] Transformador de cuarto de onda:  Z_t = sqrt(30*50) = {Zt:.1f} ohm")
    print(f"    Z_in = Z_t^2/R = {Z_final:.1f} ohm  (la lamina: ~38.7 ohm)")

    # 2) Comprobacion con scikit-rf (parmetros S / carta de Smith)
    freq = rf.Frequency(F0_HZ, F0_HZ, 1, 'Hz')
    media = DefinedGammaZ0(freq, z0=Z0)

    # 2.1) Red de carga desadaptada (solo la antena, referencia 50 ohm)
    red_carga = rf.Network(
        s=np.array([[[gamma(ZL, Z0)]]]), frequency=freq, z0=Z0)

    print("\n[skrf] Verificacion del punto de carga (Z_L contra 50 ohm):")
    s11 = red_carga.s[0, 0, 0]
    print(f"       s11       = {s11.real:+.3f}{s11.imag:+.3f}j")
    print(f"       |s11|     = {abs(s11):.3f}")
    print(f"       VSWR(s11) = {red_carga.s_vswr[0, 0, 0]:.2f}")

    # 2.2) Serie: capacitor de 79.6 pF (paso 3)  ->  Z = 30 + j0
    cap = media.capacitor(C_farad, unit='F')
    tras_cap = cap ** red_carga

    # 2.3) Transformador de cuarto de onda (paso 4) ->  Gamma ~= 0
    #      El QWT es una seccion de linea de 38.7 ohm y 90 grados. Sus
    #      puertos se renormalizan (entrada a 50, salida a 30) para que el
    #      encadenado represente correctamente el circuito fisico.
    qwt = DefinedGammaZ0(freq, z0=Zt).line(d=90, unit='deg')
    qwt.renormalize([50.0, ZL.real])
    adaptado = qwt ** tras_cap

    print("\n[skrf] Red de adaptacion (cap. serie + transformador 1/4 de onda):")
    s11_adapt = adaptado.s[0, 0, 0]
    print(f"       Z tras capacitor        = {tras_cap.z[0, 0, 0]:.2f} ohm")
    print(f"       Z entrada tras QWT      = {adaptado.z[0, 0, 0]:.2f} ohm")
    print(f"       |s11| entrada           = {abs(s11_adapt):.2e}")
    print("       (un valor ~1e-16 confirma la adaptacion: Gamma ~ 0)")

    # 3) Carta de Smith con la trayectoria  z_L -> z' -> centro
    puntos = np.array([
        red_carga.s[0, 0, 0],   # z_L (desadaptado)
        tras_cap.s[0, 0, 0],    # z'  (tras el capacitor)
        adaptado.s[0, 0, 0],    # centro (adaptado)
    ])
    etiquetas = ['z_L = 0.6 + j0.4', "z' = 0.6 + j0 (tras C)", 'adaptado']

    fig, ax = plt.subplots(figsize=(7, 7))
    rf.plotting.plot_smith(puntos, ax=ax, draw_labels=False, chart_type='z')
    ax.plot(puntos.real, puntos.imag, 'o-', color='crimson', lw=1.5, ms=8)
    for p, lab in zip(puntos, etiquetas):
        ax.annotate(lab, (p.real * 1.05, p.imag * 1.1),
                    fontsize=9, ha='center')
    ax.set_title('Carta de Smith - adaptacion de la antena\n'
                 f'Z_L = {ZL.real:.0f}+j{ZL.imag:.0f} ohm, Z0 = {Z0:.0f} ohm, '
                 f'f = {F0_HZ/1e6:.0f} MHz')
    fig.tight_layout()
    if not show:
        fig.savefig('smith_adaptacion.png', dpi=150)
        print("\n[figura] Carta de Smith guardada en 'smith_adaptacion.png'")
    else:
        print("\n[figura] Mostrando la carta de Smith en pantalla...")
        plt.show()

    # 4) Verificaciones numericas
    ok1 = abs(abs(gam) - 0.343) < 0.001
    ok2 = abs(swr - 2.04) < 0.01
    ok3 = abs(C_farad * 1e12 - 79.6) < 0.1
    ok4 = abs(Zt - 38.7) < 0.05
    print("\n[verificacion]")
    for nombre, cond in [('|Gamma| = 0.343', ok1),
                         ('VSWR = 2.04', ok2),
                         ('C = 79.6 pF', ok3),
                         ('Z_t = 38.7 ohm', ok4)]:
        print(f"   {nombre:<18} {'OK' if cond else 'FALLO'}")

    # 5) Ejercicios propuestos (complete y verifique)
    print("\n[ejercicios propuestos]")
    print("  E1. Repita el ejemplo con Z_L = 60 - j30 ohm: calcule C (ahora")
    print("      se necesita una inductancia X_L = +30 ohm) y el nuevo Z_t.")
    print("  E2. Verifique con scikit-rf que el VSWR de un punto en la carta")
    print("      coincide con la distancia del punto al centro (radio).")
    print("  E3. Grafique la trayectoria completa en la carta Y (admitancia)")
    print("      con chart_type='y' y explique que cambia.")

    if not show and not matplotlib.is_interactive():
        plt.close('all')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Ejemplo practico de adaptacion de antena '
                    '(carta de Smith con scikit-rf).')
    parser.add_argument('--show', action='store_true',
                        help='mostrar las graficas en pantalla en lugar de '
                             'guardarlas en archivos PNG')
    args = parser.parse_args()
    main(show=args.show)
