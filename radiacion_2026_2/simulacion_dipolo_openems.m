% simulacion_dipolo_openems.m
% -----------------------------------------------------------------------------
% Tema 2 - Practica del tema: simulacion de un dipolo de media onda (OpenEMS).
%
% LIBRERIA REQUERIDA (Octave/MATLAB):
%   - OpenEMS  (motor FDTD)  +  CSXCAD (geometria y malla)
%     Interfaz: InitCSX, AddMetal, AddBox, AddLumpedPort, DefineRectGrid,
%               CreateNF2FFBox, AddPML, calcPort, CalcNF2FF.
%     La transformacion campo cercano -> campo lejano (nf2ff) viene incluida
%     con OpenEMS.
%
%   Instalacion (Ubuntu/Debian):
%       sudo add-apt-repository ppa:thliebig/openems-ppa
%       sudo apt update && sudo apt install openems
%   o compilar desde: https://github.com/thliebig/openEMS-Project
%
% Resultados: Zin(f), S11, SWR, patron (planos E y H), HPBW, directividad,
% potencia radiada y comparacion con los valores teoricos del dipolo lambda/2
% (diapositivas "valores teoricos de referencia").
%
% Nota: el FDTD con hilo delgado es menos preciso para Zin que el MoM (NEC);
% el patron, el HPBW y la directividad son fiables.
%
% Uso:
%   octave --no-gui simulacion_dipolo_openems.m
% -----------------------------------------------------------------------------

clear; close all;

if exist('InitFDTD', 'file') ~= 2 || exist('CalcNF2FF', 'file') ~= 2
  error(['OpenEMS/CSXCAD no estan disponibles en este Octave. Instale ', ...
         'OpenEMS (interfaz Octave) y vuelva a ejecutar. Vea el encabezado ', ...
         'de este archivo.']);
end

physical_constants;
unit = 1e-3;                       % longitudes en mm

% ---- 1) Parametros del dipolo ----------------------------------------------
f0         = 1e9;                  % frecuencia de diseno [Hz]
lambda0    = c0/f0;                % [m]
f_stop     = 1.5e9;                % ancho de banda de la excitacion
lambda_min = c0/f_stop;
mesh_air   = lambda_min/20/unit;   % resolucion de malla en el aire [mm]
L          = 0.5*lambda0/unit;     % longitud del dipolo lambda/2 [mm]
feedR      = 50;                   % impedancia del puerto [ohm]

% ---- 2) Solver FDTD ---------------------------------------------------------
FDTD = InitFDTD('EndCriteria', 1e-4);
FDTD = SetGaussExcite(FDTD, f0, f_stop);
BC = {'PML_8' 'PML_8' 'PML_8' 'PML_8' 'PML_8' 'PML_8'};   % espacio abierto
FDTD = SetBoundaryCond(FDTD, BC);

% ---- 3) Geometria (CSXCAD) --------------------------------------------------
CSX = InitCSX();

CSX = AddMetal(CSX, 'Dipole');                       % PEC (dipolo en z)
CSX = AddBox(CSX, 'Dipole', 1, [0 0 -L/2], [0 0 L/2]);

% puerto concentrado en el centro (fuente + plano de referencia S11)
[CSX, port] = AddLumpedPort(CSX, 100, 1, feedR, ...
                            [-0.1 -0.1 -mesh_air/2], [0.1 0.1 mesh_air/2], ...
                            [0 0 1], true);

% ---- 4) Malla ---------------------------------------------------------------
mesh.x = [-lambda0/unit/2 0 lambda0/unit/2];
mesh.y = [-lambda0/unit/2 0 lambda0/unit/2];
mesh.z = [-lambda0/unit -L/2 -L/4 0 L/4 L/2 lambda0/unit];
mesh   = SmoothMesh(mesh, mesh_air, 1.2);

% caja nf2ff (campo cercano -> lejano)
start = [mesh.x(1) mesh.y(1) mesh.z(1)];
stop  = [mesh.x(end) mesh.y(end) mesh.z(end)];
[CSX, nf2ff] = CreateNF2FFBox(CSX, 'nf2ff', start, stop, ...
                              'OptResolution', lambda_min/15/unit);
mesh = AddPML(mesh, 10);                 % aire entre nf2ff y el PML
CSX  = DefineRectGrid(CSX, unit, mesh);

% ---- 5) Ejecutar la simulacion ---------------------------------------------
Sim_Path = 'tmp_dipolo';
Sim_CSX  = 'dipolo.xml';
if exist(Sim_Path, 'dir') && exist(fullfile(Sim_Path, 'Et'), 'file')
  fprintf('Reutilizando resultados en %s ...\n', Sim_Path);      % post-proceso
