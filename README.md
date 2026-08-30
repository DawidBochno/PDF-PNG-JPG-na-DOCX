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

## Instalacja

Wymaga Pythona 3.11–3.13 na PATH oraz internetu (jednorazowo).

1. Kliknij `install.bat` — zainstaluje biblioteki Pythona i silnik OCR (Tesseract, jeśli brakuje).
2. Gotowe.

## Użycie

Kliknij `program_file-to-docx.bat`. W oknie:
- wskaż pliki (można zaznaczyć wiele naraz) albo cały folder,
- wskaż folder wyjściowy,
- kliknij *Konwertuj*.

Domyślnie program podnosi pliki z folderu `INPUT/` i zapisuje wynik do `OUTPUT/`.

Tryb konsolowy:

```
py -3.11 pdf2doc.py INPUT_folder OUTPUT_folder
```

Test poprawności działania:

```
py -3.11 pdf2doc.py --selftest
```

## Struktura

- `pdf2doc.py` — cały program (GUI + logika konwersji)
- `tessdata/` — pakiet językowy OCR (pol + eng), dołączony na stałe — nie trzeba niczego dodatkowo pobierać
- `INPUT/`, `OUTPUT/` — foldery robocze (zawartość nie jest wysyłana do repozytorium)
