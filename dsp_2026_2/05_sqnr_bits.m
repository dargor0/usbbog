% 05_sqnr_bits.m
% Tema 1 - SQNR vs numero de bits: SQNR ~ 6.02 b + 1.76 dB (seno plena escala).
% Ejecutar:  octave-cli 05_sqnr_bits.m
%

clear; close all; clc;

Vmax = 1; Vmin = -1;
N = 2^16;
t = (0:N-1) / N;                 % 1 segundo, periodos enteros (sin fuga)
x = cos(2*pi*3*t);               % seno a plena escala (3 periodos)

bvec = 2:16;
sqnr = zeros(size(bvec));
for i = 1:numel(bvec)
  b = bvec(i);
  Delta = (Vmax - Vmin) / (2^b);
  xq = Delta * round(x / Delta);
  Px = mean(x.^2);
  Pe = mean((x - xq).^2);
  sqnr(i) = 10 * log10(Px / Pe);
end

teoria = 6.02 * bvec + 1.76;

figure('Name', 'SQNR vs bits');
plot(bvec, sqnr, 'o', bvec, teoria, '-');
legend('SQNR simulada', '6.02 b + 1.76 dB', 'Location', 'northwest');
xlabel('Bits b'); ylabel('SQNR [dB]');
title('SQNR en funcion de la resolucion');

fprintf('  b   SQNR sim [dB]  teoria [dB]  dif [dB]\n');
for i = 1:numel(bvec)
  fprintf('%3d  %12.2f  %11.2f  %8.2f\n', bvec(i), sqnr(i), teoria(i), ...
          sqnr(i) - teoria(i));
end

% Ejemplos de las laminas
fprintf('\nCD de audio (16 bits):  SQNR ~= %.1f dB\n', 6.02*16 + 1.76);
fprintf('Voz/PCM (8 bits):       SQNR ~= %.1f dB\n', 6.02*8 + 1.76);

%% Ejercicio 1
% Verifique la regla "cada bit extra ~6 dB": calcule sqnr(b) - sqnr(b-1)
% para b = 3..16 a partir del vector sqnr.

%% Ejercicio 2 (propuesto)
% Un sensor de 12 bits para instrumentacion: SQNR esperado de un seno a
% plena escala. Compararlo con uno de 24 bits (audio profesional).
