import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage

from scraper import consultar_fechas_disponibles

load_dotenv()

def enviar_email(remitente, contrasena,
                 destinatarios, asunto,
                 contenido, ruta_archivo):

    mensaje = EmailMessage()

    mensaje["From"] = remitente
    mensaje["To"] = remitente
    mensaje["Bcc"] = ", ".join(destinatarios)
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
