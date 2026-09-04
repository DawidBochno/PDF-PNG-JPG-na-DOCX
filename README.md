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

### A2. Wariant folderowy — gdy sieć ma UTM albo antywirus blokuje `.exe`

`build.py --onedir` daje folder `plik-to-docx/` (plus gotowy zip do przeniesienia). Klika się `plik-to-docx.exe` w środku.

Dwie przewagi nad pojedynczym plikiem:

- **Rzadziej blokowany.** Pojedynczy `.exe` rozpakowuje się przy każdym starcie do katalogu tymczasowego i stamtąd uruchamia — heurystyki antywirusów i UTM traktują to jak zachowanie droppera. Wariant folderowy tego nie robi.
- **Startuje szybciej** — ok. 3 s zamiast 10 s, bo nie musi za każdym razem rozpakowywać 209 MB.

Wada: to folder, a nie jedna ikonka.

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

Wynik: `dist/plik-to-docx.exe`. Wariant folderowy: `py -3.13 build.py --onedir` → `dist/plik-to-docx/` oraz `dist/plik-to-docx-folder.zip`.

Skrypt sam wybiera z Tesseracta tylko to, co potrzebne do działania (silnik i biblioteki graficzne), pomijając narzędzia treningowe — to około połowa jego rozmiaru.

### Przenoszenie do sieci z UTM

Paczka jest offline — nic nie pobiera przy uruchomieniu, więc firewall i UTM nie mają czego blokować **w trakcie działania**. Problemem bywa samo dostarczenie pliku:

- przenoś pendrivem albo jako zip, nie przez pobieranie z sieci,
- jeśli UTM odrzuca `.exe` z zasady (niepodpisany plik wykonywalny), użyj wariantu folderowego w zipie,
- w razie blokady poproś dział IT o wyjątek dla konkretnego pliku — program jest lokalny i nie łączy się z internetem, co łatwo uzasadnić.

## Problemy

**„Brak Tesseracta (silnika OCR)"** — dotyczy tylko wariantu ze źródeł; `.exe` ma silnik w środku. Repozytorium zawiera pakiet językowy OCR, ale nie sam silnik (to osobny program). Uruchom `install.bat`; jeśli instalacja przez winget nie przejdzie (np. brak zgody UAC), zainstaluj ręcznie z [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki). Instalacja bez uprawnień administratora też jest OK — program sprawdza również folder użytkownika.

Dotyczy tylko skanów, zdjęć i PDF-ów bez warstwy tekstowej. PDF-y z tekstem konwertują się bez Tesseracta.

## Co jest w repozytorium, a co nie

Podział jest celowy:

| | Gdzie żyje | Dlaczego |
|---|---|---|
| Kod, skrypty, pakiet językowy OCR | **w repozytorium** (~23 MB) | to się pisze i rozwija; pakiet językowy jest dołączony, żeby nic nie trzeba było dociągać z sieci |
| Zbudowany `.exe`, folder `dist/`, zipy | **poza repozytorium** | to się generuje z kodu, waży setki MB i przekracza limity GitHuba |

Ciężką paczkę odtwarza się w każdej chwili poleceniem z sekcji *Budowanie* — nie ma potrzeby jej wersjonować. Przenosi się ją pendrivem, nie przez GitHuba.

## Struktura

- `pdf2doc.py` — cały program (GUI + logika konwersji)
- `build.py` — buduje samodzielny `.exe`
- `install.bat` — instalacja zależności dla wariantu ze źródeł
- `program_file-to-docx.bat` — uruchamia program ze źródeł
- `tessdata/` — pakiet językowy OCR (pol + eng), dołączony na stałe — nie trzeba niczego dodatkowo pobierać
- `INPUT/`, `OUTPUT/` — foldery robocze (zawartość nie jest wysyłana do repozytorium)
