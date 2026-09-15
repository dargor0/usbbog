#!/usr/bin/env python3
"""23_dtmf_dec.py

Tema 3 - Decodificador de secuencias DTMF.
================================================================================
OBJETIVO
--------
Leer un archivo WAV (o grabar del microfono con sounddevice) y decodificar
la secuencia de tonos DTMF presentes en el audio, imprimiendo la cadena
correspondiente. Los espacios en la salida indican silencios prolongados o
datos no reconocidos.

DEPENDENCIAS
------------
  - numpy, scipy (instalacion estandar del curso)
  - sounddevice (para grabar desde el microfono):
        pip install sounddevice
    Si solo usa archivos WAV (-i), sounddevice no es necesario.

ALGORITMO
---------
1. Leer el archivo WAV (fs + muestras), normalizando a float32 en [-1, 1].
2. Segmentar la senal en ventanas (frames) con traslape (hop).
3. Para cada frame:
   a) Calcular la energia promedio (x^2).
   b) Si la energia supera un umbral, aplicar FFT al frame.
   c) Buscar los dos picos dominantes en el rango DTMF (600-1700 Hz).
   d) Clasificar los picos como (fila, columna) y mapear a tecla.
4. Agrupar frames consecutivos que detecten la misma tecla (estabilidad).
5. Insertar espacios cuando hay silencios prolongados.

REFERENCIAS (laminas Tema 3)
----------------------------
  - DTMF usa dos frecuencias simultaneas: una baja (fila) y una alta (columna).
  - La FFT permite identificar las frecuencias presentes en cada intervalo.
  - Con fs = 8000 Hz y frame de 50 ms se obtienen 400 muestras/frame;
    la resolucion es df = fs/N = 8000/400 = 20 Hz, suficiente para
    discriminar las frecuencias DTMF (separacion minima ~70 Hz).

Ejemplos:
  python3 23_dtmf_dec.py -i tonos.wav
  python3 23_dtmf_dec.py --record --duration 5
  python3 23_dtmf_dec.py -i tonos.wav --threshold 0.005
"""

import argparse
import sys
import tempfile
import os

import numpy as np
from scipy.io import wavfile

# ------------------------------------------------------------------------------
# Verificar que sounddevice esta instalado (solo se necesita para --record)
# ------------------------------------------------------------------------------
try:
    import sounddevice as sd
except ImportError:
    # No forzar la salida aqui: si el usuario solo usa -i, no necesita sd.
    # Se verificara en tiempo de ejecucion si se solicita --record.
    sd = None

# ============================================================================
# TABLA DTMF (misma que en el generador)
# ============================================================================
# Filas bajas:    697,  770,  852,  941  Hz
# Columnas altas: 1209, 1336, 1477, 1633 Hz
# ============================================================================
DTMF_MAP = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477), 'A': (697, 1633),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477), 'B': (770, 1633),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477), 'C': (852, 1633),
    '*': (941, 1209), '0': (941, 1336), '#': (941, 1477), 'D': (941, 1633),
}

# Diccionario inverso: dada una tupla (fila, columna) devuelve la tecla
DTMF_REVERSE = {v: k for k, v in DTMF_MAP.items()}

# Arrays NumPy con las frecuencias para busqueda rapida
DTMF_ROWS = np.array([697, 770, 852, 941])
DTMF_COLS = np.array([1209, 1336, 1477, 1633])

# Tolerancia relativa para coincidencia de frecuencia (1.5%).
# Si la frecuencia detectada se desvia mas de 1.5% de la teorica,
# se considera que no coincide y se rechaza la clasificacion.
FREQ_TOL = 0.015


