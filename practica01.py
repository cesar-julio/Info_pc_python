import credenciales
import main

import smtplib, ssl

msg = str(main.mostrarInfo())
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = credenciales.email # Enter your address
receiver_email = credenciales.email # Enter receiver address
password = credenciales.passw
message = f"""\
Subject: Hi there

This message is sent from Python.{msg}"""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)