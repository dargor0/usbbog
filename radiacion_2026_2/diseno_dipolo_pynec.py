#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""diseno_dipolo_pynec.py

Tema 2 - Diseno de un dipolo resonante a una frecuencia dada.

Recibe la **frecuencia de operacion** y calcula la **longitud** que hace que el
dipolo resuene alli (reactancia de entrada X(f0) = 0), usando PyNEC (NEC2).

Idea del metodo
---------------
La frecuencia de resonancia de un dipolo depende de su longitud electrica:
    f_res ~ 1 / L      (para una geometria y un radio de hilo dados).
Partiendo de una longitud inicial L (p. ej. 0.48*lambda) se simula Zin(f) en un
barrido alrededor de f0 para hallar f_res (cruce por cero de X) y se corrige
    L_nuevo = L * f_res / f0
repitiendo hasta que f_res = f0 dentro de la tolerancia.  Es el mismo criterio
que se usa en el laboratorio al recortar un dipolo mirando el minimo de SWR.

Uso:
    python3 diseno_dipolo_pynec.py -f 300
    python3 diseno_dipolo_pynec.py -f 145 -a 0.002 -z 50
    python3 diseno_dipolo_pynec.py -f 300 -s        # mostrar grafica en pantalla
    python3 diseno_dipolo_pynec.py -f 300 --nec     # ademas, exportar el .nec

Dependencias:
    python3 -m pip install --user pynec numpy matplotlib
