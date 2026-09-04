# PDF/PNG/JPG → DOCX

Lokalny, wsadowy konwerter dokumentów do edytowalnego Worda. Pliki nie opuszczają komputera — nic nie jest wysyłane do chmury ani do żadnej usługi zewnętrznej.

Wymaga systemu **Windows**.

## Co przetwarza

- **PDF z tekstem** (nie skan) → konwersja bezpośrednia, najlepsza jakość: układ i tabele odtworzone jako prawdziwe, edytowalne elementy Worda.
- **PDF-skan / PNG / JPG** → najpierw OCR (Tesseract, język polski + angielski), dopiero potem konwersja do DOCX.

Program sam rozpoznaje, z którym przypadkiem ma do czynienia — nie trzeba nic przełączać.

## Ograniczenia

- Dobrze radzi sobie z prostymi dokumentami: faktury, WZ, formularze, pisma.
- **Nie odtwarza** struktury logicznej złożonych dokumentów (nagłówki, automatyczny spis treści) — dla wielostronicowych opracowań z rozdziałami wynik będzie linearnym tekstem bez stylów.
- Jakość OCR na obrazach zależy od rozdzielczości i ostrości zdjęcia.

---

## Uruchomienie

Są dwie drogi: **gotowa paczka** dla kogoś, kto ma tylko używać programu, i **wariant ze źródeł** dla rozwijania kodu.

### A. Gotowa paczka — nic nie trzeba instalować

W środku siedzi już Python, wszystkie biblioteki, silnik OCR i pakiet językowy. **Nie wymaga Pythona, internetu ani uprawnień administratora.** Można przenieść na pendrive i uruchomić na obcym komputerze.

Foldery robocze `INPUT/` i `OUTPUT/` tworzą się obok programu.

Paczka nie leży w repozytorium (waży ponad 200 MB, GitHub nie przyjmuje tak dużych plików w kodzie) — buduje się ją poleceniem z sekcji *Budowanie* i przenosi pendrivem. Dostępna w dwóch wariantach:

| Wariant | Co to jest | Start | Kiedy używać |
|---|---|---|---|
| **Jeden plik** | `plik-to-docx.exe` (209 MB) | ~10 s | domyślnie — jedna ikonka, najwygodniej |
| **Folder** | `plik-to-docx/` + zip (210 MB) | ~3 s | gdy antywirus lub UTM blokuje pojedynczy `.exe` |

Wariant folderowy jest szybszy i rzadziej blokowany, bo pojedynczy `.exe` przy każdym starcie rozpakowuje się do katalogu tymczasowego i stamtąd uruchamia — heurystyki antywirusów i UTM traktują to jak zachowanie droppera. Kosztem jest to, że klika się plik wewnątrz folderu, a nie samotną ikonkę.

Przy pierwszym uruchomieniu Windows może pokazać ostrzeżenie SmartScreen („Nieznany wydawca") — to normalne dla niepodpisanego programu: *Więcej informacji* → *Uruchom mimo to*.

### B. Ze źródeł — do rozwijania programu

Wymaga Pythona 3.11–3.13 na PATH oraz internetu (jednorazowo, na pobranie bibliotek).

1. Kliknij `install.bat` — zainstaluje biblioteki Pythona i silnik OCR (Tesseract, jeśli brakuje).
2. Uruchamiaj przez `program_file-to-docx.bat`.

---

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

## Test poprawności

Sprawdza konwersję PDF z tabelą, OCR obrazu i start okna:

```
py -3.13 pdf2doc.py --selftest
```

Ten sam test działa na zbudowanej paczce — `plik-to-docx.exe --selftest` kończy się kodem wyjścia `0`, gdy wszystko działa. Warto tak sprawdzić paczkę po przeniesieniu na inny komputer, zanim odda się ją użytkownikowi.

## Budowanie paczki

Na komputerze z Pythonem 3.13 i zainstalowanym Tesseractem (czyli po `install.bat`):

```
py -3.13 -m pip install -r requirements.txt pyinstaller
py -3.13 build.py
```

Wynik: `dist/plik-to-docx.exe`.

Wariant folderowy:

```
py -3.13 build.py --onedir
```

Wynik: `dist/plik-to-docx/` oraz gotowy do przeniesienia `dist/plik-to-docx-folder.zip`.

Skrypt kopiuje z Tesseracta tylko to, co potrzebne do działania (silnik i biblioteki graficzne), pomijając narzędzia treningowe — to około połowa jego rozmiaru.

### Przenoszenie do sieci z firewallem lub UTM

Paczka jest w pełni offline — nic nie pobiera przy uruchomieniu, więc **w trakcie działania** firewall i UTM nie mają czego blokować. Problemem bywa samo dostarczenie pliku:

- przenoś pendrivem albo jako zip, zamiast pobierać z sieci,
- jeśli UTM odrzuca `.exe` z zasady (niepodpisany plik wykonywalny), użyj wariantu folderowego w zipie,
- w razie blokady poproś dział IT o wyjątek — program działa lokalnie i nie łączy się z internetem, co łatwo uzasadnić.

---

## Problemy

**„Brak Tesseracta (silnika OCR)"**

Dotyczy tylko wariantu ze źródeł — gotowa paczka ma silnik w środku. Repozytorium zawiera pakiet językowy OCR, ale nie sam silnik (to osobny program).

Uruchom `install.bat`. Jeśli instalacja przez winget nie przejdzie (np. nie ma komu kliknąć okna UAC), zainstaluj ręcznie z [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki). Instalacja bez uprawnień administratora też jest w porządku — program sprawdza również folder użytkownika.

Błąd dotyczy wyłącznie skanów, zdjęć i PDF-ów bez warstwy tekstowej. PDF-y z tekstem konwertują się bez Tesseracta.

**Program znika zaraz po uruchomieniu (wariant ze źródeł)**

Zwykle oznacza Pythona bez zainstalowanych bibliotek. Uruchom `install.bat` i spróbuj ponownie.

---

## Co jest w repozytorium, a co nie

Podział jest celowy:

| | Gdzie żyje | Dlaczego |
|---|---|---|
| Kod, skrypty, pakiet językowy OCR | **w repozytorium** (~23 MB) | to się pisze i rozwija; pakiet językowy jest dołączony, żeby nic nie trzeba było dociągać z sieci |
| Zbudowana paczka, `dist/`, `build/`, zipy | **poza repozytorium** | to się generuje z kodu, waży setki MB i przekracza limity GitHuba |

Ciężką paczkę odtwarza się w każdej chwili jednym poleceniem, więc nie ma potrzeby jej wersjonować. Przenosi się ją pendrivem, nie przez GitHuba.

## Struktura

- `pdf2doc.py` — cały program (GUI + logika konwersji)
- `build.py` — buduje gotową paczkę
- `install.bat` — instalacja zależności dla wariantu ze źródeł
- `program_file-to-docx.bat` — uruchamia program ze źródeł
- `requirements.txt` — biblioteki Pythona
- `tessdata/` — pakiet językowy OCR (pol + eng), dołączony na stałe
- `INPUT/`, `OUTPUT/` — foldery robocze (ich zawartość nie trafia do repozytorium)

## Użyte składniki

- [pdf2docx](https://github.com/ArtifexSoftware/pdf2docx) i [PyMuPDF](https://github.com/pymupdf/PyMuPDF) — analiza PDF i odtwarzanie układu
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (Apache 2.0) — silnik OCR; gotowa paczka zawiera jego pliki wykonywalne, co licencja dopuszcza
- [tessdata](https://github.com/tesseract-ocr/tessdata) — modele językowe pol + eng
