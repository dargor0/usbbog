% 23_dtmf_goertzel.m
% Tema 3 - Decodificador de secuencias DTMF usando Goertzel.
% ================================================================================
% OBJETIVO
% --------
% Version alternativa de 23_dtmf_dec.m que usa el algoritmo de Goertzel
% (en lugar de FFT completa) para detectar las frecuencias DTMF.
%
% DEPENDENCIAS
% ------------
%   - MATLAB con Signal Processing Toolbox (funcion goertzel)
%   - La funcion goertzel NO esta disponible en Octave
%
% POR QUE GOERTZEL?
% -----------------
% La FFT calcula N/2+1 bins simultaneamente (O(N log N)).
% Goertzel calcula un unico bin exacto con un filtro IIR de 2do orden (O(N)).
% Para DTMF solo necesitamos 8 frecuencias especificas (4 filas + 4 columnas),
% por lo que 8 x O(N) Goertzel puede ser mas eficiente que una FFT completa.
%
% ALGORITMO
% ---------
% 1. Leer el archivo WAV (fs + muestras), normalizando a [-1, 1].
% 2. Segmentar la senal en ventanas (frames) con traslape (hop).
% 3. Para cada frame activo (energia > umbral):
%    a) Ejecutar goertzel(frame, k) en las 8 frecuencias DTMF.
%       Los indices k se calculan como k = round(freq*N/fs) + 1 (1-based).
%    b) Seleccionar la amplitud maxima del grupo bajo (fila) y del grupo
%       alto (columna).
%    c) Clasificar la pareja (fila, columna) en tecla DTMF.
% 4. Agrupar frames consecutivos que detecten la misma tecla.
% 5. Insertar espacios cuando hay silencios prolongados.
%
% USO
% ---
% Edite las constantes en la seccion "PARAMETROS" y ejecute en MATLAB:
%   run('23_dtmf_goertzel.m')
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
% DECODIFICACION DTMF CON GOERTZEL
% ============================================================================
frame_len = round(FS * FRAME_MS / 1000);
hop_len   = round(FS * HOP_MS / 1000);

% Frecuencias unicas a evaluar (4 filas + 4 columnas)
rows_unique = unique(DTMF_ROWS);
cols_unique = unique(DTMF_COLS);
all_freqs = [rows_unique, cols_unique];

% Calcular indices de bin para goertzel (MATLAB usa indices 1-based)
% frecuencia del bin k:  f_k = (k-1) * fs / N
% despejando k:         k = round(freq * N / fs) + 1
bin_indices = round(all_freqs * frame_len / FS) + 1;
bin_indices = max(1, min(frame_len, bin_indices));   % clamp a [1, N]

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
        % Ejecutar goertzel de MATLAB en las 8 frecuencias DTMF (vectorizado)
        d = goertzel(frame, bin_indices);
        amps = abs(d);

        % Separar amplitudes de filas (bajas) y columnas (altas)
        row_amps = amps(1:length(rows_unique));
        col_amps = amps(length(rows_unique)+1:end);

        % Seleccionar la frecuencia con mayor amplitud en cada grupo
        [~, row_idx] = max(row_amps);
        [~, col_idx] = max(col_amps);

        f_low = rows_unique(row_idx);
        f_high = cols_unique(col_idx);

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
