"""Buduje samodzielny plik-to-docx.exe - jeden plik, bez Pythona i bez instalacji.

Do paczki trafiaja: Python, biblioteki, pakiet jezykowy tessdata/ oraz silnik
OCR (tesseract.exe + biblioteki .dll). Narzedzia treningowe Tesseracta sa
pomijane - to polowa jego rozmiaru, a program ich nie uzywa.

Uzycie:  py -3.13 build.py
Wynik:   dist/plik-to-docx.exe
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
STAGE = HERE / "build" / "tesseract"
NAME = "plik-to-docx"

TESS_DIRS = [
    Path(r"C:\Program Files\Tesseract-OCR"),
    Path(r"C:\Program Files (x86)\Tesseract-OCR"),
    Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Tesseract-OCR",
]


def collect_tesseract() -> Path:
    """Kopiuje minimalny zestaw plikow silnika OCR do build/tesseract/."""
    src = next((d for d in TESS_DIRS if (d / "tesseract.exe").exists()), None)
    if src is None:
        sys.exit(
            "Nie znaleziono zainstalowanego Tesseracta - jest potrzebny do zbudowania\n"
            "paczki (kopiujemy z niego silnik OCR). Uruchom najpierw install.bat."
        )
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)
    for f in src.iterdir():
        if f.is_file() and (f.suffix.lower() == ".dll" or f.name == "tesseract.exe"):
            shutil.copy2(f, STAGE / f.name)
    mb = sum(f.stat().st_size for f in STAGE.iterdir()) / 1024 / 1024
    print(f"[build] silnik OCR z {src} -> {len(list(STAGE.iterdir()))} plikow, {mb:.0f} MB")
    return STAGE


def main() -> None:
    tess = collect_tesseract()
    if not (HERE / "tessdata" / "configs" / "pdf").exists():
        sys.exit("Brak tessdata/configs/pdf - bez tego OCR nie zapisze PDF-a.")

    cmd = [
        sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean",
        "--onefile", "--windowed", "--name", NAME,
        "--add-data", f"{HERE / 'tessdata'}{os.pathsep}tessdata",
        "--add-data", f"{tess}{os.pathsep}tesseract",
        str(HERE / "pdf2doc.py"),
    ]
    print("[build] PyInstaller...")
    subprocess.run(cmd, check=True, cwd=HERE)

    exe = HERE / "dist" / f"{NAME}.exe"
    print(f"[build] gotowe: {exe} ({exe.stat().st_size / 1024 / 1024:.0f} MB)")


if __name__ == "__main__":
    main()
