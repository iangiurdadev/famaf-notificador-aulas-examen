import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
NOTIFICADAS_PATH = BASE_DIR / "state" / "notificadas.json"


def cargar_estado():
    if not NOTIFICADAS_PATH.exists():
        print(f"No existe el archivo {NOTIFICADAS_PATH}")
        return set()

    with NOTIFICADAS_PATH.open("r", encoding="utf-8") as archivo:
        return set(json.load(archivo))

def guardar_estado(notificados):
    with NOTIFICADAS_PATH.open("w", encoding="utf-8") as archivo:
        json.dump(list(notificados), archivo)

def cargar_interesados():
    return {
        "29-06-2026": [
            "iangiurda.dev@gmail.com"
        ]
    }