import smtplib
from email.message import EmailMessage

def send_email(receiver_email, zip_path):

    sender_email = "yourgmail@gmail.com"
    sender_password = "your_app_password"

    msg = EmailMessage()
    msg["Subject"] = "Your Mashup File"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content("Your mashup file is attached.")

    with open(zip_path, "rb") as f:
        file_data = f.read()

    msg.add_attachment(file_data,
                       maintype="application",
                       subtype="zip",
                       filename="mashup.zip")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)
