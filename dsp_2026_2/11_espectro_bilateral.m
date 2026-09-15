% 11_espectro_bilateral.m
% Tema 2 - Espectro bilateral, frecuencias negativas y simetria hermitiana.
% Ejecutar:  octave-cli 11_espectro_bilateral.m
%
% Referencias a las laminas del Tema 2:
%   - "El espectro de magnitud y de fase"
%   - "Por que existen frecuencias negativas": para senales reales hay
%     simetria hermitiana; la asimetria implica senal compleja.

clear; close all; clc;

A = 1.0; T = 1.0; f0 = 1/T;

ck_cuadrada = @(k) (mod(k,2)==1) * (2*A/(1j*pi*k));

k = -12:12;
c_real = arrayfun(ck_cuadrada, k);

fprintf('============================================================\n');
fprintf('ESPECTRO BILATERAL Y SIMETRIA HERMITIANA\n');
fprintf('============================================================\n');

fprintf('\n[1] Senal real (onda cuadrada): espectro SIMETRICO\n');
fprintf('|c_1| = %.4f  |c_-1| = %.4f\n', abs(c_real(14)), abs(c_real(12)));
fprintf('fase c_1 = %+.4f  fase c_-1 = %+.4f (opuestas)\n', ...
        angle(c_real(14)), angle(c_real(12)));
fprintf('-> |c_-k| = |c_k|  y  fase impar  (simetria hermitiana)\n');

fprintf('\n[2] Senal compleja x(t) = e^{j2pi f0 t}: espectro ASIMETRICO\n');
fprintf('c_1 = 1 (solo frecuencia positiva); c_-1 = 0\n');

% graficas
figure;
subplot(2,2,1);
stem(k, abs(c_real), 'filled'); grid on;
title('Real: |c_k| (simetrico)'); xlabel('k');
subplot(2,2,2);
stem(k, angle(c_real), 'filled'); grid on;
title('Real: fase (impar)'); xlabel('k'); ylim([-3 3]);
subplot(2,2,3);
c_comp = double(k == 1);
stem(k, abs(c_comp), 'filled'); grid on;
title('Compleja: |c_k| (asimetrico)'); xlabel('k');
subplot(2,2,4);
stem(k, angle(double(k==1)), 'filled'); grid on;
title('Compleja: fase'); xlabel('k');

fprintf('\n[3] Espectro unilateral (frecuencias positivas, senal real):\n');
fprintf('se duplica la amplitud de |c_k| (k>0): P = |c_0|^2 + 2 sum |c_k|^2\n');
for kk = 1:6
  fprintf('|c_%d| unilateral = %.4f\n', kk, 2*abs(ck_cuadrada(kk)));
end

%% --------------------------------------------------------------------------
%% Ejercicios propuestos (complete y verifique)
%% --------------------------------------------------------------------------
%  E1. Verifique que la potencia bilateral = potencia unilateral.
%  E2. x(t) = cos(2pi f0 t): muestre dos lineas en +f0 y -f0 (ampl. 1/2).
%  E3. Explique por que las frecuencias negativas no son fisicas pero
%      simplifican el calculo (formulacion exponencial).
%  E4. x(t) = e^{j2pi f1 t} + e^{j2pi f2 t}: grafique y observe que no hay
%      simetria.