def record_audio(duration_sec, fs=8000):
    """
    Graba audio desde el microfono usando sounddevice.

    Parametros
    ----------
    duration_sec : int
        Duracion de la grabacion en segundos.
    fs : int
        Frecuencia de muestreo (Hz).

    Retorna
    -------
    tmp_path : str
        Ruta al archivo WAV temporal generado.
    """
    if sd is None:
        print(
            "Error: el paquete 'sounddevice' no esta instalado.\n"
            "Instalelo con:  pip install sounddevice",
            file=sys.stderr
        )
        sys.exit(1)

    # Calcular numero de muestras a grabar
    samples = int(duration_sec * fs)

    print("Grabando... (presione Ctrl+C para cancelar)", file=sys.stderr)
    recording = sd.rec(samples, samplerate=fs, channels=1, dtype='float32')
    sd.wait()   # bloquear hasta que termine la grabacion

    # Guardar en WAV temporal
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        tmp_path = f.name

    # Convertir a int16 para WAV (escalar por 32767)
    int_rec = np.clip(recording.flatten(), -1.0, 1.0)
    wavfile.write(tmp_path, fs, (int_rec * 32767).astype(np.int16))

    return tmp_path


def read_wav(path):
    """
    Lee un archivo WAV y devuelve (fs, signal) normalizado a float32 en [-1, 1].

    Parametros
    ----------
    path : str
        Ruta al archivo WAV.

    Retorna
    -------
    fs : int
        Frecuencia de muestreo leida del archivo.
    signal : ndarray(float32)
        Senal normalizada al rango [-1, 1].

    Nota
    ----
    Si el archivo es estereo, se promedia a mono.
    Soporta int16 e int32; otros tipos se asumen ya flotantes.
    """
    fs, data = wavfile.read(path)

    # Si es estereo (2 canales), promediar a mono
    if data.ndim > 1:
        data = data.mean(axis=1)

    # Normalizar segun el tipo de dato original del WAV
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768.0
    elif data.dtype == np.int32:
        data = data.astype(np.float32) / 2147483648.0
    else:
        data = data.astype(np.float32)

    return fs, data


def find_two_peaks(mag, freqs, min_freq=600, max_freq=1700):
    """
    Encuentra las dos frecuencias dominantes dentro del rango DTMF.

    Parametros
    ----------
    mag : ndarray
        Magnitud del espectro |X[k]|.
    freqs : ndarray
        Eje de frecuencias correspondiente a cada bin de mag.
    min_freq, max_freq : float
        Rango de busqueda (Hz). Default 600-1700 cubre todas las frecuencias
        DTMF con margen de seguridad.

    Retorna
    -------
    f_low, f_high : float o None
        Las dos frecuencias detectadas (la menor y la mayor).
        Si no se encuentran al menos dos picos, retorna (None, None).

    Algoritmo
    ---------
    1. Filtrar el espectro al rango [min_freq, max_freq].
    2. Buscar picos locales (puntos mayores que sus vecinos inmediatos).
    3. Elegir los dos picos de mayor magnitud.
    4. Devolver el menor como frecuencia "baja" (fila) y el mayor como
       frecuencia "alta" (columna).
    """
    # Indices de las muestras dentro del rango DTMF
    valid = np.where((freqs >= min_freq) & (freqs <= max_freq))[0]
    if len(valid) < 3:
        # No hay suficientes puntos para detectar picos
        return None, None

    # Extraer sub-espectro valido
    spectrum = mag[valid]
    freqs_v = freqs[valid]

    # Deteccion de picos locales: un punto es pico si es mayor que
    # su vecino izquierdo y su vecino derecho.
    peaks_idx = []
    for i in range(1, len(spectrum) - 1):
        if spectrum[i] > spectrum[i - 1] and spectrum[i] > spectrum[i + 1]:
            peaks_idx.append(i)

    if len(peaks_idx) < 2:
        # Menos de dos picos: no se puede clasificar como DTMF
        return None, None

    # Seleccionar los 2 picos mas altos por magnitud
    peak_vals = spectrum[peaks_idx]
    peak_freqs = freqs_v[peaks_idx]
    order = np.argsort(peak_vals)[::-1]   # orden descendente

    # Separar en baja (fila) y alta (columna)
    f_low = min(peak_freqs[order[0]], peak_freqs[order[1]])
    f_high = max(peak_freqs[order[0]], peak_freqs[order[1]])
    return f_low, f_high


