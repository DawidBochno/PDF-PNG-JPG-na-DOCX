# PDF/PNG/JPG → DOCX

Lokalny, wsadowy konwerter dokumentów do edytowalnego Worda. Działa offline (poza jednorazową instalacją), bez wysyłania plików gdziekolwiek.

## Co przetwarza

- **PDF z tekstem** (nie skan) → konwersja bezpośrednia, najlepsza jakość: układ i tabele odtworzone jako prawdziwe, edytowalne elementy Worda.
- **PDF-skan / PNG / JPG** → najpierw OCR (Tesseract, język polski + angielski), dopiero potem konwersja do DOCX.

Program sam rozpoznaje, z którym przypadkiem ma do czynienia — nie trzeba nic przełączać.

## Ograniczenia

- Dobrze radzi sobie z prostymi dokumentami: faktury, WZ, formularze, pisma.
- **Nie odtwarza** struktury logicznej złożonych dokumentów (nagłówki, automatyczny spis treści) — dla wielostronicowych opracowań z rozdziałami wynik będzie linearnym tekstem bez stylów.
- Jakość OCR na obrazach zależy od rozdzielczości/ostrości zdjęcia.

## Uruchomienie — dwa warianty

### A. Gotowy plik `.exe` (zalecany, nic nie trzeba instalować)

Jeden plik `plik-to-docx.exe` — kliknąć i działa. W środku siedzi już Python, wszystkie biblioteki, silnik OCR i pakiet językowy. **Nie wymaga Pythona, internetu ani uprawnień administratora.** Można go przenieść na pendrive.

Foldery `INPUT/` i `OUTPUT/` tworzą się obok `.exe`.

> Plik waży ~209 MB, więc nie leży w repozytorium (GitHub nie przyjmuje tak dużych plików w kodzie). Buduje się go samodzielnie — patrz *Budowanie* niżej — albo pobiera z sekcji *Releases*.

Przy pierwszym uruchomieniu Windows może pokazać ostrzeżenie SmartScreen („Nieznany wydawca") — to normalne dla niepodpisanego programu: *Więcej informacji* → *Uruchom mimo to*.

### B. Ze źródeł (dla rozwijania programu)

Wymaga Pythona 3.11–3.13 na PATH oraz internetu (jednorazowo).

1. Kliknij `install.bat` — zainstaluje biblioteki Pythona i silnik OCR (Tesseract, jeśli brakuje).
2. Uruchamiaj przez `program_file-to-docx.bat`.

## Użycie

W oknie programu:
- wskaż pliki (można zaznaczyć wiele naraz) albo cały folder,
- wskaż folder wyjściowy,
- kliknij *Konwertuj*.

Domyślnie program podnosi pliki z folderu `INPUT/` i zapisuje wynik do `OUTPUT/`.

Tryb konsolowy:

```
py -3.13 pdf2doc.py INPUT_folder OUTPUT_folder
```

Test poprawności działania (konwersja PDF + OCR obrazu + start okna):

```
py -3.13 pdf2doc.py --selftest
```

Ten sam test działa na zbudowanym pliku — `plik-to-docx.exe --selftest` kończy się kodem `0`, gdy wszystko gra.

## Budowanie pliku `.exe`

Na komputerze z Pythonem 3.13 i zainstalowanym Tesseractem (`install.bat`):

```
py -3.13 -m pip install -r requirements.txt pyinstaller
py -3.13 build.py
```

Wynik: `dist/plik-to-docx.exe`. Skrypt sam wybiera z Tesseracta tylko to, co potrzebne do działania (silnik i biblioteki graficzne), pomijając narzędzia treningowe — to około połowa jego rozmiaru.

## Problemy

**„Brak Tesseracta (silnika OCR)"** — dotyczy tylko wariantu ze źródeł; `.exe` ma silnik w środku. Repozytorium zawiera pakiet językowy OCR, ale nie sam silnik (to osobny program). Uruchom `install.bat`; jeśli instalacja przez winget nie przejdzie (np. brak zgody UAC), zainstaluj ręcznie z [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki). Instalacja bez uprawnień administratora też jest OK — program sprawdza również folder użytkownika.

Dotyczy tylko skanów, zdjęć i PDF-ów bez warstwy tekstowej. PDF-y z tekstem konwertują się bez Tesseracta.

## Struktura

- `pdf2doc.py` — cały program (GUI + logika konwersji)
- `build.py` — buduje samodzielny `.exe`
- `install.bat` — instalacja zależności dla wariantu ze źródeł
- `program_file-to-docx.bat` — uruchamia program ze źródeł
- `tessdata/` — pakiet językowy OCR (pol + eng), dołączony na stałe — nie trzeba niczego dodatkowo pobierać
- `INPUT/`, `OUTPUT/` — foldery robocze (zawartość nie jest wysyłana do repozytorium)