else
  CleanupSimPath(Sim_Path);
  WriteOpenEMS(fullfile(Sim_Path, Sim_CSX), FDTD, CSX);
  % CSXGeomPlot(fullfile(Sim_Path, Sim_CSX));   % previsualizacion (opcional)
  RunOpenEMS(Sim_Path, Sim_CSX);
end

% ---- 6) Puerto: Zin, S11, SWR ----------------------------------------------
freq = linspace(0.7e9, 1.3e9, 121);
port = calcPort(port, Sim_Path, freq);

s11 = port.uf.ref ./ port.uf.inc;
Zin = port.uf.tot ./ port.if.tot;
swr = (1 + abs(s11)) ./ (1 - abs(s11));

[~, i0]   = min(abs(freq - f0));
[~, ires] = min(abs(imag(Zin)));

fprintf('\n[1] Impedancia a f0: Z = %.1f %+.1f j ohm\n', real(Zin(i0)), imag(Zin(i0)));
fprintf('    Resonancia: f = %.0f MHz, R = %.1f ohm\n', freq(ires)/1e6, real(Zin(ires)));
fprintf('    |S11|(f0) = %.3f  SWR = %.2f\n', abs(s11(i0)), swr(i0));

% ---- 7) Campo lejano: patron, HPBW, directividad ---------------------------
theta = 0:2:180;
phi   = 0:5:355;
nf2ff = CalcNF2FF(nf2ff, Sim_Path, f0, theta*pi/180, phi*pi/180, 'Mode', 1);

E = squeeze(nf2ff.E_norm{1});            % ntheta x nphi
U = abs(E).^2;
dth = deg2rad(2); dph = deg2rad(5);
w = sin(theta'*pi/180);                  % ntheta x 1 (broadcast sobre phi)
Prad_int = sum(sum(U .* w)) * dth * dph;
D_dBi = 10*log10(4*pi*max(U(:))/Prad_int);

Ec = abs(E(:,1)); Ec = Ec/max(Ec);       % corte del plano E (phi=0)
idx = find(Ec >= 1/sqrt(2));             % -3 dB en potencia
hpbw = theta(max(idx)) - theta(min(idx));

fprintf('\n[2] HPBW (plano E) = %.1f grados\n', hpbw);
fprintf('    Directividad (integrada) = %.2f dBi\n', D_dBi);
fprintf('    Potencia radiada = %.4f W\n', nf2ff.Prad);

% ---- 8) Comparacion con la teoria ------------------------------------------
Rrad_t = 73.1; X_t = 42.5; HPBW_t = 78; SWR_t = 1.46; D0_t = 2.15;
fprintf('\n[3] Comparacion simulacion vs. teoria (dipolo lambda/2)\n');
fprintf('    %-26s%12s%12s\n', 'Parametro', 'Simulado', 'Teoria');
fprintf('    %-26s%12.2f%12.2f\n', 'Directividad D0 (dBi)', D_dBi, D0_t);
fprintf('    %-26s%12.1f%12.1f\n', 'HPBW (grados)', hpbw, HPBW_t);
fprintf('    %-26s%12.1f%12.1f\n', 'R en resonancia (ohm)', real(Zin(ires)), Rrad_t);
fprintf('    %-26s%12.1f%12.1f\n', 'X a f0 (ohm)', imag(Zin(i0)), X_t);
fprintf('    %-26s%12.2f%12.2f\n', 'SWR en resonancia', swr(ires), SWR_t);

% ---- 9) Figuras -------------------------------------------------------------
figure; plot(freq/1e6, real(Zin), 'b-', freq/1e6, imag(Zin), 'r--', 'LineWidth', 1.5);
grid on; xlabel('f [MHz]'); ylabel('Z_{in} [ohm]');
title('Impedancia de entrada - dipolo \lambda/2 (OpenEMS)');
legend('R', 'X'); print('-dpng', 'dipolo_t2_openems_impedancia.png');

figure; plot(freq/1e6, swr, 'b-', 'LineWidth', 1.5); hold on;
grid on; xlabel('f [MHz]'); ylabel('SWR'); title('SWR (Z_0 = 50 ohm)');
print('-dpng', 'dipolo_t2_openems_swr.png');

figure; polar(theta*pi/180, 20*log10(Ec)); grid on;
title('Patron (dB) - plano E'); print('-dpng', 'dipolo_t2_openems_patron.png');

fprintf('\n[figuras] dipolo_t2_openems_impedancia.png, _swr.png, _patron.png\n');