def classify_dtmf(f_low, f_high):
    """
    Clasifica un par de frecuencias (fila, columna) en una tecla DTMF.

    Parametros
    ----------
    f_low, f_high : float o None
        Frecuencia baja (fila) y alta (columna) detectadas.

    Retorna
    -------
    key : str o None
        La tecla DTMF correspondiente, o None si no hay coincidencia
        dentro de la tolerancia FREQ_TOL.

    Algoritmo
    ---------
    1. Buscar la fila teorica mas cercana a f_low.
    2. Buscar la columna teorica mas cercana a f_high.
    3. Verificar que ambas esten dentro de la tolerancia relativa FREQ_TOL.
    4. Buscar la tecla en DTMF_REVERSE[(fila, columna)].
    """
    if f_low is None or f_high is None:
        return None

    # Fila y columna mas cercanas (argumento del minimo absoluto)
    row = DTMF_ROWS[np.argmin(np.abs(DTMF_ROWS - f_low))]
    col = DTMF_COLS[np.argmin(np.abs(DTMF_COLS - f_high))]

    # Comprobar tolerancia relativa
    # Si la desviacion respecto a la frecuencia teorica supera FREQ_TOL,
    # se descarta la clasificacion (ruido, interferencia, etc.)
    if abs(row - f_low) / row > FREQ_TOL or abs(col - f_high) / col > FREQ_TOL:
        return None

    return DTMF_REVERSE.get((int(row), int(col)), None)


