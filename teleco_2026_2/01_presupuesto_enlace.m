% 01_presupuesto_enlace.m
% Tema 1 - Presupuesto de enlace (version Octave de
% 01_presupuesto_enlace.py). Lamina "Ejemplo: enlace a 5.8 GHz".
%
% Ejecutar:
%     octave-cli 01_presupuesto_enlace.m
%
% Dependencias: Octave (>= 6).

clear; close all; clc;

% ---- ejemplo de la lamina -------------------------------------------------
Pt = 20; Gt = 15; Gr = 12;          % dBm, dBi, dBi
LcableTx = 2; LcableRx = 2;         % dB
Lcables = LcableTx + LcableRx;
d = 5; f = 5.8;                     % km, GHz
Pmin = -90;                         % sensibilidad (dBm)

Lesp = 92.45 + 20*log10(f) + 20*log10(d);
EIRP = Pt + Gt - LcableTx;
Pr = Pt + Gt + Gr - Lesp - Lcables;
margen = Pr - Pmin;

fprintf('============================================================\n');
fprintf('PRESUPUESTO DE ENLACE (ejemplo 5.8 GHz)\n');
fprintf('============================================================\n');
fprintf('EIRP = %5.1f dBm\n', EIRP);
fprintf('L_esp = %5.1f dB  (la lamina: 121.7)\n', Lesp);
fprintf('P_r  = %5.1f dBm (la lamina: -78.7)\n', Pr);
fprintf('Margen = %5.1f dB\n', margen);

% ---- variar d y f ---------------------------------------------------------
fprintf('\nd[km] |  f=2.4  f=5.8  f=10  f=24  (P_r en dBm)\n');
for d_i = [1 2 5 10 20]
  fila = [];
  for f_i = [2.4 5.8 10 24]
    Le = 92.45 + 20*log10(f_i) + 20*log10(d_i);
    fila = [fila, Pt + Gt + Gr - Le - Lcables];
  end
  fprintf('%5.1f | %6.1f %6.1f %6.1f %6.1f\n', d_i, fila);
end

% ---- grafica P_r vs d -----------------------------------------------------
ds = linspace(0.5, 25, 200);
figure;
hold on;
for f_i = [2.4 5.8 10 24]
  Le = 92.45 + 20*log10(f_i) + 20*log10(ds);
  plot(ds, Pt + Gt + Gr - Le - Lcables, 'LineWidth', 1.2);
end
plot([0.5 25], [Pmin Pmin], 'r--', 'LineWidth', 1.2);
legend('f=2.4','f=5.8','f=10','f=24',['Sens. ' num2str(Pmin) ' dBm']);
xlabel('Distancia [km]'); ylabel('P_r [dBm]');
title('Presupuesto de enlace: P_r vs distancia');
grid on;

% ---- alcance maximo -------------------------------------------------------
dmax = 10^((Pt + Gt + Gr - Lcables - Pmin - 92.45 - 20*log10(f))/20);
fprintf('\nAlcance maximo a %.1f GHz: %.2f km\n', f, dmax);

M_fade = 10;
dmax_fade = 10^((Pt + Gt + Gr - Lcables - M_fade - Pmin - 92.45 - 20*log10(f))/20);
fprintf('Con margen de fading M=%.0f dB: %.2f km\n', M_fade, dmax_fade);

%% --------------------------------------------------------------------------
%% Ejercicios propuestos (complete y verifique)
%% --------------------------------------------------------------------------
%  E1. Cambie la sensibilidad a -85 dBm: nuevo margen y nuevo alcance.
%  E2. Agregue 3 dB de perdidas por lluvia y verifique la caida del margen.
%  E3. Enlace satelital (f = 12 GHz, d = 36000 km): calcule L_esp y
%      explique por que se usan antenas de alta ganancia.
%  E4. Duplique la distancia (10 km): verifique que P_r cae 6 dB.
