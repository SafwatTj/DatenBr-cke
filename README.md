# DatenBrücke – Excel/PDF Parser mit SQLite-Datenbank

**DatenBrücke** ist ein Desktop-Tool zum Extrahieren von Daten aus Excel- (`.xlsx`, `.xls`) und PDF-Dateien und deren Speicherung in einer SQLite-Datenbank. Entwickelt von **Safwat Burkhonov**, Java Fullstack Developer mit über 15 Jahren Erfahrung in 3D-Visualisierung, Kryptographie und IT-Sicherheit.

![GUI Screenshot](screenshot.png)

---

## 🚀 Funktionen

- 📊 **Excel-Parser** – Unterstützt `.xlsx` (openpyxl) und `.xls` (xlrd)
- 📄 **PDF-Parser** – Textextraktion mit PyPDF2
- 💾 **SQLite-Datenbank** – Automatische Speicherung aller extrahierten Daten
- 🖥️ **Deutschsprachige GUI** – Einfache Bedienung mit Tkinter
- 📦 **Einzelne EXE-Datei** – Keine Python-Installation nötig

---

## 📥 Download & Installation

### Für Endbenutzer (kein Python erforderlich)

1. Gehe zu **Releases**:  
   [https://github.com/SafwatTj/DatenBr-cke/releases](https://github.com/SafwatTj/DatenBr-cke/releases)

2. Lade `DatenBruecke.exe` herunter

3. Führe die `.exe` aus (keine Installation nötig)

### Für Entwickler (aus dem Quellcode)

```bash
git clone https://github.com/SafwatTj/DatenBr-cke.git
cd DatenBr-cke
pip install -r requirements.txt
python gui.py
