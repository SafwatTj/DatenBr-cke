# pdf_parser.py

import PyPDF2
import json

def parse_pdf(file_path: str):
    try:
        text = ""
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
        return {
            "status": "erfolg",
            "quelle": "pdf",
            "seiten": len(reader.pages),
            "daten": json.dumps({"text": text[:5000]}, default=str)
        }
    except Exception as e:
        return {
            "status": "fehler",
            "quelle": "pdf",
            "fehler": str(e)
        }