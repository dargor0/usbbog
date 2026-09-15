% 18_fft_sin_fs.m
% Tema 3 - FFT con y sin frecuencia de muestreo.
% Ejecutar:  octave-cli 18_fft_sin_fs.m
%
% Referencias a las laminas del Tema 3:
%   - "Interpretacion de las frecuencias (bins)":
%         sin fs: bins k=0..N-1;  con fs: f_k = k*fs/N.

clear; close all; clc;

fs = 8000; f0 = 1000; N = 64;
n = 0:N-1;
x = sin(2*pi*f0*n/fs);

X = fft(x);
k = 0:N-1;
f = k*fs/N;          % frecuencias en Hz
w = 2*pi*k/N;        % frecuencias normalizadas (rad/muestra)

[~, kmax] = max(abs(X(1:N/2)));
fprintf('============================================================\n');
fprintf('FFT CON Y SIN FRECUENCIA DE MUESTREO\n');
fprintf('============================================================\n');
fprintf('pico en el bin k = %d\n', kmax-1);
fprintf('sin fs:  omega = %.3f rad/muestra\n', w(kmax));
fprintf('con fs:  f = %.1f Hz (esperado %.0f Hz)\n', f(kmax), f0);

figure;
subplot(3,1,1); stem(k, abs(X)); title('Eje en bins k (sin fs)'); xlabel('k'); grid on;
subplot(3,1,2); stem(w, abs(X)); title('Eje en \omega (rad/muestra)'); xlabel('\omega [rad/muestra]'); grid on;
subplot(3,1,3); stem(f, abs(X)); title('Eje en Hz (con fs)'); xlabel('f [Hz]'); grid on;
