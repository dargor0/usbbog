% 21_dtmf.m
% Tema 3 - Identificacion de tonos DTMF con la FFT.
% Ejecutar:  octave-cli 21_dtmf.m
%
% Referencias a las laminas del Tema 3:
%   - La FFT permite identificar las dos frecuencias de un tono DTMF.
%   - Tabla DTMF: filas 697,770,852,941 Hz; columnas 1209,1336,1477,1633 Hz.

clear; close all; clc;

fs = 8000; N = 800; t = (0:N-1)/fs;

fila = 770; columna = 1336;      % tono '5'
x = sin(2*pi*fila*t) + sin(2*pi*columna*t);

X = fft(x);
f = (0:N-1)*fs/N;
Xm = abs(X(1:N/2));

[~, i1] = max(Xm); Xm(i1) = 0;
[~, i2] = max(Xm);
frecs = sort([f(i1) f(i2)]);

fprintf('============================================================\n');
fprintf('IDENTIFICACION DE TONOS DTMF\n');
fprintf('============================================================\n');
fprintf('tono generado: fila %d + columna %d Hz\n', fila, columna);
fprintf('frecuencias detectadas: %.0f y %.0f Hz\n', frecs(1), frecs(2));

filas = [697 770 852 941];
cols  = [1209 1336 1477 1633];
teclas = ['1' '2' '3'; '4' '5' '6'; '7' '8' '9'; '*' '0' '#'];
[~, ri] = min(abs(filas - frecs(1)));
[~, ci] = min(abs(cols - frecs(2)));
if abs(filas(ri)-frecs(1))<50 && abs(cols(ci)-frecs(2))<50
  fprintf('tecla detectada: %s\n', teclas(ri,ci));
else
  fprintf('no se pudo mapear a una tecla\n');
end

figure;
plot(f(1:N/2), Xm); hold on;
plot([fila fila], ylim, 'r--'); plot([columna columna], ylim, 'g--');
title('Espectro del tono DTMF (dos picos)'); xlabel('f [Hz]'); grid on;
