% 04_error_cuantizacion.m
% Tema 1 - Error de cuantizacion: modelo de ruido uniforme.
% Ejecutar:  octave-cli 04_error_cuantizacion.m
%

clear; close all; clc;

Vmax = 1; Vmin = -1;
b = 8;
Delta = (Vmax - Vmin) / (2^b);

N = 20000;
rng(0);
x = 0.9 * (2*rand(1, N) - 1);        % senal uniforme en [-0.9, 0.9]
xq = Delta * round(x / Delta);
e = x - xq;

figure('Name', 'Error de cuantizacion');
hist(e, 50);
hold on;
line([-Delta/2 -Delta/2], ylim, 'Color', 'r', 'LineStyle', '--');
line([ Delta/2  Delta/2], ylim, 'Color', 'r', 'LineStyle', '--');
title('Histograma del error de cuantizacion');
xlabel('e[n]'); ylabel('Conteo');

rms_e = sqrt(mean(e.^2));
fprintf('b = %d bits, Delta = %.5f\n', b, Delta);
fprintf('RMS empirico del error:    %.6f\n', rms_e);
fprintf('Teorico Delta/sqrt(12):    %.6f\n', Delta/sqrt(12));

%% Ejercicio 1
% Repita con b = 4 y b = 12. Compare el RMS empirico con Delta/sqrt(12) en
% cada caso y verifique que el error queda acotado entre -Delta/2 y Delta/2.

%% Ejercicio 2 (propuesto)
% Use una senal sinusoidal a plena escala (x = 0.9*cos(2*pi*2*t)) en vez de
% uniforme. El histograma del error deja de ser plano: explique por que
% (la densidad de muestras no es uniforme cerca de los extremos del seno).
