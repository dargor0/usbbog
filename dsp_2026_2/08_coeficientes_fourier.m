% 08_coeficientes_fourier.m
% Tema 2 - Coeficientes de las series de Fourier (CTFS) de una onda cuadrada.
% Ejecutar:  octave-cli 08_coeficientes_fourier.m
%
% Referencias a las laminas del Tema 2:
%   - "Como calcular los coeficientes (analisis)": c_k = (1/T) int_T x(t) e^{-j2pi k f0 t} dt
%   - "Ejemplo: coeficientes de la onda cuadrada": solo armonicos impares,
%     |c_k| = 2A/(pi |k|), fase -pi/2 (k>0) y +pi/2 (k<0).
%   - "El espectro de magnitud y de fase" y "Por que existen frecuencias negativas?".

clear; close all; clc;

A = 1.0;        % amplitud
T = 1.0;        % periodo [s]
f0 = 1/T;       % frecuencia fundamental

% funcion de la onda cuadrada (por muestras)
Ns = 10000;
ts = linspace(0, T, Ns);
xs = A * (ts < T/2) - A * (ts >= T/2);

% coeficiente analitico
ck_ana = @(k) (mod(k,2)==1) * (2*A/(1j*pi*k));

% coeficiente numerico (integral por trapecios)
ck_num = @(k) (1/T) * trapz(ts, xs .* exp(-1j*2*pi*k*f0*ts));

fprintf('============================================================\n');
fprintf('COEFICIENTES DE FOURIER DE LA ONDA CUADRADA\n');
fprintf('============================================================\n');
fprintf('Onda cuadrada: A = %g, T = %g s, f0 = %g Hz\n', A, T, f0);

k = -9:9;
c_ana = arrayfun(ck_ana, k);
c_num = arrayfun(ck_num, k);

fprintf('\n k   | c_k analitico      | c_k numerico\n');
for i = 1:numel(k)
  fprintf('%3d | %+.4f%+.4fj | %+.4f%+.4fj\n', k(i), real(c_ana(i)), imag(c_ana(i)), ...
          real(c_num(i)), imag(c_num(i)));
end

% espectro de magnitud y fase
figure;
subplot(2,1,1);
stem(k, abs(c_ana), 'filled'); grid on;
title('Espectro de magnitud |c_k| (onda cuadrada)');
xlabel('k'); ylabel('|c_k|');
subplot(2,1,2);
stem(k, angle(c_ana), 'filled'); grid on;
title('Espectro de fase ang(c_k)');
xlabel('k'); ylabel('ang(c_k) [rad]');
ylim([-2 2]);

fprintf('\nVerificaciones:\n');
fprintf('|c_1| teorico = 2A/pi = %.4f;  numerico = %.4f\n', 2*A/pi, abs(c_num(11)));
fprintf('c_2 (par) = %.4f (debe ser 0)\n', abs(c_num(12)));
fprintf('|c_-1| = %.4f vs |c_1| = %.4f (simetria hermitiana)\n', abs(c_num(9)), abs(c_num(11)));

%% --------------------------------------------------------------------------
%% Ejercicios propuestos (complete y verifique)
%% --------------------------------------------------------------------------
%  E1. Cambie la amplitud a A = 2 y verifique que |c_k| se duplica.
%  E2. Calcule la potencia: P = sum |c_k|^2 y compare con el valor medio
%      cuadratico de x(t) (teorema de Parseval).
%  E3. Use la formula trigonometrica b_k = 4A/(pi k) (impares) y verifique
%      que |c_k| = b_k/2.
%  E4. Cambie la onda a una con ciclo de trabajo diferente y observe que
%      aparecen armonicos pares.
