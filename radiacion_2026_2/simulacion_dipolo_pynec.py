#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""simulacion_dipolo_pynec.py

Tema 2 - Practica del tema: simulacion de un dipolo de media onda.

Modela un dipolo con PyNEC (puerto Python de NEC2, el mismo metodo de momentos
que usan 4nec2 / xnec2c / nec2c) y extrae, para comparar con la teoria:

  1. Impedancia de entrada Z(f) = R + jX y frecuencia de resonancia.
  2. Coeficiente de reflexion Gamma, SWR y Return Loss (para Z0).
  3. Patron de radiacion en los planos E y H y el HPBW (puntos de -3 dB).
  4. Directividad (integrando el patron sobre la esfera), ganancia, eficiencia
     y apertura efectiva Ae = lambda^2 G / (4 pi).

Genera ademas el archivo .nec para abrirlo en 4nec2 / xnec2c y comparar.

Uso (todos los parametros tienen valor por defecto):
    python3 simulacion_dipolo_pynec.py [opciones]
    python3 simulacion_dipolo_pynec.py -f 500 -n 21 -a 0.002 -z 75
    python3 simulacion_dipolo_pynec.py --sweep 450 550 2
    python3 simulacion_dipolo_pynec.py -s          # mostrar en pantalla
    python3 simulacion_dipolo_pynec.py --nec       # ademas, exportar el .nec
    MPLBACKEND=Agg python3 simulacion_dipolo_pynec.py   # sin pantalla

Dependencias:
    python3 -m pip install --user pynec numpy matplotlib

------------------------------------------------------------------------------
GLOSARIO DE LAS TARJETAS NEC2 USADAS (formato de entrada de NEC2):
  GW  Geometry Wire: define un hilo recto -> GW tag nseg x1 y1 z1 x2 y2 z2 rad
  GE  Geometry End: cierra la geometria (0 = sin plano de tierra)
  FR  FRequency: define la frecuencia -> FR 0 nfreq f0
  EX  EXcitation: fuente -> EX 0 tag seg 0 V 0 (fuente de tension en 'seg')
  RP  Radiation Pattern: pide el patron -> RP ... ntheta nphi ...
  XQ  eXecute: ejecuta el calculo antes de leer resultados
