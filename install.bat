@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
echo.
echo === PDF/PNG/JPG -^> DOCX - INSTALATOR ===
echo.

set PYCMD=
for %%v in (3.13 3.12 3.11) do (
    if not defined PYCMD (
        py -%%v -c "1" >nul 2>&1 && set PYCMD=py -%%v
    )
)
if not defined PYCMD (
    echo BLAD: nie znaleziono Pythona 3.11-3.13.
    echo Zainstaluj z https://www.python.org ^(zaznacz "Add python.exe to PATH"^)
    pause
    exit /b 1
)
echo Uzyty Python: %PYCMD%

echo.
echo [1/2] Instaluje biblioteki Pythona...
%PYCMD% -m pip install -q -r requirements.txt
if errorlevel 1 (
    echo BLAD instalacji bibliotek.
    pause
    exit /b 1
)
echo OK

echo.
echo [2/2] Sprawdzam silnik OCR (Tesseract)...
where tesseract >nul 2>&1
if errorlevel 1 (
    if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
        echo OK - juz zainstalowany
    ) else (
        echo Nie znaleziono - instaluje przez winget ^(moze pojawic sie okno UAC^)...
        winget install --id UB-Mannheim.TesseractOCR -e --accept-package-agreements --accept-source-agreements
        if errorlevel 1 (
            echo BLAD: zainstaluj recznie: https://github.com/UB-Mannheim/tesseract/wiki
            pause
            exit /b 1
        )
    )
) else (
    echo OK - juz zainstalowany
)

echo.
echo ================================
echo Gotowe. Uruchamiaj: program_file-to-docx.bat
echo ================================
pause