"""

import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from PyNEC import nec_context

C = 299792458.0            # velocidad de la luz [m/s]


# ---------------------------------------------------------------------------
# Modelo NEC2 del dipolo
# ---------------------------------------------------------------------------
def dipolo_z(freq_mhz, longitud, seg, radio):
    """Dipolo centrado en el origen, sobre el eje z, alimentado al centro."""
    nec = nec_context()
    geo = nec.get_geometry()
    # GW: hilo de (0,0,-L/2) a (0,0,+L/2); razones de expansion 1.0,1.0
    geo.wire(1, seg, 0, 0, -longitud / 2, 0, 0, longitud / 2, radio, 1.0, 1.0)
    nec.geometry_complete(0)                    # GE: sin plano de tierra
    nec.fr_card(0, 1, freq_mhz, 0)              # FR: frecuencia [MHz]
    nec.ex_card(0, 1, seg // 2, 0, 1.0, 0, 0, 0, 0, 0)  # EX: fuente 1 V al centro
    return nec


def impedancia(freq_mhz, longitud, seg, radio):
    """Devuelve Zin = R + jX [ohm] del dipolo de longitud dada a 'freq_mhz'."""
    nec = dipolo_z(freq_mhz, longitud, seg, radio)
    nec.xq_card(0)                              # XQ: ejecutar
    z = nec.get_input_parameters(0).get_impedance()
    return complex(float(np.ravel(z.real)[0]), float(np.ravel(z.imag)[0]))


def gamma_swr(zin, z0):
    """Gamma y SWR de Zin frente a una linea de impedancia z0."""
    g = (zin - z0) / (zin + z0)
    return g, (1 + abs(g)) / (1 - abs(g))


# ---------------------------------------------------------------------------
# Busqueda de la frecuencia de resonancia (X = 0) para una longitud dada
# ---------------------------------------------------------------------------
def frecuencia_resonancia(f0_mhz, L, seg, radio, npts=61, span=0.25):
    """Halla f_res [MHz] (cruce por cero de la reactancia X) barriendo la
    frecuencia en +/- span*f0 alrededor de f0, para la longitud L dada.

    Si hay varios cruces se toma el mas cercano a f0; si no hay cruce, se
    devuelve la frecuencia de |X| minimo (aproximacion)."""
    fs = np.linspace(f0_mhz * (1 - span), f0_mhz * (1 + span), npts)
    X = np.array([impedancia(f, L, seg, radio).imag for f in fs])

    cruces = np.where(np.diff(np.sign(X)))[0]     # indices donde X cambia de signo
    if len(cruces) == 0:
        return fs[int(np.argmin(np.abs(X)))]
    # interpolacion lineal en cada cruce y escoger el mas cercano a f0
    f_roots = []
    for i in cruces:
        f1, f2, x1, x2 = fs[i], fs[i + 1], X[i], X[i + 1]
        f_roots.append(f1 - x1 * (f2 - f1) / (x2 - x1))
    f_roots = np.array(f_roots)
    return float(f_roots[np.argmin(np.abs(f_roots - f0_mhz))])


# ---------------------------------------------------------------------------
# Diseno iterativo de la longitud resonante
# ---------------------------------------------------------------------------
def disenar_longitud(f0_mhz, seg, radio, z0, tol=1e-4, max_iter=20, K0=0.48,
                     verbose=True):
    """Calcula la longitud L que hace resonar el dipolo en f0.

    Parametros:
      f0_mhz : frecuencia de operacion [MHz].
      seg    : numero de segmentos (impar).
      radio  : radio del hilo [m].
      z0     : impedancia de referencia para el SWR [ohm].
      tol    : tolerancia relativa en frecuencia (def 1e-4 = 0.01 %).
      max_iter : iteraciones maximas.
      K0     : factor inicial de longitud (L0 = K0*lambda); 0.48 es tipico.
    Devuelve un diccionario con los resultados.
    """
    lam = C / (f0_mhz * 1e6)          # longitud de onda [m]
    L = K0 * lam                      # longitud inicial [m]

    if verbose:
        print(f"lambda = {lam:.4f} m   longitud inicial L0 = {K0:.3f} lambda = {L:.4f} m")
        print(f"\n{'it':>3} {'L [m]':>10} {'L/lambda':>9} {'f_res [MHz]':>12} "
              f"{'X(L) [ohm]':>11}")
    for it in range(1, max_iter + 1):
        f_res = frecuencia_resonancia(f0_mhz, L, seg, radio)
        x_l = impedancia(f0_mhz, L, seg, radio).imag
        if verbose:
            print(f"{it:>3} {L:>10.5f} {L/lam:>9.4f} {f_res:>12.3f} {x_l:>11.2f}")
        if abs(f_res - f0_mhz) / f0_mhz < tol:
            break
        # Como f_res ~ 1/L, se corrige proporcionalmente:
        L = L * f_res / f0_mhz

    zin = impedancia(f0_mhz, L, seg, radio)
    g, swr = gamma_swr(zin, z0)
    return {
        "f0_mhz": f0_mhz, "lambda_m": lam, "L_m": L, "L_over_lambda": L / lam,
        "K": L / (lam / 2), "f_res_mhz": f_res, "Zin": zin,
        "Gamma": g, "SWR": swr, "z0": z0, "iteraciones": it,
    }


# ---------------------------------------------------------------------------
# Interfaz de linea de comandos
# ---------------------------------------------------------------------------
def parse_args(argv=None):
    ap = argparse.ArgumentParser(
        description='Disena la longitud de un dipolo resonante a una frecuencia.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument('-f', '--freq', type=float, required=True,
                    help='frecuencia de operacion [MHz] (obligatorio)')
    ap.add_argument('-a', '--radius', type=float, default=1e-3,
                    help='radio del hilo [m]')
    ap.add_argument('-n', '--segments', type=int, default=31,
                    help='numero de segmentos del hilo (impar)')
    ap.add_argument('-z', '--z0', type=float, default=50.0,
                    help='impedancia de referencia para el SWR [ohm]')
    ap.add_argument('--tol', type=float, default=1e-4,
                    help='tolerancia relativa en frecuencia')
    ap.add_argument('--max-iter', type=int, default=20,
                    help='numero maximo de iteraciones')
    ap.add_argument('--k0', type=float, default=0.48,
                    help='factor de longitud inicial (L0 = k0*lambda)')
    ap.add_argument('-s', '--show', action='store_true',
                    help='mostrar la grafica en pantalla en lugar de guardarla')
    ap.add_argument('--nec', action='store_true',
                    help='generar el archivo .nec para 4nec2/xnec2c (por defecto: no)')
    return ap.parse_args(argv)


def backend_is_interactive():
    """True si matplotlib puede abrir ventanas (QtAgg, TkAgg, ... son GUI)."""
    b = matplotlib.get_backend().lower()
    try:
        from matplotlib.backends import backend_registry, BackendFilter
        non_gui = {str(x).lower() for x in
                   backend_registry.list_builtin(BackendFilter.NON_INTERACTIVE)}
    except Exception:
        non_gui = {'agg', 'cairo', 'pdf', 'pgf', 'ps', 'svg', 'template'}
    return b not in non_gui


def main(args):
    use_screen = args.show and backend_is_interactive()

    print("=" * 66)
    print("DISENO DE UN DIPOLO RESONANTE (PyNEC)")
    print("=" * 66)
    print(f"f0 = {args.freq:.3f} MHz   radio = {args.radius*1e3:.2f} mm   "
          f"segmentos = {args.segments}   Z0 = {args.z0:.0f} ohm")

    r = disenar_longitud(args.freq, args.segments, args.radius, args.z0,
                         tol=args.tol, max_iter=args.max_iter, K0=args.k0)

    print("\n[RESULTADO]")
    print(f"  Longitud resonante  L   = {r['L_m']*100:.2f} cm = {r['L_m']:.5f} m")
    print(f"  Normalizada             = {r['L_over_lambda']:.4f} lambda")
    print(f"  Factor de acortamiento  = {r['K']:.4f}  (L / (lambda/2))")
    print(f"  Frecuencia de resonancia= {r['f_res_mhz']:.3f} MHz (objetivo {r['f0_mhz']:.3f})")
    print(f"  Zin(L) a f0             = {r['Zin'].real:.2f} {r['Zin'].imag:+.2f} j ohm")
    print(f"  |Gamma| = {abs(r['Gamma']):.3f}   SWR = {r['SWR']:.2f}  (Z0 = {r['z0']:.0f} ohm)")
    print(f"  Iteraciones             = {r['iteraciones']}")

    # ---- grafica Z(f) alrededor de f0 con la longitud resonante -----------
    fs = np.linspace(args.freq * 0.85, args.freq * 1.15, 121)
    Z = np.array([impedancia(f, r['L_m'], args.segments, args.radius) for f in fs])
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(fs, Z.real, 'b', label='R (ohm)')
    ax.plot(fs, Z.imag, 'r--', label='X (ohm)')
    ax.axhline(0, color='k', lw=0.5)
    ax.axvline(r['f_res_mhz'], color='g', ls=':', label=f"f_res = {r['f_res_mhz']:.2f} MHz")
    ax.set_xlabel('Frecuencia [MHz]'); ax.set_ylabel('Impedancia [ohm]')
    ax.set_title(f"Dipolo disenado: L = {r['L_m']:.4f} m ({r['L_over_lambda']:.3f} $\\lambda$)")
    ax.legend(); ax.grid(alpha=0.3); fig.tight_layout()
    if use_screen:
        plt.show()
    else:
        fig.savefig('diseno_dipolo_impedancia.png', dpi=150)
        print("\n[figura] diseno_dipolo_impedancia.png")
        if not matplotlib.is_interactive():
            plt.close('all')

    # ---- archivo .nec de la antena disenada (solo si se pide con --nec) ---
    if args.nec:
      lineas = [
        "CM Dipolo resonante disenado con diseno_dipolo_pynec.py",
        "CE",
        f"GW 1 {args.segments} 0 0 {-r['L_m']/2:.6f} 0 0 {r['L_m']/2:.6f} {args.radius:.6f}",
        "GE 0",
        f"FR 0 1 {args.freq:.3f}",
        f"EX 0 1 {args.segments//2} 0 1 0",
        "RP 0 181 1 1001 0 0 1 1",
        "EN",
      ]
      with open('dipolo_diseno.nec', 'w') as fh:
        fh.write("\n".join(lineas) + "\n")
      print("[nec]    dipolo_diseno.nec (para 4nec2 / xnec2c)")


if __name__ == '__main__':
    main(parse_args())
