% 09_reconstruccion_gibbs.m
% Tema 2 - Reconstruccion (sintesis) de la onda cuadrada y fenomeno de Gibbs.
% Ejecutar:  octave-cli 09_reconstruccion_gibbs.m
%
% Referencias a las laminas del Tema 2:
%   - "La idea base (2/3): del tiempo a la frecuencia"
%   - "Ejemplo: coeficientes de la onda cuadrada": x(t) = (4A/pi)[sen + (1/3)sen3 + ...]
%   - Fenomeno de Gibbs: sobrepaso de ~9% en los bordes.

clear; close all; clc;

A = 1.0;
T = 1.0;
w0 = 2*pi/T;

t = linspace(0, 2*T, 4000);
x_ideal = A*(mod(t,T) < T/2) - A*(mod(t,T) >= T/2);

function x = recon(N, A, w0, t)
  x = zeros(size(t));
  for k = 1:2:N
    x += sin(k*w0*t)/k;
  end
  x = (4*A/pi)*x;
end

fprintf('============================================================\n');
fprintf('RECONSTRUCCION DE LA ONDA CUADRADA Y FENOMENO DE GIBBS\n');
fprintf('============================================================\n');

for N = [1 3 5 9 21 101]
  xN = recon(N, A, w0, t);
  fprintf('N = %3d: error RMS = %.4f (A = %g)\n', N, sqrt(mean((xN - x_ideal).^2)), A);
end

xN = recon(501, A, w0, t);
sobrepaso = (max(xN) - A)/A*100;
fprintf('\nSobrepaso de Gibbs con N = 501: %.2f%% (del salto 2A es ~9%%)\n', sobrepaso);

figure;
plot(t, x_ideal, 'k--', 'LineWidth', 1.5); hold on;
colores = {'b','g','r','m'}; ns = [1 3 9 101];
for i = 1:numel(ns)
  plot(t, recon(ns(i), A, w0, t), colores{i}, 'LineWidth', 1.2);
end
xlim([0 T]); xlabel('t [s]'); ylabel('x(t)');
title('Aproximacion de la onda cuadrada con N armonicos');
legend('ideal','N=1','N=3','N=9','N=101','Location','southeast');
grid on;

Ns = [1 3 5 9 21 51 101 501];
maxs = zeros(size(Ns));
for i = 1:numel(Ns)
  maxs(i) = max(recon(Ns(i), A, w0, t));
end
figure;
semilogx(Ns, maxs, 'o-'); hold on;
line([min(Ns) max(Ns)], [A*1.17896 A*1.17896], 'Color','r', 'LineStyle','--');
xlabel('Numero de armonicos N'); ylabel('Pico de la aproximacion');
title('Convergencia del maximo (fenomeno de Gibbs)');
legend('pico','limite ~1.179 A');
grid on;

%% --------------------------------------------------------------------------
%% Ejercicios propuestos (complete y verifique)
%% --------------------------------------------------------------------------
%  E1. Aumente N a 1001 y verifique que el sobrepaso sigue en ~9%.
%  E2. Aplique una ventana (Lanczos/Hanning) a los coeficientes y observe
%      la reduccion del sobrepaso.
%  E3. Cambie la amplitud a A = 2 y verifique que el sobrepaso es ~9% de A.
%  E4. Reconstruya una senal triangular (coeficientes ~1/k^2) y compare la
%      velocidad de convergencia con la onda cuadrada.
