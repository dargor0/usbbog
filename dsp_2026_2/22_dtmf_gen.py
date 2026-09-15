#!/usr/bin/env python3
"""22_dtmf_gen.py

Tema 3 - Generador de secuencias DTMF.
================================================================================
OBJETIVO
--------
Generar un archivo WAV (o reproducir por el parlante) que contenga una
secuencia de tonos DTMF definida por una cadena de texto.

DEPENDENCIAS
------------
  - numpy, scipy (instalacion estandar del curso)
  - sounddevice (para reproduccion por parlante):
        pip install sounddevice
    Si no se necesita reproduccion en vivo, puede omitirse y usar solo -o.

ALGORITMO
---------
1. Parsear la cadena de entrada, filtrando solo caracteres DTMF validos.
2. Para cada caracter, obtener de la tabla DTMF sus dos frecuencias
   (una de la "fila" baja y una de la "columna" alta).
3. Generar un tono como la suma de dos senos: x(t)=A/2*(sin(2*pi*f1*t)+sin(2*pi*f2*t)).
   La amplitud de cada seno es A/2 para que el pico de la suma sea A.
4. Concatenar cada tono con un intervalo de silencio.
5. Escribir la senal a WAV (siempre disponible) o reproducirla con sounddevice.

REFERENCIAS (laminas Tema 3)
----------------------------
  - Cada tecla DTMF usa dos tonos simultaneos: una frecuencia de fila
    (grupo bajo: 697, 770, 852, 941 Hz) y una de columna (grupo alto:
    1209, 1336, 1477, 1633 Hz).
  - Muestreo tipico: fs = 8000 Hz (cumple Nyquist para las frecuencias usadas).

Ejemplos:
  python3 22_dtmf_gen.py "123*#ABCD"
  python3 22_dtmf_gen.py "1234567890" -o tonos.wav
  python3 22_dtmf_gen.py "555_1234" --tone-duration 200 --silence-duration 100
"""

import argparse
import sys

import numpy as np
from scipy.io import wavfile

# ------------------------------------------------------------------------------
# Verificar que sounddevice esta instalado (requerido para reproduccion en vivo)
# ------------------------------------------------------------------------------
try:
    import sounddevice as sd
except ImportError:
    print(
        "Error: el paquete 'sounddevice' no esta instalado.\n"
        "Instalelo con:  pip install sounddevice\n"
        "O use -o para guardar en WAV sin reproducir.",
        file=sys.stderr
    )
    sd = None

# ============================================================================
# TABLA DTMF
# ============================================================================
# Cada tecla se define por una pareja (fila, columna).
# Filas bajas:    697,  770,  852,  941  Hz
# Columnas altas: 1209, 1336, 1477, 1633 Hz
# ============================================================================
DTMF_MAP = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477), 'A': (697, 1633),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477), 'B': (770, 1633),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477), 'C': (852, 1633),
    '*': (941, 1209), '0': (941, 1336), '#': (941, 1477), 'D': (941, 1633),
}

VALID_KEYS = set(DTMF_MAP.keys())   # conjunto para busqueda rapida


def generate_tone(f1, f2, duration_ms, fs, amplitude=0.5):
    """
    Genera un tono DTMF como suma de dos senos puros.

    Parametros
    ----------
    f1, f2 : float
        Frecuencias de fila y columna (Hz).
    duration_ms : int
        Duracion del tono en milisegundos.
    fs : int
        Frecuencia de muestreo (Hz).
    amplitude : float
        Amplitud pico deseada del tono resultante.

    Retorna
    -------
    tone : ndarray(float32)
        Vector con las muestras del tono.

    Nota
    ----
    Cada seno individual tiene amplitud A/2; al sumarlos, el pico
    maximo de la senal compuesta es A (cuando ambas componentes
    alcanzan su maximo simultaneamente).
    """
    # Calcular el numero de muestras: duracion[s] * fs[muestras/s]
    samples = int(fs * duration_ms / 1000)

    # Vector de tiempo discreto: t[n] = n/fs, con n = 0 .. samples-1
    t = np.arange(samples) / fs

    # Seno 1 (fila) + Seno 2 (columna), cada uno a la mitad de la amplitud total
    tone = (amplitude / 2.0) * (
        np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)
    )

    return tone.astype(np.float32)


def generate_silence(duration_ms, fs):
    """
    Genera un segmento de silencio (ceros).

    Parametros
    ----------
    duration_ms : int
        Duracion del silencio en milisegundos.
    fs : int
        Frecuencia de muestreo (Hz).

    Retorna
    -------
    silence : ndarray(float32)
        Vector de ceros.
    """
    return np.zeros(int(fs * duration_ms / 1000), dtype=np.float32)


