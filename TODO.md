# Lista pomysłów (TODO)

Pomysły na rozwój programu, od największego zysku dla typowych plików
(skany pism urzędowych z pieczątkami). Każdy punkt to osobny, mały PR.
Odhaczone `[x]` = zrobione.

## Jakość OCR

- [ ] **Przygotowanie obrazu przed OCR** — prostowanie krzywego skanu,
  kontrast, odszumianie. Pomaga przy błędach w polskich znakach na skanach
  w niskiej rozdzielczości („Majac” zamiast „Mając”).
- [ ] **Słownik poprawek** — plik tekstowy z parami `błąd → poprawka`
  (np. „Zyrardów” → „Żyrardów”), uzupełniany przez użytkownika i stosowany
  po OCR.
- [ ] **Dokładniejszy model polskiego** (`tessdata_best/pol`) — wolniejszy
  (ok. 2×). Najpierw zmierzyć różnicę na prawdziwych skanach.

## Wierność układu

- [ ] **Logo, pieczątki, podpisy jako obrazki** — fragmenty skanu bez tekstu
  wycinane i wstawiane do DOCX w tym samym miejscu.
- [ ] **Tabele w skanach** — wykrywanie linii tabeli na obrazie i budowa
  prawdziwej tabeli Worda (formularze, faktury). Najwięcej pracy.
- [ ] **Wyrównanie do prawej / do środka** — np. „Żyrardów, dnia …”, tytuł
  „Wniosek”. Dziś odwzorowane wcięciem.
- [ ] **Pogrubienie** — wykrywanie grubszych liter (nagłówki, „UZASADNIENIE”).

## Wygoda

- [ ] **Podgląd przed zapisem** — oryginał obok rozpoznanego tekstu,
  podświetlone słowa, których OCR był niepewny.
- [ ] **Przeciągnij i upuść** plików na okno.
- [ ] **Szybsza praca** — OCR kilku stron naraz na wszystkich rdzeniach
  (dziś ok. 1,5 s na stronę).
- [ ] **Otwórz wynik po konwersji** — przycisk „Otwórz folder OUTPUT” /
  podwójne kliknięcie pliku w logu.
- [ ] **Raport jakości** — w logu średnia pewność OCR każdego pliku,
  ostrzeżenie przy słabym skanie.

## Opcjonalne ustawienia (w oknie, domyślnie jak dziś)

Pole wyboru / lista w oknie, zapamiętywane między uruchomieniami
(plik `ustawienia.json` obok programu).

- [ ] **Format wyjścia**: DOCX (domyślnie) / PDF z warstwą tekstu
  (przeszukiwalny skan) / TXT.
- [x] **Język OCR**: polski + angielski (domyślnie) / tylko polski /
  dodatkowo niemiecki, ukraiński (modele `tessdata_fast` w `tessdata/`).
- [x] **Zakres stron**: np. `1-3, 5` z długiego PDF-a.
- [x] **Pomijanie pustych stron**: włączone (domyślnie) / wyłączone.
- [ ] **Czułość filtra śmieci** (próg pewności OCR): łagodny / normalny /
  ostry — przy pieczątkach na tekście.
- [ ] **Czcionka i rozmiar**: automatycznie (domyślnie) / wybrana czcionka
  (np. Arial, Calibri) i rozmiar.
- [ ] **Wymuś OCR** także dla PDF-ów z tekstem — gdy warstwa tekstu jest
  zepsuta (krzaki po kopiowaniu).
- [ ] **Tryb „tylko tekst”** — bez wcięć i odstępów, same akapity
  (do wklejania w inne pismo).
- [ ] **Podział stron**: każda strona od nowej strony (domyślnie) /
  ciągły tekst.
- [ ] **Jeden plik zbiorczy** — wszystkie wybrane pliki do jednego DOCX
  (np. pismo + załączniki).
- [ ] **Nazwa pliku wyjściowego**: jak źródło (domyślnie) / z dopiskiem
  daty / z dopiskiem `_OCR`.
- [ ] **Nadpisywanie**: pytaj / nadpisz / dopisz numer `(2)`.
- [ ] **Rozdzielczość OCR** (DPI): 300 (domyślnie) / 400 przy drobnym druku.
- [ ] **Usuń plik źródłowy z INPUT po udanej konwersji** (przeniesienie do
  `INPUT/zrobione/`, bez kasowania).

## Integracja z innymi programami

- [ ] **Anonimizacja po konwersji** — opcja wywołująca program
  *Anonimizacja RODO* na gotowym DOCX (PESEL, nazwiska, adresy).
  Programy pozostają osobne — jeden tylko uruchamia drugi.
