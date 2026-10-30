@echo off
setlocal EnableExtensions
title Apio system-wide installer for Windows

rem Install Apio system-wide for all users. Requires Administrator.
rem
rem CLI:          %ProgramFiles%\Apio\apio
rem Shared home:  %ProgramData%\Apio\home
rem Packages:     %ProgramData%\Apio\packages
rem Machine env:  PATH, APIO_HOME, APIO_PACKAGES
rem
rem Users get read/execute access to the CLI and packages, and modify access
rem to the shared Apio home. Only an administrator should update packages.

set "APIO_ROOT=%ProgramFiles%\Apio"
if defined ProgramW6432 set "APIO_ROOT=%ProgramW6432%\Apio"
set "APIO_DIR=%APIO_ROOT%\apio"
set "APIO_EXE=%APIO_DIR%\apio.exe"
set "APIO_DATA=%ProgramData%\Apio"
set "APIO_HOME_DIR=%APIO_DATA%\home"
set "APIO_PACKAGES_DIR=%APIO_DATA%\packages"
set "TMP_JSON=%TEMP%\apio-release.json"
set "TMP_ZIP=%TEMP%\apio-bundle.zip"
set "TMP_URL=%TEMP%\apio-url.txt"

rem Use the shared locations for this elevated install process.
set "APIO_HOME=%APIO_HOME_DIR%"
set "APIO_PACKAGES=%APIO_PACKAGES_DIR%"

del /q "%TMP_JSON%" "%TMP_ZIP%" "%TMP_URL%" 2>nul

if /i "%PROCESSOR_ARCHITECTURE%"=="AMD64" goto :arch_ok
if /i "%PROCESSOR_ARCHITEW6432%"=="AMD64" goto :arch_ok
echo ERROR: This script requires 64-bit Windows (x86-64).
goto :fail_no_pause

:arch_ok
where powershell.exe >nul 2>nul
if errorlevel 1 (
    echo ERROR: Windows PowerShell was not found.
    goto :fail_no_pause
)

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) { exit 1 }"
if errorlevel 1 (
    echo ERROR: This script must be run as Administrator.
    echo Right-click the file and choose "Run as administrator".
    goto :fail_no_pause
)

echo.
echo === Apio system-wide installer for Windows ===
echo.

