from fastapi_mail import FastMail, MessageSchema
from pydantic import EmailStr
from config.mailConfig import connection_mail

async def enviar_correo(destinatario: EmailStr, asunto: str, contenido: str):

    mensaje = MessageSchema(
        subject=asunto,
        recipients=[destinatario],
        body=contenido,
        subtype="html"
    )

    aux = FastMail(connection_mail)
    await aux.send_message(mensaje)
