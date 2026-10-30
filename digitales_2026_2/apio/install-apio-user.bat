@echo off
setlocal EnableExtensions
title Apio per-user installer for Windows

rem Install Apio for the current user without administrator rights.
rem The script uses the official portable Apio bundle, which includes Python.
rem It installs under %LOCALAPPDATA%\Apio, updates the user PATH, and downloads
rem the Apio FPGA packages.

set "APIO_ROOT=%LOCALAPPDATA%\Apio"
set "APIO_DIR=%APIO_ROOT%\apio"
set "APIO_EXE=%APIO_DIR%\apio.exe"
set "TMP_JSON=%TEMP%\apio-release.json"
set "TMP_ZIP=%TEMP%\apio-bundle.zip"
set "TMP_URL=%TEMP%\apio-url.txt"

rem Force per-user locations even if a system-wide Apio installation exists.
set "APIO_HOME="
set "APIO_PACKAGES="

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

echo.
echo === Apio per-user installer for Windows (no admin required) ===
echo.

echo [1/6] Downloading the latest Apio release information...
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

echo [2/6] Downloading the Apio bundle...
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

echo [3/6] Unblocking and extracting...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "Unblock-File -LiteralPath '%TMP_ZIP%' -ErrorAction SilentlyContinue"
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

echo [4/6] Adding Apio to the current user PATH...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$d = Join-Path $env:LOCALAPPDATA 'Apio\apio'; $p = [Environment]::GetEnvironmentVariable('Path','User'); $parts = @(); if ($p) { $parts = $p -split ';' | Where-Object { $_ -ne '' } }; if ($parts -notcontains $d) { if ($parts.Count -eq 0) { $new = $d } else { $new = ($parts + $d) -join ';' }; [Environment]::SetEnvironmentVariable('Path', $new, 'User') }"
if errorlevel 1 (
    echo ERROR: Could not update the user PATH.
    goto :fail
)
set "PATH=%APIO_DIR%;%PATH%"

echo [5/6] Verifying Apio...
"%APIO_EXE%" --version
if errorlevel 1 (
    echo ERROR: Apio did not run correctly.
    goto :fail
)

echo [6/6] Installing Apio FPGA packages...
echo This downloads the openXC7 toolchain and chip databases; it may take a while.
"%APIO_EXE%" packages install
if errorlevel 1 (
    echo ERROR: Apio package installation failed.
    goto :fail
)
"%APIO_EXE%" packages list --check
if errorlevel 1 (
    echo WARNING: Some Apio packages are not healthy.
    echo Run: apio packages install --force
)

del /q "%TMP_JSON%" "%TMP_ZIP%" "%TMP_URL%" 2>nul

echo.
echo ============================================================
echo Apio is installed for the current user.
echo.
echo Open a NEW Command Prompt or PowerShell window and run:
echo   apio --version
echo   apio packages list --check
echo.
echo For the Nexys 4 DDR:
echo   apio examples fetch nexys-a7-100t/blinky
echo   cd blinky
echo   apio build
echo   apio upload
echo.
echo Programming the FPGA still requires a one-time admin step to
echo install the FTDI/WinUSB driver:
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
