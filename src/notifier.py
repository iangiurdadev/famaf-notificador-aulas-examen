import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
from email.message import EmailMessage

from scraper import consultar_fechas_disponibles

load_dotenv()

def enviar_email(remitente, contrasena,
                 destinatarios, asunto,
                 contenido, ruta_archivo):

    mensaje = EmailMessage()

    mensaje["From"] = remitente
    mensaje["To"] = ", ".join(destinatarios)
    mensaje["Subject"] = asunto

    mensaje.set_content(contenido)

    with open(ruta_archivo, "rb") as f:
        datos = f.read()

    mensaje.add_attachment(
        datos,
        maintype="image",
        subtype="png",
        filename="aula.png"
    )

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()

        server.login(remitente, contrasena)

        server.send_message(mensaje)

        server.quit()

        print(f"Enviando a {len(destinatarios)} destinatarios")

    except Exception as e:
        print(f"Error al enviar correo: {e}")


if __name__ == "__main__":

    CORREO_REMITENTE = os.getenv("CORREO_REMITENTE")
    CONTRASENA = os.getenv("CONTRASENA")
    CORREO_DESTINATARIO = os.getenv("CORREO_DESTINATARIO")


    resultados_fechas = consultar_fechas_disponibles() 
    if resultados_fechas:

        #Como prueba, mandamos el primero
        dia = resultados_fechas[0]["dia"]
        ruta_adjunto = resultados_fechas[0]["ruta"]

        enviar_email(CORREO_REMITENTE,
                     CONTRASENA,
                     CORREO_DESTINATARIO,
                     f"Aulas Examen {dia}",
                     "Adjunto la imagen de las aulas :D",
                     ruta_adjunto)