def decode_dtmf(signal, fs, frame_ms=50, hop_ms=25,
                energy_threshold=0.01, silence_frames=3, min_key_frames=2):
    """
    Decodifica una secuencia DTMF completa a partir de una senal en el tiempo.

    Parametros
    ----------
    signal : ndarray
        Senal de audio normalizada.
    fs : int
        Frecuencia de muestreo (Hz).
    frame_ms : int
        Duracion de cada ventana de analisis (ms). Con fs=8000 y 50 ms
        se obtienen 400 muestras; la resolucion FFT es df=fs/400=20 Hz.
    hop_ms : int
        Paso entre ventanas consecutivas (ms). Un hop del 50% (25 ms)
        proporciona buena cobertura temporal sin mucho solapamiento.
    energy_threshold : float
        Umbral de energia promedio (x^2) para considerar que hay actividad
        en el frame. Debajo de este valor se asume silencio.
    silence_frames : int
        Numero minimo de frames consecutivos de silencio para insertar
        un espacio en la salida.
    min_key_frames : int
        Numero minimo de frames consecutivos detectando la misma tecla
        para aceptarla (evita falsos positivos por ruido momentaneo).

    Retorna
    -------
    decoded_str : str
        Cadena decodificada. Puede contener espacios como separadores.

    Algoritmo paso a paso
    ---------------------
    1. Calcular longitud de frame y hop en muestras.
    2. Recorrer la senal con ventanas deslizantes (frame a frame).
    3. Para cada frame:
       a) Energia = mean(x^2). Si es baja -> silencio.
       b) Si la energia es alta, calcular FFT y buscar 2 picos.
       c) Clasificar picos como tecla DTMF.
    4. Mantener un estado (tipo actual, valor actual, contador de frames).
       Cuando cambia el estado, evaluar si el segmento anterior duro
       suficiente para emitir un caracter o un espacio.
    5. Al finalizar, vaciar el ultimo segmento pendiente.
    """
    # Convertir duraciones de ms a numero de muestras
    frame_len = int(fs * frame_ms / 1000)
    hop_len = int(fs * hop_ms / 1000)

    segments = []   # lista de caracteres y espacios detectados

    # Estado del segmentador (maquina de estados simple)
    curr_type = 'silence'   # 'key' o 'silence'
    curr_val = ''           # tecla detectada o ''
    curr_count = 0          # cuantos frames consecutivos lleva este estado

    i = 0
    while i + frame_len <= len(signal):
        # Extraer la ventana actual
        frame = signal[i:i + frame_len]

        # Energia promedio del cuadrado: estimador rapido de "actividad"
        energy = np.mean(frame ** 2)

        if energy < energy_threshold:
            # Frame muy silencioso: no hay tono DTMF
            key = None
        else:
            # Calcular FFT del frame y extraer magnitud (solo mitad positiva)
            X = np.fft.fft(frame)
            mag = np.abs(X[:frame_len // 2])

            # Eje de frecuencias para esta FFT: f_k = k * fs / N_frame
            freqs = np.arange(frame_len // 2) * fs / frame_len

            # Buscar las dos frecuencias dominantes
            f_low, f_high = find_two_peaks(mag, freqs)

            # Clasificar como tecla DTMF
            key = classify_dtmf(f_low, f_high)

        # Tipo y valor del frame actual
        seg_type = 'key' if key is not None else 'silence'
        seg_val = key if key is not None else ''

        if seg_type == curr_type and seg_val == curr_val:
            # Seguimos en el mismo estado: incrementar contador
            curr_count += 1
        else:
            # Cambio de estado: evaluar el segmento que termino
            if curr_type == 'key' and curr_count >= min_key_frames:
                # Hubo suficientes frames de la misma tecla: emitirla
                segments.append(curr_val)
            elif curr_type == 'silence' and curr_count >= silence_frames:
                # Silencio prolongado: emitir un espacio separador
                segments.append(' ')

            # Iniciar nuevo segmento con el estado actual
            curr_type = seg_type
            curr_val = seg_val
            curr_count = 1

        # Avanzar la ventana deslizante
        i += hop_len

    # ========================================================================
    # Vaciar el ultimo segmento pendiente al terminar la senal
    # ========================================================================
    if curr_type == 'key' and curr_count >= min_key_frames:
        segments.append(curr_val)
    elif curr_type == 'silence' and curr_count >= silence_frames:
        segments.append(' ')

    # Concatenar todos los segmentos en la cadena final
    return ''.join(segments)


def main():
    # ========================================================================
    # PARSING DE ARGUMENTOS (argparse)
    # ========================================================================
    parser = argparse.ArgumentParser(
        description='Decodificador de secuencias DTMF desde audio'
    )
    parser.add_argument(
        '-i', '--input',
        help='Ruta del archivo WAV de entrada'
    )
    parser.add_argument(
        '--record', action='store_true',
        help='Grabar audio desde el microfono (usa sounddevice)'
    )
    parser.add_argument(
        '--duration', type=int, default=5,
        help='Duracion de la grabacion en segundos (default: 5)'
    )
    parser.add_argument(
        '--fs', type=int, default=8000,
        help='Frecuencia de muestreo del audio (default: 8000)'
    )
    parser.add_argument(
        '--frame-ms', type=int, default=50,
        help='Duracion del frame de analisis en ms (default: 50)'
    )
    parser.add_argument(
        '--hop-ms', type=int, default=25,
        help='Salto entre frames consecutivos en ms (default: 25)'
    )
    parser.add_argument(
        '--threshold', type=float, default=0.01,
        help='Umbral de energia normalizada para detectar actividad (default: 0.01)'
    )
    args = parser.parse_args()

    # Validar que no se pidan ambas fuentes al tiempo
    if args.input and args.record:
        print(
            "Error: no puede usar --input y --record al mismo tiempo.",
            file=sys.stderr
        )
        sys.exit(1)

    # ========================================================================
    # ADQUISICION DE AUDIO (archivo o microfono)
    # ========================================================================
    tmp_path = None
    if args.record:
        tmp_path = record_audio(args.duration, args.fs)
        fs, signal = read_wav(tmp_path)
    elif args.input:
        fs, signal = read_wav(args.input)
    else:
        print("Error: proporcione --input o --record.", file=sys.stderr)
        sys.exit(1)

    # ========================================================================
    # DECODIFICACION DTMF
    # ========================================================================
    decoded = decode_dtmf(
        signal, fs,
        args.frame_ms,
        args.hop_ms,
        args.threshold
    )

    # Imprimir resultado (puede contener espacios)
    print(decoded)

    # Limpiar archivo temporal de grabacion si existe
    if tmp_path is not None and os.path.exists(tmp_path):
        os.remove(tmp_path)


if __name__ == '__main__':
    main()
