# main.py

from excel_parser import parse_excel
from pdf_parser import parse_pdf
from database import SessionLocal, create_tables
from models import Dokument
import sys


def speichere_in_db(ergebnis: dict, dateiname: str):
    db = SessionLocal()
    try:
        neuer_eintrag = Dokument(
            dateiname=dateiname,
            quelle=ergebnis["quelle"],
            daten_inhalt=ergebnis.get("daten")
        )
        db.add(neuer_eintrag)
        db.commit()
        print(f"[+] Gespeichert: {dateiname}")
    except Exception as e:
        print(f"[-] Fehler beim Speichern: {e}")
        db.rollback()
    finally:
        db.close()


def main():
    create_tables()

    if len(sys.argv) < 3:
        print("Benutzung: python main.py <excel|pdf> <dateipfad>")
        return

    modus = sys.argv[1]
    pfad = sys.argv[2]

    if modus == "excel":
        ergebnis = parse_excel(pfad)
    elif modus == "pdf":
        ergebnis = parse_pdf(pfad)
    else:
        print("Unbekannter Modus. Verwende 'excel' oder 'pdf'.")
        return

    if ergebnis["status"] == "erfolg":
        speichere_in_db(ergebnis, pfad)
        print(ergebnis)
    else:
        print(f"Fehler: {ergebnis['fehler']}")


if __name__ == "__main__":
    main()