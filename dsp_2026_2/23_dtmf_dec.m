% 23_dtmf_dec.m
% Tema 3 - Decodificador de secuencias DTMF.
% ================================================================================
% OBJETIVO
% --------
% Leer un archivo WAV y decodificar la secuencia de tonos DTMF presentes
% en el audio, imprimiendo la cadena correspondiente.
% Los espacios en la salida indican silencios prolongados o datos no
% reconocidos.
%
% DEPENDENCIAS
% ------------
%   - Octave/MATLAB (funciones audioread, fft)
%
% ALGORITMO
% ---------
% 1. Leer el archivo WAV (fs + muestras), normalizando a [-1, 1].
% 2. Segmentar la senal en ventanas (frames) con traslape (hop).
% 3. Para cada frame:
%    a) Calcular la energia promedio (x^2).
%    b) Si la energia supera un umbral, aplicar FFT al frame.
%    c) Buscar los dos picos dominantes en el rango DTMF (600-1700 Hz).
%    d) Clasificar los picos como (fila, columna) y mapear a tecla.
% 4. Agrupar frames consecutivos que detecten la misma tecla (estabilidad).
% 5. Insertar espacios cuando hay silencios prolongados.
%
% USO
% ---
% Edite las constantes en la seccion "PARAMETROS" y ejecute:
%   octave-cli 23_dtmf_dec.m
% ================================================================================

clear; close all; clc;

% ============================================================================
% PARAMETROS (editar aqui)
% ============================================================================
INPUT_FILE          = '/tmp/test_dtmf.wav';   % archivo WAV de entrada
FS                  = 8000;                    % frecuencia de muestreo (Hz)
FRAME_MS            = 50;                      % duracion del frame (ms)
HOP_MS              = 25;                      % salto entre frames (ms)
ENERGY_THRESHOLD    = 0.01;                    % umbral de energia
SILENCE_FRAMES      = 3;                       % frames de silencio para espacio
MIN_KEY_FRAMES      = 2;                       % frames minimos para aceptar tecla

% ============================================================================
% TABLA DTMF
% ============================================================================
DTMF_KEYS = {'1','2','3','A','4','5','6','B','7','8','9','C','*','0','#','D'};
DTMF_ROWS = [697, 697, 697, 697, 770, 770, 770, 770, 852, 852, 852, 852, 941, 941, 941, 941];
DTMF_COLS = [1209,1336,1477,1633, 1209,1336,1477,1633, 1209,1336,1477,1633, 1209,1336,1477,1633];

FREQ_TOL = 0.015;   % tolerancia relativa 1.5%

% ============================================================================
% FUNCIONES AUXILIARES
% ============================================================================

function [f_low, f_high] = find_two_peaks(mag, freqs, min_freq, max_freq)
    % Encuentra las dos frecuencias dominantes en el rango DTMF.
    valid = find(freqs >= min_freq & freqs <= max_freq);
    if length(valid) < 3
        f_low = []; f_high = []; return;
    end

    spectrum = mag(valid);
    freqs_v = freqs(valid);

    % Picos locales
    peaks_idx = [];
    for i = 2:length(spectrum)-1
        if spectrum(i) > spectrum(i-1) && spectrum(i) > spectrum(i+1)
            peaks_idx(end+1) = i;
        end
    end

    if length(peaks_idx) < 2
        f_low = []; f_high = []; return;
    end

    peak_vals = spectrum(peaks_idx);
    peak_freqs = freqs_v(peaks_idx);
    [~, order] = sort(peak_vals, 'descend');

    f_low = min(peak_freqs(order(1)), peak_freqs(order(2)));
    f_high = max(peak_freqs(order(1)), peak_freqs(order(2)));
end

function key = classify_dtmf(f_low, f_high, dtmf_rows, dtmf_cols, dtmf_keys, tol)
    % Clasifica un par de frecuencias en una tecla DTMF.
    if isempty(f_low) || isempty(f_high)
        key = ''; return;
    end

    [~, r_idx] = min(abs(dtmf_rows - f_low));
    [~, c_idx] = min(abs(dtmf_cols - f_high));
    row = dtmf_rows(r_idx);
    col = dtmf_cols(c_idx);

    if abs(row - f_low)/row > tol || abs(col - f_high)/col > tol
        key = ''; return;
    end

    for n = 1:length(dtmf_keys)
        if dtmf_rows(n) == row && dtmf_cols(n) == col
            key = dtmf_keys{n}; return;
        end
    end
    key = '';
end

% ============================================================================
% LEER ARCHIVO WAV
% ============================================================================
[signal_raw, fs_file] = audioread(INPUT_FILE);
if size(signal_raw, 2) > 1
    signal = mean(signal_raw, 2);   % mono
else
    signal = signal_raw;
end
signal = signal(:)';

if fs_file ~= FS
    fprintf('Advertencia: fs del archivo (%.0f) difiere de FS (%.0f)\n', fs_file, FS);
end

% ============================================================================
% DECODIFICACION DTMF
% ============================================================================
frame_len = round(FS * FRAME_MS / 1000);
hop_len   = round(FS * HOP_MS / 1000);

segments = {};
curr_type = 'silence';
curr_val = '';
curr_count = 0;

i = 1;
while i + frame_len - 1 <= length(signal)
    frame = signal(i:i+frame_len-1);
    energy = mean(frame.^2);

    if energy < ENERGY_THRESHOLD
        key = '';
    else
        X = fft(frame);
        mag = abs(X(1:frame_len/2));
        freqs = (0:frame_len/2-1) * FS / frame_len;
        [f_low, f_high] = find_two_peaks(mag, freqs, 600, 1700);
        key = classify_dtmf(f_low, f_high, DTMF_ROWS, DTMF_COLS, DTMF_KEYS, FREQ_TOL);
    end

    if ~isempty(key)
        seg_type = 'key';
        seg_val = key;
    else
        seg_type = 'silence';
        seg_val = '';
    end

    if strcmp(seg_type, curr_type) && strcmp(seg_val, curr_val)
        curr_count = curr_count + 1;
    else
        if strcmp(curr_type, 'key') && curr_count >= MIN_KEY_FRAMES
            segments{end+1} = curr_val;
        elseif strcmp(curr_type, 'silence') && curr_count >= SILENCE_FRAMES
            segments{end+1} = ' ';
        end
        curr_type = seg_type;
        curr_val = seg_val;
        curr_count = 1;
    end

    i = i + hop_len;
end

% Vaciar ultimo segmento
if strcmp(curr_type, 'key') && curr_count >= MIN_KEY_FRAMES
    segments{end+1} = curr_val;
elseif strcmp(curr_type, 'silence') && curr_count >= SILENCE_FRAMES
    segments{end+1} = ' ';
end

% Concatenar e imprimir
decoded = strjoin(segments, '');
fprintf('%s\n', decoded);
