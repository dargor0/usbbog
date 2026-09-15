% 10_dtfs.m
% Tema 2 - Series de Fourier discretas (DTFS).
% Ejecutar:  octave-cli 10_dtfs.m
%
% Referencias a las laminas del Tema 2:
%   - "Senales discretas: la DTFS en detalle"
%   - "Ejemplo: DTFS de una senal discreta": x[n]=[1,2,1,2] (N=4) ->
%        c0=1.5, c1=0, c2=-0.5, c3=0.

clear; close all; clc;

N = 4;
x = [1 2 1 2];       % un periodo

% analisis: c_k = (1/N) sum_n x[n] e^{-j2pi k n/N}
k = 0:N-1; n = 0:N-1;
W = exp(-1j*2*pi*(k'*n)/N);
ck = (W * x(:)) / N;

fprintf('============================================================\n');
fprintf('SERIES DE FOURIER DISCRETAS (DTFS)\n');
fprintf('============================================================\n');
fprintf('x[n] = [1 2 1 2], periodo N = %d\n', N);
fprintf('\n k |  c_k\n');
for kk = 1:N
  fprintf(' %d | %+.3f%+.3fj\n', kk-1, real(ck(kk)), imag(ck(kk)));
end

fprintf('\nVerificaciones:\n');
fprintf('c_0 = %.2f (valor medio, debe ser 1.5)\n', real(ck(1)));
fprintf('|c_2| = %.2f (debe ser 0.5)\n', abs(ck(3)));
fprintf('|c_1| = %.2f, |c_3| = %.2f (deben ser 0)\n', abs(ck(2)), abs(ck(4)));

% sintesis
x_rec = sum(ck(:) .* exp(1j*2*pi*(k(:)*n)/N));
fprintf('\nSintesis: x_rec = %s\n', mat2str(real(x_rec), 6));
fprintf('Error de reconstruccion = %.2e\n', max(abs(x_rec - x)));

% periodicidad c_{k+N} = c_k (misma senal de periodo N, k = 0..2N-1)
Nk = 8;
ks = 0:Nk-1;
W3 = exp(-1j*2*pi*(ks'*n)/N);
ck_ext = (W3 * x(:)) / N;
fprintf('Periodicidad (misma senal N=4, k = 0..7):\n');
for kk = 0:3
  fprintf('c_%d = %+.3f%+.3fj  vs c_%d = %+.3f%+.3fj\n', ...
          kk+4, real(ck_ext(kk+5)), imag(ck_ext(kk+5)), ...
          kk, real(ck(kk+1)), imag(ck(kk+1)));
end

figure;
subplot(2,1,1);
stem(0:N-1, abs(ck), 'filled'); grid on;
title('DTFS de x[n]=[1,2,1,2]: |c_k|');
xlabel('k'); ylabel('|c_k|');
subplot(2,1,2);
stem(0:N-1, angle(ck), 'filled'); grid on;
title('DTFS: fase ang(c_k)');
xlabel('k'); ylabel('ang(c_k) [rad]');

%% --------------------------------------------------------------------------
%% Ejercicios propuestos (complete y verifique)
%% --------------------------------------------------------------------------
%  E1. Use x[n] = [1 0 -1 0] (N=4): calcule c_k y observe que solo
%      sobrevive la frecuencia k=1 (un tono).
%  E2. Verifique el teorema de Parseval discreto: sum |c_k|^2 =
%      (1/N) sum |x[n]|^2.
%  E3. Cambie N (p. ej., N=8 con una onda discreta) y compruebe que hay
%      exactamente N coeficientes independientes.
%  E4. Grafique el espectro en k = -N/2..N/2 (simetria hermitiana) para
%      una x[n] real.
