# excel_parser.py

import pandas as pd
import json
import os


def parse_excel(file_path: str):
    try:
        if os.path.getsize(file_path) == 0:
            return {
                "status": "fehler",
                "quelle": "excel",
                "fehler": "Die Excel-Datei ist leer"
            }

        # Автоматически выбираем движок в зависимости от расширения
        if file_path.endswith('.xls'):
            df = pd.read_excel(file_path, engine='xlrd')
        else:
            df = pd.read_excel(file_path, engine='openpyxl')

        data = df.to_dict(orient="records")
        return {
            "status": "erfolg",
            "quelle": "excel",
            "zeilen": len(data),
            "daten": json.dumps(data, default=str)
        }
    except Exception as e:
        return {
            "status": "fehler",
            "quelle": "excel",
            "fehler": str(e)
        }