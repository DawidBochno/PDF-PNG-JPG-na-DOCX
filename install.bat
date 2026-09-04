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
call :findtess
if not defined TESS (
    echo Nie znaleziono - instaluje przez winget ^(moze pojawic sie okno UAC^)...
    winget install --id UB-Mannheim.TesseractOCR -e --accept-package-agreements --accept-source-agreements
    call :findtess
)
if not defined TESS (
    echo.
    echo BLAD: silnik OCR nadal niedostepny - bez niego skany i zdjecia nie zadzialaja.
    echo Zainstaluj recznie: https://github.com/UB-Mannheim/tesseract/wiki
    pause
    exit /b 1
)
echo OK - %TESS%

echo.
echo ================================
echo Gotowe. Uruchamiaj: program_file-to-docx.bat
echo ================================
pause
exit /b 0

:findtess
rem Instalacja bez praw administratora laduje w folderze uzytkownika, nie w Program Files.
set TESS=
for /f "delims=" %%p in ('where tesseract 2^>nul') do if not defined TESS set TESS=%%p
for %%p in (
    "C:\Program Files\Tesseract-OCR\tesseract.exe"
    "C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    "%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe"
    "%LOCALAPPDATA%\Tesseract-OCR\tesseract.exe"
) do if not defined TESS if exist %%p set TESS=%%~p
exit /b 0
