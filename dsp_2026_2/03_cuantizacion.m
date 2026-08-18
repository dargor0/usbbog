% 03_cuantizacion.m
% Tema 1 - Cuantizacion uniforme (conversion analogico-digital).
% Ejecutar:  octave-cli 03_cuantizacion.m
%

clear; close all; clc;

Vmax = 1; Vmin = -1;
b = 4;                                  % bits por muestra
Delta = (Vmax - Vmin) / (2^b);
fprintf('b = %d bits -> 2^b = %d niveles, Delta = %.4f\n', b, 2^b, Delta);

fs = 100; f0 = 2;
t = (0:fs-1) / fs;
x = 0.9 * cos(2*pi*f0*t);               % senal de entrada (plena escala 0.9)

xq = Delta * round(x / Delta);          % cuantizador uniforme por redondeo

figure('Name', 'Cuantizacion');
plot(t, x, 'b'); hold on;
stairs(t, xq, 'r', 'LineWidth', 1.5);
title(['Cuantizacion uniforme, b = ' num2str(b) ' bits']);
xlabel('t [s]'); ylabel('Amplitud');
legend('Original x[n]', 'Cuantizada x_q[n]');
ylim([-1.1 1.1]);

%% Ejercicio 1: efecto del numero de bits
% Repita la grafica para b = 1, 3, 8 y 16. Observaciones:
%   - b = 1 -> solo 2 niveles (escalera muy gruesa).
%   - b creciente -> la escalera se acerca a la senal original.
% Calcule Delta en cada caso.

%% Ejercicio 2 (propuesto)
% Un ADC de 12 bits con Vmin = 0 V y Vmax = 5 V: calcule Delta (mV) y el
% numero de niveles. Verifique que Delta = 5/4096 ~ 1.22 mV.
