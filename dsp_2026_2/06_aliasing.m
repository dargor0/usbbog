% 06_aliasing.m
% Tema 1 - Aliasing: muestreo por debajo de Nyquist (fs < 2 f0).
% Ejecutar:  octave-cli 06_aliasing.m
%

clear; close all; clc;

f0 = 100;                   % frecuencia de la senal [Hz]
t = 0:1e-5:0.1;

% --- Caso 1: muestreo insuficiente (fs < 2 f0) ---------------------------
fs = 70;                    % 70 < 200 Hz -> hay aliasing
Ts = 1/fs;
n = 0:round(0.1/Ts);
tn = n * Ts;

xt = cos(2*pi*f0*t);
xn = cos(2*pi*f0*tn);

% Frecuencia del alias: fa = |f0 - k*fs| (primer alias, k = 1)
fa = abs(f0 - fs);

figure('Name', 'Aliasing');
plot(t, xt, 'b'); hold on;
stem(tn, xn, 'r', 'filled', 'LineWidth', 1.2);
plot(t, cos(2*pi*fa*t), 'g--', 'LineWidth', 1.5);
title(sprintf('Muestreo insuficiente: fs = %g Hz < 2 f0 = %g Hz', fs, 2*f0));
xlabel('t [s]'); ylabel('Amplitud');
legend('x(t) = cos(2\pi 100 t)', ['Muestras fs = ' num2str(fs) ' Hz'], ...
       ['Alias ' num2str(fa) ' Hz'], 'Location', 'northeast');
ylim([-1.3 1.3]);

fprintf('fs = %g Hz < 2*f0 = %g Hz: aparece un alias en %g Hz.\n', fs, 2*f0, fa);

% --- Caso 2: muestreo correcto (fs > 2 f0) --------------------------------
fs2 = 250;                  % 250 > 200 Hz -> sin aliasing
Ts2 = 1/fs2;
n2 = 0:round(0.1/Ts2);
tn2 = n2 * Ts2;
xn2 = cos(2*pi*f0*tn2);

figure('Name', 'Muestreo correcto');
plot(t, xt, 'b'); hold on;
stem(tn2, xn2, 'r', 'filled', 'LineWidth', 1.2);
title(sprintf('Muestreo correcto: fs = %g Hz > 2 f0 = %g Hz', fs2, 2*f0));
xlabel('t [s]'); ylabel('Amplitud');
legend('x(t) = cos(2\pi 100 t)', ['Muestras fs = ' num2str(fs2) ' Hz']);
ylim([-1.3 1.3]);

%% Ejercicio 1
% Verifique la regla del alias: para f0 = 100 Hz pruebe fs = 80, 90, 150, 180
% y calcule fa = abs(f0 - fs) en cada caso. Compruebe graficamente que las
% muestras "caminan" sobre la coseno de frecuencia fa.

%% Ejercicio 2 (propuesto)
% Un audio con fmax = 20 kHz muestreado a fs = 44.1 kHz: verifique que
% fs > 2*fmax. Repita el ejercicio con fs = 32 kHz y explique por que el
% resultado cambia.
