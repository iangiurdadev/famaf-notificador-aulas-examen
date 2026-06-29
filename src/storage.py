import json
import os

FECHAS_NOTIFICADAS = "notificadas.json"


def cargar_estado():
    if not os.path.exists(FECHAS_NOTIFICADAS):
        print(f"no existe el archivo {FECHAS_NOTIFICADAS}")
        return set()

    with open(FECHAS_NOTIFICADAS, "r", encoding="utf-8") as archivo:
        return set(json.load(archivo))

def guardar_estado(notificados):
    with open(FECHAS_NOTIFICADAS, "w", encoding="utf-8") as archivo:
        json.dump(list(notificados), archivo)

def cargar_interesados():
    return {
        "lunes": [
            "iangiurda.dev@gmail.com"
        ]
    }