@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
for %%v in (3.13 3.12 3.11) do (
    if not defined PYV (
        py -%%v -c "import pdf2docx" >nul 2>&1 && set PYV=%%v
    )
)
if not defined PYV (
    echo Nie znaleziono Pythona z zainstalowanymi bibliotekami.
    echo Uruchom najpierw: install.bat
    pause
    exit /b 1
)
start "" pyw -%PYV% "%~dp0pdf2doc.py"