------------------------------------------------------------------------------
"""

# ---------------------------------------------------------------------------
# Importaciones
# ---------------------------------------------------------------------------
import argparse               # lectura de parametros de linea de comandos
import numpy as np            # calculo numerico (arreglos, trigonometria)
import matplotlib             # backend de graficacion
import matplotlib.pyplot as plt
from PyNEC import nec_context  # motor NEC2 (metodo de momentos)

# Constante fisica
C = 299792458.0            # velocidad de la luz en el vacio [m/s]

# Valores teoricos de referencia para el dipolo de lambda/2 con hilo delgado
# (dependen SOLO de la relacion L/lambda = 0.5, no de la frecuencia absoluta;
#  ver diapositivas "valores teoricos de referencia").
TEORIA = {
    "D0_dBi": 2.15,        # directividad teorica [dBi]  (D0 = 1.64)
    "HPBW_deg": 78.0,      # ancho de haz a -3 dB en el plano E [grados]
    "Rrad_ohm": 73.1,      # resistencia de radiacion [ohm]  (30*Cin(2*pi))
    "X_ohm": 42.5,         # reactancia a L = lambda/2 exacta [ohm] (30*Si(2*pi))
    "Ae_lambda2": 0.13,    # apertura efectiva normalizada: Ae/lambda^2
    "SWR_res": 1.46,       # SWR en resonancia (Z0 = 50 ohm)
}


# ---------------------------------------------------------------------------
# Modelo geometrico del dipolo
# ---------------------------------------------------------------------------
def dipolo_z(freq_mhz, longitud, seg, radio):
    """Construye un dipolo centrado en el origen, orientado sobre el eje z y
    alimentado en el centro.

    Por que en el eje z: con el hilo en z, el corte phi=0 corresponde al
    **plano E**; el maximo del patron queda en theta=90 (figura en ocho) y el
    HPBW se lee directamente entre los dos puntos de -3 dB.

    Parametros:
      freq_mhz : frecuencia de excitacion [MHz].
      longitud : longitud total del hilo [m].
      seg      : numero de segmentos del hilo (impar, para que exista un
                 segmento central donde colocar la alimentacion).
      radio    : radio del hilo [m] (hilo delgado: radio << lambda).

    Devuelve el objeto nec_context configurado (geometria, frecuencia y fuente).
    """
    nec = nec_context()
    geo = nec.get_geometry()

    # Tarjeta GW: un hilo del origen (0,0,-L/2) al extremo (0,0,+L/2) sobre z.
    # Los dos ultimos argumentos (1.0, 1.0) son las razones de expansion.
    geo.wire(1, seg, 0, 0, -longitud / 2, 0, 0, longitud / 2, radio, 1.0, 1.0)

    # Tarjeta GE: fin de geometria. El argumento 0 indica SIN plano de tierra.
    nec.geometry_complete(0)

    # Tarjeta FR: frecuencia. (0 = sin salto, 1 punto, f en MHz).
    nec.fr_card(0, 1, freq_mhz, 0)

    # Tarjeta EX: fuente de tension de 1 V (tipo 0) en el hilo 1, en el
    # segmento central (seg//2): alimenta el dipolo en el centro.
    nec.ex_card(0, 1, seg // 2, 0, 1.0, 0, 0, 0, 0, 0)

    return nec


# ---------------------------------------------------------------------------
# Impedancia de entrada
# ---------------------------------------------------------------------------
def impedancia(nec):
    """Ejecuta la simulacion de la geometria y devuelve la impedancia de
    entrada compleja Zin = R + jX [ohm].

    La tarjeta XQ (execute) resuelve el sistema del metodo de momentos; luego
    se lee la impedancia del puerto de entrada (segmento alimentado).
    """
    nec.xq_card(0)                                   # ejecutar el calculo
    z = nec.get_input_parameters(0).get_impedance()  # Zin compleja en el puerto
    # np.ravel(...) extrae el escalar aunque el resultado venga como arreglo.
    return complex(float(np.ravel(z.real)[0]), float(np.ravel(z.imag)[0]))


# ---------------------------------------------------------------------------
# Adaptacion: coeficiente de reflexion y SWR
# ---------------------------------------------------------------------------
def gamma_swr(zin, z0):
    """Calcula el coeficiente de reflexion y el SWR de una carga Zin frente a
    una linea de impedancia caracteristica z0.

        Gamma = (Zin - Z0) / (Zin + Z0)
        SWR   = (1 + |Gamma|) / (1 - |Gamma|)

    Devuelve (Gamma, SWR).
    """
    g = (zin - z0) / (zin + z0)
    return g, (1 + abs(g)) / (1 - abs(g))


# ---------------------------------------------------------------------------
# Patron de radiacion
# ---------------------------------------------------------------------------
def patron(freq_mhz, longitud, seg, radio, n_theta, n_phi, delta_theta, delta_phi):
    """Calcula el patron de radiacion (ganancia total en dBi) del dipolo.

    Parametros:
      freq_mhz, longitud, seg, radio : parametros del dipolo.
      n_theta, delta_theta : numero y paso de angulos theta (desde +z).
      n_phi,   delta_phi   : numero y paso de angulos phi (azimut).

    Devuelve (theta, phi, ganancia):
      theta : arreglo de angulos theta [grados].
      phi   : arreglo de angulos phi [grados].
      ganancia : ganancia total [dBi], con los nulos de NEC (-999.99) sustituidos
                 por un piso de -30 dB para poder graficar en escala dB.
    """
    nec = dipolo_z(freq_mhz, longitud, seg, radio)

    # Tarjeta RP: solicita el patron.
    #   calc_mode=0 : calculo normal (sin promediado).
    #   output_format=0, normalization=0 : salida estandar (ganancia total).
    #   theta0=0/phi0=0 y delta_* : reticula de angulos a evaluar.
    nec.rp_card(calc_mode=0, n_theta=n_theta, n_phi=n_phi, output_format=0,
                normalization=0, D=0, A=0, theta0=0, delta_theta=delta_theta,
                phi0=0, delta_phi=delta_phi, radial_distance=0, gain_norm=0)
    nec.xq_card(0)                                   # ejecutar
    r = nec.get_radiation_pattern(0)

    th = np.array(r.get_theta_angles()).ravel()
    ph = np.array(r.get_phi_angles()).ravel()
    g = np.array(r.get_gain()).ravel()
    # NEC marca las direcciones nulas con -999.99; se reemplazan por -30 dB.
    return th, ph, np.where(g < -900, -30.0, g)


# ---------------------------------------------------------------------------
# Exportacion a NEC2 (.nec) para 4nec2 / xnec2c / nec2c
# ---------------------------------------------------------------------------
def escribir_nec(nombre, f_mhz, long, radio, seg):
    """Escribe un archivo de entrada NEC2 (tarjetas) del mismo dipolo, para
    abrirlo en 4nec2 / xnec2c y comparar los resultados con PyNEC."""
    lineas = [
        "CM Dipolo (eje z) - tema2 - PyNEC",                 # comentario
        "CE",                                                # fin de comentarios
        f"GW 1 {seg} 0 0 {-long/2:.6f} 0 0 {long/2:.6f} {radio:.6f}",
        "GE 0",                                              # sin plano de tierra
        f"FR 0 1 {f_mhz:.1f}",                               # frecuencia [MHz]
        f"EX 0 1 {seg//2} 0 1 0",                            # fuente 1 V al centro
        "RP 0 181 1 1001 0 0 1 1",                           # patron theta 0..180
        "EN",                                                # fin del archivo
    ]
    with open(nombre, "w") as fh:
        fh.write("\n".join(lineas) + "\n")


# ---------------------------------------------------------------------------
# Deteccion de backend grafico
# ---------------------------------------------------------------------------
def backend_is_interactive():
    """True si matplotlib puede abrir ventanas (backend con GUI).

    Nota importante: los backends con GUI ('QtAgg', 'TkAgg', 'GTK3Agg', ...)
    CONTIENEN la subcadena 'agg' pero SI son interactivos. Solo los backends
    puramente no interactivos ('Agg', 'cairo', 'pdf', 'pgf', 'ps', 'svg',
    'template') no abren ventanas. Por eso se compara el nombre EXACTO contra
    esa lista (no por subcadena, lo que hacia que QtAgg se confundiera con Agg).
    """
    b = matplotlib.get_backend().lower()
    try:
        # API moderna (matplotlib >= 3.9)
        from matplotlib.backends import backend_registry, BackendFilter
        non_gui = {str(x).lower() for x in
                   backend_registry.list_builtin(BackendFilter.NON_INTERACTIVE)}
    except Exception:
        # Respaldo si la API no esta disponible
        non_gui = {'agg', 'cairo', 'pdf', 'pgf', 'ps', 'svg', 'template'}
    return b not in non_gui


# ---------------------------------------------------------------------------
# Interfaz de linea de comandos
# ---------------------------------------------------------------------------
def parse_args(argv=None):
    """Define y lee los parametros de simulacion (reemplaza valores fijos)."""
    ap = argparse.ArgumentParser(
        description='Simulacion de un dipolo con PyNEC (NEC2).',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument('-f', '--freq', type=float, default=300.0,
                    help='frecuencia de diseno [MHz]')
    ap.add_argument('-l', '--length', type=float, default=None,
                    help='longitud total del dipolo [m] (por defecto lambda/2)')
    ap.add_argument('-a', '--radius', type=float, default=1e-3,
                    help='radio del hilo [m]')
    ap.add_argument('-n', '--segments', type=int, default=31,
                    help='numero de segmentos del hilo (impar)')
    ap.add_argument('-z', '--z0', type=float, default=50.0,
                    help='impedancia caracteristica de la linea [ohm]')
    ap.add_argument('--sweep', type=float, nargs=3, default=[250.0, 350.0, 2.0],
                    metavar=('MIN', 'MAX', 'PASO'),
                    help='barrido de frecuencia [MHz]: inicio fin paso')
    ap.add_argument('--n-theta', type=int, default=181,
                    help='numero de puntos del patron en theta')
    ap.add_argument('--n-phi', type=int, default=72,
                    help='numero de puntos del patron en phi (para integrar D)')
    ap.add_argument('-s', '--show', action='store_true',
                    help='mostrar las graficas en pantalla en lugar de guardarlas')
    ap.add_argument('--nec', action='store_true',
                    help='generar el archivo .nec para 4nec2/xnec2c (por defecto: no)')
    return ap.parse_args(argv)


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------
def main(args):
    # ---- parametros (desde la linea de comandos) ----------------------
    f0_mhz = args.freq
    radio = args.radius
    seg = args.segments
    z0 = args.z0
    lam = C / (f0_mhz * 1e6)                 # longitud de onda [m]
    L = args.length if args.length is not None else lam / 2
    f_min, f_max, f_step = args.sweep
    use_screen = args.show and backend_is_interactive()

    print("=" * 66)
    print("PRACTICA TEMA 2 - SIMULACION DE UN DIPOLO (PyNEC)")
    print("=" * 66)
    print(f"f0 = {f0_mhz:.1f} MHz   lambda = {lam:.4f} m   L = {L:.4f} m "
          f"(L/lambda = {L/lam:.3f})")
    print(f"radio = {radio*1e3:.2f} mm   segmentos = {seg}   Z0 = {z0:.0f} ohm")
    print(f"barrido = {f_min:.0f}..{f_max:.0f} MHz (paso {f_step:.0f})")
    if abs(L - lam / 2) > 1e-9:
        print("[nota] L != lambda/2: los valores teoricos de referencia (tabla) "
              "corresponden a L = lambda/2.")

    # ------------------------------------------------------------------
    # 1) Barrido de impedancia Z(f) y busqueda de la resonancia
    # ------------------------------------------------------------------
    # Resonancia: frecuencia donde |X| es minima (idealmente X=0).
    freqs = np.arange(f_min, f_max + f_step / 2, f_step)
    Z = np.array([impedancia(dipolo_z(f, L, seg, radio)) for f in freqs])
    idx_res = int(np.argmin(np.abs(Z.imag)))
    f_res, R_res = freqs[idx_res], Z[idx_res].real

    # Impedancia a la frecuencia de diseno f0, y adaptacion a z0.
    Z0f = impedancia(dipolo_z(f0_mhz, L, seg, radio))
    g0, swr0 = gamma_swr(Z0f, z0)                        # en f0
    gres, swr_res = gamma_swr(complex(R_res, 0.0), z0)   # en resonancia (X=0)

    print(f"\n[1] Impedancia a {f0_mhz:.0f} MHz: Z = {Z0f.real:.1f} {Z0f.imag:+.1f}j ohm")
    print(f"    Resonancia (X=0): f = {f_res:.0f} MHz, R = {R_res:.1f} ohm")
    # Return Loss RL = -20*log10(|Gamma|) [dB].
    print(f"    |Gamma| = {abs(g0):.3f}   SWR = {swr0:.2f}   RL = {-20*np.log10(abs(g0)):.2f} dB")
    print(f"    (teoria a L=lambda/2: R_rad = {TEORIA['Rrad_ohm']} ohm, "
          f"X = +j{TEORIA['X_ohm']} ohm)")

    # ------------------------------------------------------------------
    # 2) Patron, HPBW y directividad
    # ------------------------------------------------------------------
    # 2a) Corte del plano E (phi=0) para medir el HPBW.
    th, _, g = patron(f0_mhz, L, seg, radio, n_theta=args.n_theta, n_phi=1,
                      delta_theta=180 // max(args.n_theta - 1, 1), delta_phi=1)
    i = int(np.argmax(g))            # indice del maximo del patron
    tgt = g[i] - 3.0                 # nivel de -3 dB (media potencia)
    il = ir = i                      # buscar los dos cruces de -3 dB
    while il > 0 and g[il] > tgt:
        il -= 1
    while ir < len(g) - 1 and g[ir] > tgt:
        ir += 1
    hpbw = th[ir] - th[il]           # ancho de haz a -3 dB [grados]
    gmax = g[i]                      # ganancia maxima simulada [dBi]

    # 2b) Patron en 2D (theta x phi) para integrar la esfera y obtener D.
    #     U(theta,phi) ~ potencia; D = 4*pi*Umax / (int U dOmega).
    th2, ph2, g2 = patron(f0_mhz, L, seg, radio, n_theta=91, n_phi=args.n_phi,
                          delta_theta=2, delta_phi=5)
    # Convertir ganancia [dBi] a potencia lineal y reacomodar en matriz (th x ph).
    U = 10 ** (g2 / 10).reshape(len(np.unique(th2)), -1)
    # Elemento de angulo solido: dOmega = sin(theta) dtheta dphi.
    w = np.sin(np.deg2rad(np.unique(th2)))[:, None]
    # Potencia radiada proporcional a la integral discreta (suma) de U dOmega.
    Prad = (U * w).sum() * np.deg2rad(2) * np.deg2rad(5)
    D = 4 * np.pi * U.max() / Prad      # directividad (lineal)
    D_dBi = 10 * np.log10(D)            # directividad [dBi]

    # Eficiencia = ganancia/directividad; apertura efectiva Ae = lambda^2 G/(4pi).
    eta = 10 ** ((gmax - D_dBi) / 10)
    Ae = lam ** 2 * D / (4 * np.pi)

    print(f"\n[2] Patron (plano E, phi=0): HPBW = {hpbw:.1f} deg   Gmax = {gmax:.2f} dBi")
    print(f"    Directividad (integrada) = {D_dBi:.2f} dBi")
    print(f"    Eficiencia eta = G/D = {eta:.3f}")
    print(f"    Apertura efectiva Ae = lambda^2 G/(4 pi) = {Ae:.4f} m^2 = {Ae/lam**2:.3f} lambda^2")

    # ------------------------------------------------------------------
    # 3) Comparacion simulacion vs. teoria (referencia L = lambda/2)
    # ------------------------------------------------------------------
    print("\n[3] Comparacion simulacion vs. teoria (dipolo lambda/2)")
    print(f"    {'Parametro':<26}{'Simulado':>12}{'Teoria':>12}")
    filas = [
        ("Directividad D0 (dBi)", f"{D_dBi:.2f}", f"{TEORIA['D0_dBi']:.2f}"),
        ("HPBW (grados)", f"{hpbw:.1f}", f"{TEORIA['HPBW_deg']:.1f}"),
        ("R a resonancia (ohm)", f"{R_res:.1f}", f"{TEORIA['Rrad_ohm']:.1f}"),
        ("X a f0 (ohm)", f"{Z0f.imag:.1f}", f"+{TEORIA['X_ohm']:.1f}"),
        ("Ae (lambda^2)", f"{Ae/lam**2:.3f}", f"{TEORIA['Ae_lambda2']:.2f}"),
        ("SWR en resonancia", f"{swr_res:.2f}", f"{TEORIA['SWR_res']:.2f}"),
    ]
    for nom, sim, teo in filas:
        print(f"    {nom:<26}{sim:>12}{teo:>12}")

    # ------------------------------------------------------------------
    # 4) Figuras
    # ------------------------------------------------------------------
    # (a) Impedancia de entrada R(f) y X(f).
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(freqs, Z.real, 'b', label='R (ohm)')
    ax.plot(freqs, Z.imag, 'r--', label='X (ohm)')
    ax.axhline(0, color='k', lw=0.5)
    ax.axvline(f_res, color='g', ls=':', label=f'resonancia {f_res:.0f} MHz')
    ax.set_xlabel('Frecuencia [MHz]'); ax.set_ylabel('Impedancia [ohm]')
    ax.set_title('Impedancia de entrada del dipolo (NEC2)')
    ax.legend(); ax.grid(alpha=0.3); fig.tight_layout()
    if not use_screen:               # solo se guarda si NO se muestra en pantalla
        fig.savefig('dipolo_t2_impedancia.png', dpi=150)

    # (b) Patron en el plano E, comparado con la expresion teorica.
    fig2, ax2 = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})
    # Se duplica el corte (0..180 y 180..0) para cerrar la figura polar.
    tth = np.deg2rad(np.concatenate([th, th[::-1]]))
    gg = np.concatenate([g, g[::-1]])
    ax2.plot(tth, gg, 'b', lw=1.5, label='NEC2')
    # Patron teorico normalizado (solo valido para L=lambda/2).
    F = np.cos(np.pi/2 * np.cos(tth)) / np.maximum(np.sin(tth), 1e-9)
    ax2.plot(tth, 10*np.log10(F**2) + TEORIA['D0_dBi'], 'r--', lw=1,
             label='teoria cos(pi/2 cos t)/sin t')
    ax2.set_theta_zero_location('N'); ax2.set_ylim(-30, 5)
    ax2.set_title('Patron (dB) - plano E'); ax2.legend(loc='lower left', fontsize=8)
    fig2.tight_layout()
    if not use_screen:
        fig2.savefig('dipolo_t2_patron.png', dpi=150)

    # (c) SWR en funcion de la frecuencia (marca el criterio SWR <= 2).
    fig3, ax3 = plt.subplots(figsize=(8, 4))
    swr_f = np.array([gamma_swr(z, z0)[1] for z in Z])
    ax3.plot(freqs, swr_f, 'b', label=f'SWR (Z0={z0:.0f} ohm)')
    ax3.axhline(2, color='orange', ls='--', label='SWR = 2')
    ax3.axvline(f_res, color='g', ls=':', label=f'{f_res:.0f} MHz')
    ax3.set_xlabel('Frecuencia [MHz]'); ax3.set_ylabel('SWR')
    ax3.set_title('SWR del dipolo'); ax3.legend(); ax3.grid(alpha=0.3)
    fig3.tight_layout()
    if not use_screen:
        fig3.savefig('dipolo_t2_swr.png', dpi=150)

    # (d) Archivo .nec para 4nec2 / xnec2c (solo si se pide con --nec).
    if args.nec:
        escribir_nec('dipolo_t2.nec', f0_mhz, L, radio, seg)
        print("[nec]     dipolo_t2.nec (para 4nec2 / xnec2c)")

    # ------------------------------------------------------------------
    # 5) Mostrar en pantalla o guardar en archivos
    # ------------------------------------------------------------------
    if use_screen:
        # Hay pantalla y se pidio -s/--show: mostrar las figuras.
        print("\n[figuras] mostrando en pantalla (cierre las ventanas para terminar)...")
        plt.show()
    else:
        # Guardar en PNG (caso por defecto, o si no hay backend interactivo).
        if args.show:
            print(f"\n[aviso] backend '{matplotlib.get_backend()}' no interactivo: "
                  "se guardan las figuras en archivos.")
        print("[figuras] guardadas: dipolo_t2_impedancia.png, dipolo_t2_patron.png, dipolo_t2_swr.png")
        if not matplotlib.is_interactive():
            plt.close('all')


if __name__ == '__main__':
    main(parse_args())
