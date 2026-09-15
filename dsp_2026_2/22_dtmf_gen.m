% 22_dtmf_gen.m
% Tema 3 - Generador de secuencias DTMF.
% ================================================================================
% OBJETIVO
% --------
% Generar un archivo WAV (o reproducir por el parlante) que contenga una
% secuencia de tonos DTMF definida por una cadena de texto.
%
% DEPENDENCIAS
% ------------
%   - Octave/MATLAB (funciones sound, audiowrite, audioread)
%
% ALGORITMO
% ---------
% 1. Parsear la cadena de entrada, filtrando solo caracteres DTMF validos.
% 2. Para cada caracter, obtener de la tabla DTMF sus dos frecuencias
%    (una de la "fila" baja y una de la "columna" alta).
% 3. Generar un tono como la suma de dos senos: x(t)=A/2*(sin(2*pi*f1*t)+sin(2*pi*f2*t)).
% 4. Concatenar cada tono con un intervalo de silencio.
% 5. Escribir la senal a WAV o reproducirla con sound().
%
% USO
% ---
% Edite las constantes en la seccion "PARAMETROS" y ejecute:
%   octave-cli 22_dtmf_gen.m
% ================================================================================

clear; close all; clc;

% ============================================================================
% PARAMETROS (editar aqui)
% ============================================================================
STRING       = '123A*#BCD';   % cadena DTMF a generar (0-9, A-D, #, *)
                              % use '_' para pausas fijas
OUTPUT_FILE  = '';            % archivo WAV de salida ('' = reproducir)
FS           = 8000;          % frecuencia de muestreo (Hz)
TONE_MS      = 150;           % duracion del tono (ms)
SILENCE_MS   = 50;            % silencio entre tonos (ms)
PAUSE_MS     = 300;           % pausa fija para '_' (ms)
AMPLITUDE    = 0.5;           % amplitud pico del tono

% ============================================================================
% TABLA DTMF
% ============================================================================
DTMF_KEYS = {'1','2','3','A','4','5','6','B','7','8','9','C','*','0','#','D'};
DTMF_ROWS = [697, 697, 697, 697, 770, 770, 770, 770, 852, 852, 852, 852, 941, 941, 941, 941];
DTMF_COLS = [1209,1336,1477,1633, 1209,1336,1477,1633, 1209,1336,1477,1633, 1209,1336,1477,1633];

% ============================================================================
% FUNCIONES AUXILIARES
% ============================================================================

function tone = generate_tone(f1, f2, duration_ms, fs, amplitude)
    % Genera un tono DTMF como suma de dos senos puros.
    samples = round(fs * duration_ms / 1000);
    n = 0:samples-1;
    t = n / fs;
    tone = (amplitude / 2) * (sin(2*pi*f1*t) + sin(2*pi*f2*t));
end

function silence = generate_silence(duration_ms, fs)
    % Genera un segmento de silencio (ceros).
    silence = zeros(1, round(fs * duration_ms / 1000));
end

function idx = find_key_index(ch, keys)
    % Busca el indice de un caracter en la tabla DTMF.
    idx = 0;
    for k = 1:length(keys)
        if strcmp(keys{k}, ch)
            idx = k;
            return;
        end
    end
end

% ============================================================================
% CONSTRUIR LA SENAL
% ============================================================================
parts = {};
str_upper = upper(STRING);

for i = 1:length(str_upper)
    ch = str_upper(i);
    if ch == '_'
        % '_' = pausa fija entre grupos de digitos
        parts{end+1} = generate_silence(PAUSE_MS, FS);
    else
        idx = find_key_index(ch, DTMF_KEYS);
        if idx > 0
            f1 = DTMF_ROWS(idx);
            f2 = DTMF_COLS(idx);
            parts{end+1} = generate_tone(f1, f2, TONE_MS, FS, AMPLITUDE);
            parts{end+1} = generate_silence(SILENCE_MS, FS);
        end
    end
end

% Si no hay partes, terminar
if isempty(parts)
    fprintf('Error: la cadena no contiene caracteres DTMF validos.\n');
    return;
end

% Quitar el ultimo silencio colgante
if length(parts) > 1 && all(parts{end} == 0)
    parts = parts(1:end-1);
end

% Concatenar todas las partes
signal = cell2mat(parts);
duration = length(signal) / FS;

% ============================================================================
% SALIDA: WAV o reproduccion directa
% ============================================================================
if ~isempty(OUTPUT_FILE)
    % Guardar a archivo WAV (escalar a int16)
    signal_clipped = max(min(signal, 1), -1);
    audiowrite(OUTPUT_FILE, signal_clipped, FS);
    fprintf('Guardado: %s  (%.3f s, %d tonos)\n', OUTPUT_FILE, duration, sum(cellfun(@(p) ~all(p==0), parts)));
else
    % Reproducir directamente por el parlante
    sound(signal, FS);
    fprintf('Reproducido: %.3f s, %d tonos\n', duration, sum(cellfun(@(p) ~all(p==0), parts)));
end