def build_signal(string, fs=8000, tone_ms=150, silence_ms=50,
                 pause_ms=300, amplitude=0.5):
    """
    Construye la senal completa a partir de una cadena DTMF.

    Para cada caracter valido se genera un tono seguido de silencio.
    El caracter '_' inserta una pausa fija de duracion 'pause_ms'.
    El ultimo silencio se descarta para no dejar cola muerta.

    Parametros
    ----------
    string : str
        Cadena con los caracteres DTMF a generar.
    fs : int
        Frecuencia de muestreo (Hz).
    tone_ms : int
        Duracion de cada tono (ms).
    silence_ms : int
        Duracion del silencio entre tonos (ms).
    pause_ms : int
        Duracion de la pausa fija insertada por '_' (ms).
    amplitude : float
        Amplitud pico de cada tono.

    Retorna
    -------
    signal : ndarray(float32)
        Senal completa concatenada.
    """
    parts = []   # lista de fragmentos (tonos + silencios)

    for ch in string.upper():
        if ch == '_':
            # '_' = pausa fija entre grupos de digitos
            parts.append(generate_silence(pause_ms, fs))
        elif ch in VALID_KEYS:
            f1, f2 = DTMF_MAP[ch]     # frecuencias (fila, columna)
            parts.append(generate_tone(f1, f2, tone_ms, fs, amplitude))
            parts.append(generate_silence(silence_ms, fs))
        else:
            # Caracter no valido: se ignora silenciosamente
            continue

    # Si no quedo nada, retornar vector vacio
    if not parts:
        return np.array([], dtype=np.float32)

    # Quitar el ultimo silencio colgante para que la senal termine
    # en un tono activo y no en silencio.
    if len(parts) > 1:
        parts = parts[:-1]

    # Concatenar todos los fragmentos en un solo vector
    return np.concatenate(parts)


def play_audio(signal, fs):
    """
    Reproduce la senal por el parlante usando sounddevice.

    Parametros
    ----------
    signal : ndarray
        Senal a reproducir (valores float, tipicamente [-1, 1]).
    fs : int
        Frecuencia de muestreo (Hz).
    """
    if sd is not None:
        sd.play(signal.astype(np.float32), fs)
        sd.wait()   # bloquear hasta que termine la reproduccion
    else:
        sys.exit(1)


def main():
    # Captura de argumentos
    parser = argparse.ArgumentParser(
        description='Generador de secuencias DTMF (tonos telefonicos)'
    )
    parser.add_argument(
        'string',
        help='Cadena DTMF a generar (0-9, A-D, #, *). '
             "Use '_' para insertar una pausa fija entre grupos."
    )
    parser.add_argument(
        '-o', '--output',
        help='Ruta del archivo WAV de salida (si se omite, reproduce el audio)'
    )
    parser.add_argument(
        '--fs', type=int, default=8000,
        help='Frecuencia de muestreo en Hz (default: 8000)'
    )
    parser.add_argument(
        '-t', '--tone-duration', type=int, default=150,
        help='Duracion de cada tono en ms (default: 150)'
    )
    parser.add_argument(
        '-s', '--silence-duration', type=int, default=50,
        help='Duracion del silencio entre tonos en ms (default: 50)'
    )
    parser.add_argument(
        '-p', '--pause-duration', type=int, default=300,
        help="Duracion de la pausa fija '_' en ms (default: 300)"
    )
    parser.add_argument(
        '-a', '--amplitude', type=float, default=0.5,
        help='Amplitud pico del tono, entre 0 y 1 (default: 0.5)'
    )
    args = parser.parse_args()

    # Filtrar caracteres validos: DTMF + '_' (pausa)
    valid_chars = [c for c in args.string.upper() if c in VALID_KEYS or c == '_']
    if not valid_chars or all(c == '_' for c in valid_chars):
        print("Error: la cadena no contiene caracteres DTMF validos.",
              file=sys.stderr)
        sys.exit(1)

    # Construir la senal completa
    signal = build_signal(
        ''.join(valid_chars),
        args.fs,
        args.tone_duration,
        args.silence_duration,
        args.pause_duration,
        args.amplitude
    )
    duration = len(signal) / args.fs

    # ========================================================================
    # SALIDA: WAV o reproduccion directa
    # ========================================================================
    if args.output:
        # Guardar a archivo WAV
        int_signal = np.clip(signal, -1.0, 1.0)
        wavfile.write(
            args.output,
            args.fs,
            (int_signal * 32767).astype(np.int16)
        )
        print(f"Guardado: {args.output}  ({duration:.3f} s, {len(valid_chars)} tonos)")
    else:
        # Reproducir directamente por el parlante
        play_audio(signal, args.fs)
        print(f"Reproducido: {duration:.3f} s, {len(valid_chars)} tonos")


if __name__ == '__main__':
    main()
