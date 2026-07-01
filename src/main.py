from scraper import consultar_fechas_disponibles
from storage import cargar_estado, guardar_estado
from notifier import enviar_email
from google_sheets_actions import GoogleSheets
from dotenv import load_dotenv

from pathlib import Path
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
CREDENTIALS = BASE_DIR / "credentials" / "service_account.json"


def main():

    CORREO_REMITENTE = os.getenv("CORREO_REMITENTE")
    CONTRASENA = os.getenv("CONTRASENA")

    fechas = consultar_fechas_disponibles()
    notificadas = cargar_estado()

    gs = GoogleSheets(
        str(CREDENTIALS),
        "Formulario Prueba (Respuestas)",
        "Hoja 1"
    )

    interesados = gs.obtener_interesados()


    for fecha in fechas:

        dia = fecha["dia"]
        id_examen = fecha["id"]
        ruta_adjunto = fecha["ruta"]

        print(f"id_examen: {id_examen}")
        print(f"dia: {dia}")

        if id_examen in notificadas:
            continue

        destinatarios = interesados.get(id_examen, [])
        print(interesados)
        print(f"Destinararios para {id_examen}")
        print(destinatarios)

        if not destinatarios:
            continue

        enviar_email(CORREO_REMITENTE,
                    CONTRASENA,
                    destinatarios,
                    f"Aulas Examen {id_examen}",
                    "Adjunto la imagen de las aulas :D",
                    ruta_adjunto)

        notificadas.add(id_examen)

    guardar_estado(notificadas)

if __name__ == "__main__":
    main()