% 15_ifft_recuperar.m
% Tema 3 - Recuperar la senal original con la IFFT.
% Ejecutar:  octave-cli 15_ifft_recuperar.m
%
% Referencias a las laminas del Tema 3:
%   - "DFT: definicion y propiedades": la DFT es invertible.

clear; close all; clc;

N = 256;
n = 0:N-1;
x = cos(2*pi*3*n/N) + 0.5*sin(2*pi*10*n/N);

X = fft(x);
x2 = ifft(X);

err = max(abs(x - x2));
fprintf('============================================================\n');
fprintf('RECUPERAR LA SENAL CON LA IFFT\n');
fprintf('============================================================\n');
fprintf('error maximo |x[n] - ifft(fft(x))| = %.3e\n', err);
fprintf('parte imaginaria maxima de la recuperacion = %.3e\n', max(abs(imag(x2))));

figure;
plot(n, x, 'b-', n, real(x2), 'r--');
legend('original', 'ifft(fft(x))'); title('Original y recuperada'); grid on;
