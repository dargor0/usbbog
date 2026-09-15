% 20_ruido_blanco.m
% Tema 3 - Espectro del ruido blanco.
% Ejecutar:  octave-cli 20_ruido_blanco.m
%
% Referencias a las laminas del Tema 3:
%   - El ruido blanco tiene un espectro aproximadamente plano.

clear; close all; clc;

rand('seed', 0);
N = 4096;
x = randn(N, 1);           % ruido blanco (media 0, varianza 1)

X = fft(x);
P = abs(X).^2 / N;         % densidad espectral de potencia
f = ((0:N-1)*2/N) - 1;     % frecuencia normalizada en [-1, 1)

fprintf('============================================================\n');
fprintf('ESPECTRO DEL RUIDO BLANCO\n');
fprintf('============================================================\n');
fprintf('potencia media (esperada ~1) = %.3f\n', mean(x.^2));
fprintf('media del espectro de potencia = %.3f\n', mean(P));

figure;
subplot(2,1,1); plot(x(1:512)); title('Ruido blanco (temporal)'); grid on;
subplot(2,1,2); plot(f, P); ylim([0 6]);
title('Densidad espectral de potencia (aprox. plana)'); xlabel('f normalizada'); grid on;
