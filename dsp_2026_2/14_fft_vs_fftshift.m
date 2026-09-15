% 14_fft_vs_fftshift.m
% Tema 3 - FFT vs. fftshift (espectro de 0..fs vs. centrado en 0).
% Ejecutar:  octave-cli 14_fft_vs_fftshift.m
%
% Referencias a las laminas del Tema 3:
%   - "Espectro simetrico: centrado en 0 vs. 0-N"

clear; close all; clc;

fs = 8000; f0 = 1000; N = 1024;
n = 0:N-1;
x = sin(2*pi*f0*n/fs);

X = fft(x);
Xc = fftshift(X);

f1 = (0:N-1)*fs/N;                 % 0 .. fs
f2 = ((0:N-1) - N/2)*fs/N;         % -fs/2 .. fs/2

fprintf('============================================================\n');
fprintf('FFT vs. FFT-SHIFT\n');
fprintf('============================================================\n');
[~, k1] = max(abs(X));   fprintf('fft:      pico en bin %3d -> %7.1f Hz\n', k1-1, f1(k1));
[~, k2] = max(abs(Xc));  fprintf('fftshift: pico en bin %3d -> %7.1f Hz\n', k2-1, f2(k2));

figure;
subplot(2,1,1); plot(f1, abs(X));
title('fft(x): bins 0..N-1 (frecuencias 0..fs)'); xlabel('f [Hz]'); grid on;
subplot(2,1,2); plot(f2, abs(Xc));
title('fftshift(fft(x)): centrado en 0 (-fs/2..fs/2)'); xlabel('f [Hz]'); grid on;
