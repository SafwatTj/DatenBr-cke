# gui.py

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from excel_parser import parse_excel
from pdf_parser import parse_pdf
from database import SessionLocal, create_tables
from models import Dokument
import json

class DatenBrueckeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DatenBrücke - Excel/PDF Parser")
        self.root.geometry("750x580")
        self.root.configure(bg="#2c3e50")

        self.dateipfad = tk.StringVar()

        # Farben
        bg_color = "#2c3e50"
        fg_color = "#ecf0f1"
        btn_color = "#3498db"
        log_bg = "#34495e"

        # Hauptframe
        main_frame = tk.Frame(root, bg=bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Titel und Entwickler
        tk.Label(main_frame, text="DATENBRÜCKE", font=("Arial", 18, "bold"), bg=bg_color, fg="#f39c12").pack(pady=(10,0))
        tk.Label(main_frame, text="Excel/PDF Parser | SQLite-Datenbank", font=("Arial", 9), bg=bg_color, fg="#bdc3c7").pack(pady=(0,5))
        tk.Label(main_frame, text="entwickelt von SAFWAT BURKHONOV", font=("Arial", 8, "italic"), bg=bg_color, fg="#95a5a6").pack(pady=(0,15))

        # Dateipfad
        tk.Label(main_frame, text="Dateipfad:", bg=bg_color, fg=fg_color, font=("Arial", 10)).pack(anchor=tk.W)
        pfad_frame = tk.Frame(main_frame, bg=bg_color)
        pfad_frame.pack(fill=tk.X, pady=5)
        tk.Entry(pfad_frame, textvariable=self.dateipfad, width=50, bg="#ecf0f1", font=("Arial", 9)).pack(side=tk.LEFT, padx=(0,10), fill=tk.X, expand=True)
        tk.Button(pfad_frame, text="📂 Auswählen", command=self.datei_auswaehlen, bg=btn_color, fg="white", font=("Arial", 9), relief=tk.FLAT, cursor="hand2").pack(side=tk.RIGHT)

        # Dateityp
        tk.Label(main_frame, text="Dateityp:", bg=bg_color, fg=fg_color, font=("Arial", 10)).pack(anchor=tk.W, pady=(10,0))
        self.modus_frame = tk.Frame(main_frame, bg=bg_color)
        self.modus_frame.pack(anchor=tk.W, pady=5)
        self.modus_var = tk.StringVar(value="excel")
        tk.Radiobutton(self.modus_frame, text="📊 Excel (.xlsx, .xls)", variable=self.modus_var, value="excel", bg=bg_color, fg=fg_color, selectcolor=bg_color, activebackground=bg_color, font=("Arial", 9)).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(self.modus_frame, text="📄 PDF", variable=self.modus_var, value="pdf", bg=bg_color, fg=fg_color, selectcolor=bg_color, activebackground=bg_color, font=("Arial", 9)).pack(side=tk.LEFT, padx=10)

        # Parsen Button
        self.parse_btn = tk.Button(main_frame, text="🚀 Parsen & Speichern", command=self.parsen_und_speichern, bg="#e67e22", fg="white", font=("Arial", 11, "bold"), relief=tk.FLAT, cursor="hand2", padx=10, pady=5)
        self.parse_btn.pack(pady=15)

        # Log-Bereich
        tk.Label(main_frame, text="Log-Ausgabe:", bg=bg_color, fg=fg_color, font=("Arial", 10)).pack(anchor=tk.W)
        self.log_text = scrolledtext.ScrolledText(main_frame, width=80, height=12, bg=log_bg, fg=fg_color, font=("Consolas", 9), relief=tk.FLAT, borderwidth=0)
        self.log_text.pack(pady=5, fill=tk.BOTH, expand=True)

        create_tables()
        self.log("✅ Datenbank bereit (SQLite)")
        self.log("📌 Entwickelt von Safwat Burkhonov")

    def log(self, nachricht):
        self.log_text.insert(tk.END, nachricht + "\n")
        self.log_text.see(tk.END)

    def datei_auswaehlen(self):
        datei = filedialog.askopenfilename(filetypes=[("Excel Dateien", "*.xlsx *.xls"), ("PDF Dateien", "*.pdf")])
        if datei:
            self.dateipfad.set(datei)
            self.log(f"📁 Ausgewählt: {datei}")

    def parsen_und_speichern(self):
        pfad = self.dateipfad.get()
        if not pfad:
            messagebox.showerror("Fehler", "Bitte wähle eine Datei aus.")
            return

        modus = self.modus_var.get()
        self.log(f"🔄 Starte Parser für: {pfad} (Typ: {modus})")

        if modus == "excel":
            ergebnis = parse_excel(pfad)
        else:
            ergebnis = parse_pdf(pfad)

        if ergebnis["status"] == "fehler":
            self.log(f"❌ Fehler: {ergebnis['fehler']}")
            messagebox.showerror("Parser Fehler", ergebnis['fehler'])
            return

        # In DB speichern
        db = SessionLocal()
        try:
            neuer_eintrag = Dokument(
                dateiname=pfad,
                quelle=ergebnis["quelle"],
                daten_inhalt=ergebnis.get("daten")
            )
            db.add(neuer_eintrag)
            db.commit()
            self.log(f"✅ Erfolg! {ergebnis.get('zeilen', 0)} Zeilen extrahiert und gespeichert.")
            messagebox.showinfo("Erfolg", "Daten wurden erfolgreich gespeichert!")
        except Exception as e:
            self.log(f"❌ DB-Fehler: {e}")
            db.rollback()
        finally:
            db.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = DatenBrueckeGUI(root)
    root.mainloop()