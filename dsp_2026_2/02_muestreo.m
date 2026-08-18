% 02_muestreo.m
% Tema 1 - Muestreo de una senal continua.
% Ejecutar:  octave-cli 02_muestreo.m
%

clear; close all; clc;

f0 = 2;                  % frecuencia de la senal [Hz]
fs = 20;                 % tasa de muestreo [Hz], fs > 2*f0 = 4
Ts = 1/fs;

t = 0:1e-4:1;            % eje continuo (denso)
xt = cos(2*pi*f0*t);

n = 0:fs;                % indices de las muestras
tn = n*Ts;               % instantes de muestreo
xn = cos(2*pi*f0*tn);    % x[n] = x(n*Ts)

figure('Name', 'Muestreo');
plot(t, xt, 'b'); hold on;
stem(tn, xn, 'r', 'filled', 'LineWidth', 1.2);
title('Muestreo de una senal continua');
xlabel('t [s]'); ylabel('Amplitud');
legend('x(t) = cos(2\pi f_0 t)', 'Muestras x[n]');
ylim([-1.3 1.3]);

% Frecuencia normalizada
w0 = 2*pi*f0/fs;
fprintf('f0 = %g Hz, fs = %g Hz, Ts = %g s\n', f0, fs, Ts);
fprintf('Frecuencia normalizada: w0 = 2*pi*f0/fs = %.4f rad/muestra\n', w0);

%% Ejercicio 1: comprobar Nyquist
% Cambie fs a 2 (fs = 2*f0, caso limite), 3, 4 y 40. Grafique y observe:
%   - fs < 2*f0  -> las muestras ya no reconstruyen el seno (aliasing).
%   - fs >= 2*f0 -> las muestras describen bien la senal.
% Para cada fs calcule tambien la frecuencia normalizada w0.

%% Ejercicio 2 (propuesto)
% Muestree x(t) = cos(2*pi*1000*t) a fs = 8000 Hz (como en voz) y verifique
% que w0 = pi/4 rad/muestra.
