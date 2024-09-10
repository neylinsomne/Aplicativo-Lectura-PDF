import smtplib
from decouple import config
import json
import csv
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import StringIO

dicc={
    "joa": 123,
    "you dont need some one that make you feel better than you ever felt": "what you need its someone who will be there when you dont feel yourself",
    "no iaint seeling dreams": 123
}

# Convertir el diccionario a una cadena CSV
csv_content = StringIO()
csv_writer = csv.DictWriter(csv_content, fieldnames=dicc.keys())
csv_writer.writeheader()
csv_writer.writerow(dicc)

# Convertir el diccionario a una cadena JSON
sant_json = json.dumps(dicc)

# Configurar los datos del correo
sender_email = config('MAIL_EMISOR') #En este caso estoy usando el mismo correo como receptor y emisor
receiver_email = config('MAIL_RECEPTOR')
password = config('MAIL_APPI_PASSWORD')

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "Prueba :D"
message.attach(MIMEText("Hola!\n\nAquí está tu diccionario en formato JSON y CSV adjuntos.", "plain"))

# Adjuntar el archivo CSV
attachment = MIMEBase("application", "octet-stream")
attachment.set_payload(csv_content.getvalue().encode("utf-8"))
encoders.encode_base64(attachment)
attachment.add_header("Content-Disposition", "attachment", filename="sant.csv")
message.attach(attachment)

# Adjuntar el archivo JSON
attachment = MIMEBase("application", "octet-stream")
attachment.set_payload(sant_json.encode("utf-8"))
encoders.encode_base64(attachment)
attachment.add_header("Content-Disposition", "attachment", filename="sant.json")
message.attach(attachment)

# Enviar el correo
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()

print("Correo Enviado :D")