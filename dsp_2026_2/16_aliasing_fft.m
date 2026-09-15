% 16_aliasing_fft.m
% Tema 3 - Aliasing observado con la FFT.
% Compara la misma señal muestreada por debajo y por encima de Nyquist.
% Ejecutar:  octave-cli 16_aliasing_fft.m
%
% Referencias:
%   - Tema 1: muestreo y Nyquist (fs >= 2*fmax).

clear; close all; clc;

f0 = 700;        % frecuencia del seno [Hz]
fs_low = 1000;   % baja fs: f0 > fs/2 -> aliasing
fs_high = 2000;  % alta fs: f0 < fs/2 -> sin aliasing
N = 512;

% ---------- Muestras con fs baja (aliasing) ----------
n_low = 0:N-1;
t_low = n_low / fs_low;
x_low = sin(2*pi*f0*t_low);

% ---------- Muestras con fs alta (sin aliasing) ----------
n_high = 0:N-1;
t_high = n_high / fs_high;
x_high = sin(2*pi*f0*t_high);

% ---------- FFTs (rango completo) ----------
X_low = fft(x_low);
X_high = fft(x_high);
f_low = (0:N-1)*fs_low/N;
f_high = (0:N-1)*fs_high/N;

falias = abs(f0 - fs_low);

fprintf('============================================================\n');
fprintf('ALIASING: COMPARACION EN TIEMPO Y FRECUENCIA\n');
fprintf('============================================================\n');
fprintf('f0 = %d Hz\n', f0);
fprintf('fs_baja = %d Hz (fs/2 = %d) -> ALIASING\n', fs_low, fs_low/2);
fprintf('fs_alta = %d Hz (fs/2 = %d) -> SIN ALIASING\n', fs_high, fs_high/2);
fprintf('alias esperado: |f0 - fs_baja| = %d Hz\n', falias);

[~, kmax_low] = max(abs(X_low));
[~, kmax_high] = max(abs(X_high));
fprintf('pico con fs_baja en %.0f Hz\n', f_low(kmax_low));
fprintf('pico con fs_alta en %.0f Hz\n', f_high(kmax_high));

% ---------- Señal continua de referencia (fs = 10 kHz) ----------
fs_ref = 10000;
t_ref = 0:1/fs_ref:max(t_low(end), t_high(end));
x_ref = sin(2*pi*f0*t_ref);
x_alias = -sin(2*pi*falias*t_ref);  % fase invertida 180° para alinear con las muestras

% ---------- Graficas ----------
figure;

% Tiempo: fs baja
subplot(2,2,1);
plot(t_ref, x_ref, 'Color', [0.5 0.5 0.5]); hold on;
plot(t_ref, x_alias, 'Color', [1 0.65 0]);
stem(t_low, x_low);
title(sprintf('Tiempo: fs = %d Hz (ALIASING)', fs_low));
xlabel('t [s]'); legend('continua (fs = 10 kHz)', sprintf('alias (%d Hz)', falias)); xlim([0 0.01]); grid on;

% Tiempo: fs alta
subplot(2,2,2);
plot(t_ref, x_ref, 'Color', [0.5 0.5 0.5]); hold on;
stem(t_high, x_high);
title(sprintf('Tiempo: fs = %d Hz (sin aliasing)', fs_high));
xlabel('t [s]'); legend('continua (fs = 10 kHz)'); xlim([0 0.01]); grid on;

% Frecuencia: fs baja
subplot(2,2,3);
stem(f_low, abs(X_low)*2/N); hold on;
plot([f0 f0], ylim, 'r--');
plot([falias falias], ylim, 'g:');
legend('espectro', sprintf('f0 real = %d Hz', f0), sprintf('alias = %d Hz', falias));
title(sprintf('Espectro: fs = %d Hz', fs_low));
xlabel('f [Hz]'); grid on;

% Frecuencia: fs alta
subplot(2,2,4);
stem(f_high, abs(X_high)*2/N); hold on;
plot([f0 f0], ylim, 'r--');
legend('espectro', sprintf('f0 = %d Hz', f0));
title(sprintf('Espectro: fs = %d Hz', fs_high));
xlabel('f [Hz]'); grid on;
