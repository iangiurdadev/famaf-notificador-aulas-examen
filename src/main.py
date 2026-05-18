from scraper import consultar_fechas_disponibles
from storage import cargar_estado, guardar_estado, cargar_interesados
from notifier import enviar_email
from dotenv import load_dotenv

import os
load_dotenv()

def main():

    CORREO_REMITENTE = os.getenv("CORREO_REMITENTE")
    CONTRASENA = os.getenv("CONTRASENA")

    fechas = consultar_fechas_disponibles()
    notificadas = cargar_estado()
    interesados = cargar_interesados()


    for fecha in fechas:

        dia = fecha["dia"]
        id_examen = fecha["id"]
        ruta_adjunto = fecha["ruta"]

        print(f"id_examen: {id_examen}")
        print(f"dia: {dia}")

        if id_examen in notificadas:
            continue

        destinatarios = interesados.get(dia, [])

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