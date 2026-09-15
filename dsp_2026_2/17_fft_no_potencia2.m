% 17_fft_no_potencia2.m
% Tema 3 - FFT con N que NO es potencia de 2.
% Ejecutar:  octave-cli 17_fft_no_potencia2.m
%
% Referencias a las laminas del Tema 3:
%   - La FFT maneja N arbitrario; las potencias de 2 son las mas rapidas.

clear; close all; clc;

fs = 8000; f0 = 1000; N = 1000;   % N no potencia de 2
n = 0:N-1;
x = sin(2*pi*f0*n/fs);

X = fft(x);              % funciona con N=1000
N2 = 2^nextpow2(N);      % siguiente potencia de 2 (1024)
X2 = fft(x, N2);         % relleno con ceros

f1 = (0:N-1)*fs/N;
f2 = (0:N2-1)*fs/N2;

fprintf('============================================================\n');
fprintf('FFT CON N NO POTENCIA DE 2\n');
fprintf('============================================================\n');
fprintf('N = %d (no potencia de 2); siguiente potencia = %d\n', N, N2);
fprintf('resolucion sin padding: df = %.2f Hz\n', fs/N);
fprintf('resolucion con padding: df = %.2f Hz\n', fs/N2);

% Indices para el rango 975–1025 Hz
idx1 = find(f1 >= 975 & f1 <= 1025);
idx2 = find(f2 >= 975 & f2 <= 1025);

figure;
subplot(2,1,1); plot(f1(idx1), abs(X(idx1))*2/N);
title(sprintf('fft(x) con N=%d', N)); xlabel('f [Hz]'); xlim([975 1025]); grid on;
subplot(2,1,2); plot(f2(idx2), abs(X2(idx2))*2/N);
title(sprintf('fft(x, N2=%d) con zero-padding', N2)); xlabel('f [Hz]'); xlim([975 1025]); grid on;
