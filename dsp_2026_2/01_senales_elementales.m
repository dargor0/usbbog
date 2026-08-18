% 01_senales_elementales.m
% Tema 1 - Senales elementales discretas: impulso, escalon, exponencial y seno.
% Ejecutar:  octave-cli 01_senales_elementales.m
%

clear; close all; clc;

n = -5:15;

% Impulso: delta[n] = 1 si n == 0
delta = zeros(1, numel(n));
delta(n == 0) = 1;

% Escalon: u[n] = 1 si n >= 0
u = double(n >= 0);

% Exponencial: a^n u[n]
a = 0.85;
xexp = (a .^ n) .* u;

% Seno: A cos(w0 n + phi)
A = 1; w0 = 0.5*pi; phi = 0;
xseno = A * cos(w0 * n + phi);

figure('Name', 'Senales elementales');
subplot(2, 2, 1);
stem(n, delta, 'filled'); title('Impulso \delta[n]'); xlabel('n');
subplot(2, 2, 2);
stem(n, u, 'filled'); title('Escalon u[n]'); xlabel('n');
subplot(2, 2, 3);
stem(n, xexp, 'filled'); title('Exponencial a^n u[n]'); xlabel('n');
subplot(2, 2, 4);
stem(n, xseno, 'filled'); title('Seno A cos(\omega_0 n + \phi)'); xlabel('n');

%% Ejercicio 1: descomposicion en impulsos
% Dada la secuencia x = [1 2 3 4] definida para n = 0..3, exprésela como
% x[n] = sum_k x[k] delta[n-k] y grafique los impulsos ponderados.
x = [1 2 3 4];
nsup = -5:5;
xr = zeros(1, numel(nsup));
for k = 0:numel(x)-1
  d = zeros(1, numel(nsup));
  d(nsup == k) = 1;
  xr = xr + x(k+1) * d;   % suma de impulsos escalados y desplazados
end
figure('Name', 'Descomposicion en impulsos');
stem(nsup, xr, 'filled'); title('x[n] = \Sigma x[k] \delta[n-k]'); xlabel('n');
fprintf('x reconstruida en n=0..3: %d %d %d %d\n', xr(nsup == 0), ...
        xr(nsup == 1), xr(nsup == 2), xr(nsup == 3));

%% Ejercicio 2 (propuesto)
% Cambie a (por ejemplo 0.5, 1.05, -0.8) y observe como cambia la
% exponencial: decrece, crece o alterna de signo.
