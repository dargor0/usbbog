% 13_fft_basico.m
% Tema 3 - Uso basico de la FFT.
% Ejecutar:  octave-cli 13_fft_basico.m
%
% Referencias a las laminas del Tema 3:
%   - "DFT: definicion y propiedades"
%   - "Interpretacion de las frecuencias (bins)": f_k = k*f_s/N

clear; close all; clc;

fs = 8000;         % frecuencia de muestreo [Hz]
f0 = 1000;         % frecuencia del seno [Hz]
N = 1024;          % numero de muestras (potencia de 2)
n = 0:N-1;
x = sin(2*pi*f0*n/fs);    % seno muestreado

X = fft(x);
f = (0:N-1)*fs/N;         % eje de frecuencia [Hz] (rango completo)

fprintf('============================================================\n');
fprintf('USO BASICO DE LA FFT\n');
fprintf('============================================================\n');
fprintf('fs = %d Hz, f0 = %d Hz, N = %d\n', fs, f0, N);
[~, kmax] = max(abs(X));
fprintf('pico en el bin %d -> %.0f Hz (esperado %.0f Hz)\n', kmax-1, f(kmax), f0);
fprintf('energia (Parseval): tiempo %.3f vs. frecuencia %.3f\n', ...
        sum(x.^2), sum(abs(X).^2)/N);

figure;
subplot(2,2,1); stem(n, x); title('x[n] = seno de 1 kHz'); xlabel('n'); grid on;
subplot(2,2,2); stem(f, abs(X)*2/N); title('Espectro de magnitud (rango completo)'); xlabel('f [Hz]'); grid on;
subplot(2,2,3); stem(f, real(X)*2/N); title('Parte real de X[k]'); xlabel('f [Hz]'); grid on;
subplot(2,2,4); stem(f, imag(X)*2/N); title('Parte imaginaria de X[k]'); xlabel('f [Hz]'); grid on;
