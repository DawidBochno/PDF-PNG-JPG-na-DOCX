"""PDF/PNG/JPG -> DOCX. Wsadowo, z zachowaniem ukladu i tabel.

PDF z tekstem (nie skan) idzie prosto do konwersji - najlepsza jakosc.
Obrazy i zeskanowane PDF-y najpierw przechodza przez OCR (Tesseract, pol+eng),
ktory dokleja niewidoczna warstwe tekstu, a dopiero potem trafiaja do konwersji.

Okienko: wskaz pliki albo folder INPUT, wskaz OUTPUT, klikaj Konwertuj.
Konsola: python pdf2doc.py INPUT_folder OUTPUT_folder
Test:    python pdf2doc.py --selftest
"""
import queue
import shutil
import subprocess
import sys
import tempfile
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import pymupdf
from pdf2docx import Converter

HERE = Path(__file__).parent
IN_DIR = HERE / "INPUT"
OUT_DIR = HERE / "OUTPUT"
TESSDATA_DIR = HERE / "tessdata"
IMAGE_EXTS = {".png", ".jpg", ".jpeg"}
DPI = 300


def find_tesseract() -> str:
    """Szuka silnika OCR. Instalator bez praw administratora wrzuca go do
    folderu uzytkownika, a nie do Program Files - stad kilka lokalizacji.
    """
    import os
    found = shutil.which("tesseract")
    if found:
        return found
    local = os.environ.get("LOCALAPPDATA", "")
    for cand in (
        HERE / "tesseract" / "tesseract.exe",
        Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe"),
        Path(r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"),
        Path(local) / "Programs" / "Tesseract-OCR" / "tesseract.exe",
        Path(local) / "Tesseract-OCR" / "tesseract.exe",
    ):
        if cand.exists():
            return str(cand)
    raise FileNotFoundError(
        "Brak Tesseracta (silnika OCR) - jest potrzebny do skanow i zdjec.\n"
        "Uruchom install.bat, albo zainstaluj recznie:\n"
        "https://github.com/UB-Mannheim/tesseract/wiki"
    )


def _ocr_page_to_pdf(png_bytes: bytes, out_base: Path) -> Path:
    """OCR-uje jeden obraz (bajty PNG) i zwraca PDF z niewidoczna warstwa tekstu.

    Jezyk bierzemy z wlasnego folderu tessdata/ (przenosnie, bez uprawnien
    administratora) - stad TESSDATA_PREFIX zamiast --tessdata-dir, ktore w
    tesseract 5 psuje parsowanie nastepujacego po nim configfile "pdf".
    """
    import os
    env = {**os.environ, "TESSDATA_PREFIX": str(TESSDATA_DIR)}
    subprocess.run(
        [find_tesseract(), "-", str(out_base), "-l", "pol+eng", "--dpi", str(DPI), "pdf"],
        input=png_bytes, check=True, capture_output=True, env=env,
    )
    return out_base.with_suffix(".pdf")


def make_searchable(src: Path, tmp: Path) -> Path:
    """Zwraca PDF z warstwa tekstu gotowy do pdf2docx. Cyfrowy PDF (z tekstem)
    oddaje bez zmian - to daje najlepsza jakosc. Obraz albo skan bez tekstu
    najpierw OCR-uje strona po stronie."""
    if src.suffix.lower() in IMAGE_EXTS:
        png = pymupdf.open()  # tylko po to, by ujednolicic ladowanie obrazu
        pix = pymupdf.Pixmap(str(src))
        if pix.n - pix.alpha >= 4:  # CMYK -> RGB, tesseract tego nie lubi
            pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
        return _ocr_page_to_pdf(pix.tobytes("png"), tmp / src.stem)

    doc = pymupdf.open(src)
    has_text = any(p.get_text().strip() for p in doc)
    if has_text:
        doc.close()
        return src

    out = pymupdf.open()
    for i, page in enumerate(doc):
        png = page.get_pixmap(dpi=DPI).tobytes("png")
        page_pdf = _ocr_page_to_pdf(png, tmp / f"p{i}")
        with pymupdf.open(page_pdf) as one:
            out.insert_pdf(one)
    doc.close()
    dst = tmp / f"{src.stem}_ocr.pdf"
    out.save(dst)
    out.close()
    return dst


def convert_one(src: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    docx = out_dir / f"{src.stem}.docx"
    with tempfile.TemporaryDirectory() as td:
        pdf = make_searchable(src, Path(td))
        # pdf po naszym OCR ma tylko niewidoczna warstwe tekstu (bez wizualnych
        # glifow) - domyslnie pdf2docx taki tekst odrzuca (ocr=0), wiec dla
        # wlasnie zrobionego OCR mowimy mu wprost: to jest tekst z OCR (ocr=2)
        ocr_mode = 2 if pdf != src else 0
        c = Converter(str(pdf))
        try:
            c.convert(str(docx), ocr=ocr_mode)
        finally:
            c.close()
    return docx


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF/PNG/JPG -> DOCX")
        self.geometry("720x460")
        self.files: list[Path] = []
        self.log_q: queue.Queue[str] = queue.Queue()

        IN_DIR.mkdir(exist_ok=True)
        self.out_var = tk.StringVar(value=str(OUT_DIR))

        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        ttk.Button(top, text="Wybierz pliki...", command=self.pick_files).grid(row=0, column=0, sticky="w")
        ttk.Button(top, text="Wybierz folder INPUT...", command=self.pick_folder).grid(row=0, column=1, padx=6)
        self.src_lbl = ttk.Label(top, text="nic nie wybrano", foreground="gray")
        self.src_lbl.grid(row=1, column=0, columnspan=3, sticky="w", pady=(6, 12))

        ttk.Label(top, text="Folder OUTPUT:").grid(row=2, column=0, sticky="w")
        ttk.Entry(top, textvariable=self.out_var, width=62).grid(row=3, column=0, columnspan=2, sticky="we")
        ttk.Button(top, text="Zmien...", command=self.pick_out).grid(row=3, column=2, padx=6)

        self.btn = ttk.Button(self, text="Konwertuj", command=self.start)
        self.btn.pack(pady=10)
        self.bar = ttk.Progressbar(self, mode="determinate")
        self.bar.pack(fill="x", padx=10)
        self.log = tk.Text(self, height=14, wrap="none")
        self.log.pack(fill="both", expand=True, padx=10, pady=10)

        # domyslnie bierz to, co lezy w INPUT
        self.load(self._scan(IN_DIR), str(IN_DIR))
        self.after(100, self.drain)

    @staticmethod
    def _scan(folder: Path):
        exts = {".pdf", *IMAGE_EXTS}
        return sorted(p for p in folder.glob("*") if p.suffix.lower() in exts)

    def load(self, files, where):
        self.files = list(files)
        n = len(self.files)
        self.src_lbl.config(
            text=f"{n} plik(ow) z: {where}" if n else f"brak plikow PDF/PNG/JPG w: {where}",
            foreground="black" if n else "gray",
        )

    def pick_files(self):
        f = filedialog.askopenfilenames(
            title="Wybierz pliki",
            filetypes=[("PDF/PNG/JPG", "*.pdf *.png *.jpg *.jpeg"), ("Wszystkie", "*.*")],
        )
        if f:
            self.load([Path(x) for x in f], "wybor reczny")

    def pick_folder(self):
        d = filedialog.askdirectory(title="Folder ze zrodlowymi plikami")
        if d:
            self.load(self._scan(Path(d)), d)

    def pick_out(self):
        d = filedialog.askdirectory(title="Folder wyjsciowy")
        if d:
            self.out_var.set(d)

    def start(self):
        if not self.files:
            messagebox.showwarning("PDF -> DOCX", "Najpierw wskaz pliki albo folder.")
            return
        self.btn.config(state="disabled")
        self.log.delete("1.0", "end")
        self.bar.config(value=0, maximum=len(self.files))
        threading.Thread(target=self.work, args=(list(self.files), Path(self.out_var.get())),
                         daemon=True).start()

    def work(self, files, out_dir):
        ok = 0
        for i, pdf in enumerate(files, 1):
            try:
                docx = convert_one(pdf, out_dir)
                ok += 1
                self.log_q.put(f"[{i}/{len(files)}] OK   {pdf.name} -> {docx.name}")
            except Exception as e:  # jeden zly plik nie moze zatrzymac reszty
                self.log_q.put(f"[{i}/{len(files)}] BLAD {pdf.name}: {e}")
            self.log_q.put(f"__progress__{i}")
        self.log_q.put(f"__done__Gotowe: {ok}/{len(files)} przekonwertowanych -> {out_dir}")

    def drain(self):
        while not self.log_q.empty():
            msg = self.log_q.get()
            if msg.startswith("__progress__"):
                self.bar.config(value=int(msg[12:]))
            elif msg.startswith("__done__"):
                self.log.insert("end", msg[8:] + "\n")
                self.btn.config(state="normal")
            else:
                self.log.insert("end", msg + "\n")
            self.log.see("end")
        self.after(100, self.drain)


def selftest():
    import tempfile
    import zipfile

    import pymupdf

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        src = td / "t.pdf"
        doc = pymupdf.open()
        page = doc.new_page()
        page.insert_text((72, 100), "WZ nr: 1/05-2018")
        page.draw_rect(pymupdf.Rect(72, 150, 400, 180))
        page.draw_line(pymupdf.Point(236, 150), pymupdf.Point(236, 180))
        page.insert_text((80, 170), "produkt 1")
        page.insert_text((250, 170), "1.00")
        doc.save(src)
        doc.close()

        out = convert_one(src, td / "OUT")
        assert out.exists() and out.stat().st_size > 0, "brak pliku docx"
        xml = zipfile.ZipFile(out).read("word/document.xml").decode("utf8")
        assert "1/05-2018" in xml, "zgubiony tekst"
        assert "<w:tbl>" in xml, "tabela nie odtworzona"

        # obraz -> OCR -> docx
        png = td / "t.png"
        img = pymupdf.open()
        p = img.new_page(width=400, height=150)
        p.insert_text((20, 60), "Zamowienie nr 42", fontsize=24)
        img[0].get_pixmap(dpi=200).save(png)
        img.close()

        out2 = convert_one(png, td / "OUT")
        assert out2.exists() and out2.stat().st_size > 0, "OCR: brak pliku docx"
        xml2 = zipfile.ZipFile(out2).read("word/document.xml").decode("utf8")
        assert "42" in xml2, f"OCR nie odczytal tekstu z obrazu: {xml2[:300]}"
    print("selftest OK")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--selftest":
        selftest()
    elif args:  # tryb konsolowy: INPUT [OUTPUT]
        src = Path(args[0])
        dst = Path(args[1]) if len(args) > 1 else OUT_DIR
        files = App._scan(src) if src.is_dir() else [src]
        for p in files:
            print(f"{p.name} -> {convert_one(p, dst)}")
    else:
        App().mainloop()