echo [1/7] Downloading the latest Apio release information...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ErrorActionPreference='Stop'; [Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -UseBasicParsing -Uri 'https://api.github.com/repos/FPGAwars/apio/releases/latest' -OutFile '%TMP_JSON%'"
if errorlevel 1 (
    echo ERROR: Could not download release information from GitHub.
    goto :fail
)

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "(Get-Content -Raw '%TMP_JSON%' | ConvertFrom-Json).assets | Where-Object { $_.name -like 'apio-cli-windows-amd64-*-bundle.zip' } | Select-Object -First 1 -ExpandProperty browser_download_url" > "%TMP_URL%"
if errorlevel 1 (
    echo ERROR: Could not find the Windows bundle in the latest release.
    goto :fail
)
set /p APIO_URL=<"%TMP_URL%"
if not defined APIO_URL (
    echo ERROR: Could not determine the Apio bundle download URL.
    goto :fail
)

echo [2/7] Downloading the Apio bundle...
where curl.exe >nul 2>nul
if errorlevel 1 (
    powershell -NoProfile -ExecutionPolicy Bypass -Command ^
      "$ErrorActionPreference='Stop'; [Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -UseBasicParsing -Uri '%APIO_URL%' -OutFile '%TMP_ZIP%'"
) else (
    curl.exe -L --fail --silent --show-error -o "%TMP_ZIP%" "%APIO_URL%"
)
if errorlevel 1 (
    echo ERROR: Could not download the Apio bundle.
    goto :fail
)

echo [3/7] Extracting Apio to %APIO_ROOT%...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "Unblock-File -LiteralPath '%TMP_ZIP%' -ErrorAction SilentlyContinue"
if exist "%APIO_DIR%" rmdir /s /q "%APIO_DIR%"
if not exist "%APIO_ROOT%" mkdir "%APIO_ROOT%"
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ErrorActionPreference='Stop'; Expand-Archive -LiteralPath '%TMP_ZIP%' -DestinationPath '%APIO_ROOT%' -Force"
if errorlevel 1 (
    echo ERROR: Could not extract the Apio bundle.
    goto :fail
)
if not exist "%APIO_EXE%" (
    echo ERROR: apio.exe was not found at "%APIO_EXE%".
    goto :fail
)

echo [4/7] Creating shared Apio directories and permissions...
if not exist "%APIO_DATA%" mkdir "%APIO_DATA%"
if not exist "%APIO_HOME_DIR%" mkdir "%APIO_HOME_DIR%"
if not exist "%APIO_PACKAGES_DIR%" mkdir "%APIO_PACKAGES_DIR%"

icacls "%APIO_ROOT%" /grant "*S-1-5-32-545:(OI)(CI)RX" /T >nul
if errorlevel 1 (
    echo ERROR: Could not set read permissions on "%APIO_ROOT%".
    goto :fail
)
icacls "%APIO_DATA%" /grant "*S-1-5-32-545:(OI)(CI)RX" >nul
if errorlevel 1 (
    echo ERROR: Could not set permissions on "%APIO_DATA%".
    goto :fail
)
icacls "%APIO_HOME_DIR%" /grant "*S-1-5-32-545:(OI)(CI)M" /T >nul
if errorlevel 1 (
    echo ERROR: Could not set permissions on "%APIO_HOME_DIR%".
    goto :fail
)
icacls "%APIO_PACKAGES_DIR%" /grant "*S-1-5-32-545:(OI)(CI)RX" /T >nul
if errorlevel 1 (
    echo ERROR: Could not set permissions on "%APIO_PACKAGES_DIR%".
    goto :fail
)

echo [5/7] Setting machine-wide PATH and Apio environment...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$apioDir = Join-Path $env:ProgramFiles 'Apio\apio'; if ($env:ProgramW6432) { $apioDir = Join-Path $env:ProgramW6432 'Apio\apio' }; $homeDir = Join-Path $env:ProgramData 'Apio\home'; $packagesDir = Join-Path $env:ProgramData 'Apio\packages'; [Environment]::SetEnvironmentVariable('APIO_HOME', $homeDir, 'Machine'); [Environment]::SetEnvironmentVariable('APIO_PACKAGES', $packagesDir, 'Machine'); $p = [Environment]::GetEnvironmentVariable('Path','Machine'); $parts = @(); if ($p) { $parts = $p -split ';' | Where-Object { $_ -ne '' } }; if ($parts -notcontains $apioDir) { if ($parts.Count -eq 0) { $new = $apioDir } else { $new = ($parts + $apioDir) -join ';' }; [Environment]::SetEnvironmentVariable('Path', $new, 'Machine') }"
if errorlevel 1 (
    echo ERROR: Could not set machine environment variables.
    goto :fail
)
set "PATH=%APIO_DIR%;%PATH%"

echo [6/7] Installing Apio packages into the shared directory...
echo This downloads the openXC7 toolchain and chip databases; it may take a while.
"%APIO_EXE%" packages install
if errorlevel 1 (
    echo ERROR: Apio package installation failed.
    goto :fail
)
"%APIO_EXE%" packages list --check
if errorlevel 1 (
    echo WARNING: Some Apio packages are not healthy.
    echo Run this system installer again to update them.
)

echo [7/7] Applying permissions to installed files...
icacls "%APIO_HOME_DIR%" /grant "*S-1-5-32-545:(OI)(CI)M" /T >nul
if errorlevel 1 (
    echo ERROR: Could not apply permissions to "%APIO_HOME_DIR%".
    goto :fail
)
icacls "%APIO_PACKAGES_DIR%" /grant "*S-1-5-32-545:(OI)(CI)RX" /T >nul
if errorlevel 1 (
    echo ERROR: Could not apply permissions to "%APIO_PACKAGES_DIR%".
    goto :fail
)

del /q "%TMP_JSON%" "%TMP_ZIP%" "%TMP_URL%" 2>nul

echo.
echo ============================================================
echo Apio is installed system-wide for all users.
echo.
echo CLI:             %APIO_DIR%
echo Shared home:     %APIO_HOME_DIR%
echo Shared packages: %APIO_PACKAGES_DIR%
echo.
echo Each user must open a NEW Command Prompt or PowerShell window
echo and run:
echo   apio --version
echo   apio info
echo.
echo Only an administrator should update packages by re-running
echo install-apio-system.bat.
echo.
echo Programming the FPGA still requires the FTDI/WinUSB driver:
echo   apio drivers install ftdi
echo ============================================================
echo.
if "%~1"=="" pause
endlocal
exit /b 0

:fail
echo.
echo Installation failed. Review the error above.
if "%~1"=="" pause
endlocal
exit /b 1

:fail_no_pause
endlocal
exit /b 1
