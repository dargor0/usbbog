# Apio en Windows — referencia rápida

Lista de verificación breve para instalar en una máquina Windows 10/11 x86-64.

## Alcance

Instalar Apio para el usuario actual y verificar la cadena de herramientas para
la tarjeta Nexys 4 DDR.

- Apio y sus paquetes se pueden instalar **sin derechos de administrador**.
- En este procedimiento, los derechos de administrador solo son necesarios para
  el controlador FTDI/WinUSB que se usa para programar la placa.
- Se requiere acceso a Internet.
- Reserve 5 GB de espacio libre en disco.

## Instalación recomendada: ejecutar el script

1. Copie `install-apio-user.bat` a la máquina de destino.
2. Haga doble clic en él o ejecútelo desde el símbolo del sistema:

```bat
install-apio-user.bat
```

3. Espere a que termine. El script:
   - descarga el paquete oficial más reciente de Apio para Windows;
   - lo instala en `%LOCALAPPDATA%\Apio`;
   - agrega `%LOCALAPPDATA%\Apio\apio` al `PATH` del usuario;
   - instala los paquetes de Apio.
4. Abra una **nueva** ventana del símbolo del sistema o de PowerShell.

Para una instalación para todos los usuarios, use
`install-apio-system.bat` como Administrador. 

## Verificar la instalación

```bat
apio --version
apio packages list --check
apio boards | findstr /i nexys
```

Resultado esperado:

- `apio --version` muestra una versión.
- `apio packages list --check` informa que los paquetes están en buen estado.
- La lista de placas incluye `nexys-a7-100t` (Nexys 4 DDR).

Ejecute una prueba de compilación en un directorio nuevo y vacío:

```bat
cd %USERPROFILE%
mkdir apio-smoke 2>nul
cd apio-smoke
apio examples fetch nexys-a7-100t/blinky
cd blinky
apio build
```

Salida esperada:

```text
_build\default\hardware.bit
```

## Método manual alternativo

Úselo solo si el script no se puede ejecutar.

1. Descargue el paquete para Windows desde:
   https://github.com/FPGAwars/apio/releases/latest

   Archivo: `apio-cli-windows-amd64-<date>-bundle.zip`

2. Desbloquee el archivo ZIP y extráigalo en:

```text
%LOCALAPPDATA%\Apio
```

3. Agregue este directorio al `PATH` del usuario:

```text
%LOCALAPPDATA%\Apio\apio
```

4. Abra una terminal nueva y ejecute:

```bat
apio --version
apio packages install
apio packages list --check
```

Si la máquina ya tiene Python 3.11.4+ y prefiere pip, esto también funciona:

```bat
python -m pip install --user apio
apio packages install
```

## Controlador de la placa y programación

Generar un bitstream no requiere derechos de administrador.

La programación por JTAG necesita el controlador FTDI/WinUSB:

```bat
apio devices scan-usb
```

- Dispositivo esperado: `0403:6010` (FT2232).
- Si no aparece, un administrador debe ejecutar:

```bat
apio drivers install ftdi
```

En Zadig: seleccione la **interfaz 0** de la placa, elija **WinUSB**, haga clic
en **Replace Driver** y luego desconecte y vuelva a conectar la placa.

Después:

```bat
apio upload
```

Nota: esto reemplaza el controlador FTDI de la interfaz 0. Si la máquina también
usa Vivado o Digilent Adept, restaure el controlador FTDI original después con
`apio drivers uninstall ftdi`.

## Lista de aceptación

- [ ] `apio --version` funciona en una terminal nueva
- [ ] `apio packages list --check` pasa correctamente
- [ ] `apio boards` muestra `nexys-a7-100t`
- [ ] El ejemplo blinky genera `_build\default\hardware.bit`
- [ ] Si hay que programar la placa: `apio devices scan-usb` muestra `0403:6010`
      y `apio upload` funciona

## Problemas comunes

| Problema | Acción |
|---|---|
| No se reconoce `apio` | Abra una terminal nueva; verifique que `%LOCALAPPDATA%\Apio\apio` esté en el `PATH` del usuario |
| El script no puede descargar | Compruebe el acceso a Internet y la configuración de TLS/proxy; use el método manual alternativo |
| Falla la verificación de paquetes | Ejecute `apio packages install --force` |
| No se detecta la placa | Compruebe el cable USB y la alimentación; instale el controlador FTDI como administrador |
| `apio upload` deniega el acceso | Cierre Vivado/Digilent Adept; vuelva a conectar la placa |
| La instalación del controlador está bloqueada | Requiere derechos de administrador; pida ayuda a TI o use una máquina que ya tenga el controlador instalado |
