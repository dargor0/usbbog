% 19_modulacion_am.m
% Tema 3 - Modulacion y demodulacion AM (desplazamiento del espectro).
% Ejecutar:  octave-cli 19_modulacion_am.m
%
% Referencias a las laminas del Tema 3:
%   - El espectro de la senal AM muestra portadora (fc) y bandas laterales
%     (fc +/- fm).
%   - Demodulacion simple: multiplicar por la portadora desplaza el espectro
%     a banda base y a 2fc; se recupera con un filtro ideal en frecuencia.
%
% Senal AM:  x(t) = (1 + mu*cos(2*pi*fm*t))*cos(2*pi*fc*t).

clear; close all; clc;

fc = 100e3;   % portadora [Hz]
fm = 1e3;     % modulante [Hz]
fs = 400e3;   % muestreo [Hz]
N = 4000;     % N tal que fc y fm caen en bins exactos
mu = 0.5;
t = (0:N-1)/fs;

% ------------------- modulacion -------------------
m = cos(2*pi*fm*t);                    % senal modulante
x = (1 + mu*m) .* cos(2*pi*fc*t);      % senal AM

X = fft(x);
f = (0:N-1)*fs/N;
Xm = abs(X)*2/N;

fprintf('============================================================\n');
fprintf('MODULACION AM\n');
fprintf('============================================================\n');
fprintf('fc = %.0f Hz, fm = %.0f Hz, mu = %.1f\n', fc, fm, mu);
fprintf('espectro: picos en fc, fc-fm y fc+fm (%.0f, %.0f, %.0f Hz)\n', ...
        fc, fc-fm, fc+fm);

% ------------------- demodulacion (simple) -------------------
xr = x .* cos(2*pi*fc*t);      % mezcla con la portadora
Xr = fft(xr);
Xrm = abs(Xr)*2/N;             % espectro desplazado

fprintf('\nDEMODULACION (simple): ESPECTRO DESPLAZADO\n');
fprintf('============================================================\n');
fprintf('tras mezclar con la portadora, el espectro se desplaza a banda base\n');
fprintf('(picos en 0 y +/-fm) y a 2fc (2fc +/- fm).\n');

% ---------- Una sola figura con los 3 plots ----------
figure;

% 1) AM en tiempo (primeros 3 ms)
subplot(3,1,1);
idx = t <= 3e-3;
plot(t(idx)*1e3, x(idx));
title('Senal AM (temporal)'); xlabel('t [ms]'); grid on;

% 2) AM en frecuencia [0, fs/2]
subplot(3,1,2);
plot(f(1:N/2+1)/1e3, Xm(1:N/2+1));
title('Espectro AM (portadora + bandas laterales)'); xlabel('f [kHz]'); grid on;
hold on;
plot([fc fc]/1e3, ylim, 'r--');
plot([(fc-fm) (fc-fm)]/1e3, ylim, 'g:');
plot([(fc+fm) (fc+fm)]/1e3, ylim, 'g:');
legend('espectro', 'fc', 'fc±fm');

% 3) Demodulacion en frecuencia [0, fs), incluye 2fc
subplot(3,1,3);
plot(f/1e3, Xrm);
title('Espectro tras mezclar: baseband, 2fc y espejo'); xlabel('f [kHz]'); grid on;
hold on;
plot([0 0], ylim, 'b--');
plot([fm fm]/1e3, ylim, 'b:');
plot([2*fc 2*fc]/1e3, ylim, 'r--');
plot([(2*fc-fm) (2*fc-fm)]/1e3, ylim, 'g:');
plot([(2*fc+fm) (2*fc+fm)]/1e3, ylim, 'g:');
legend('espectro', '0', 'fm', '2fc', '2fc±fm');
