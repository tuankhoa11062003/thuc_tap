import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

sender = "you@gmail.com"
receiver = "someone@example.com"
password = "your_app_password"

msg = MIMEMultipart()
msg["From"] = sender
msg["To"] = receiver
msg["Subject"] = "Báo cáo tự động"

# Nội dung email
msg.attach(MIMEText("Đây là email tự động", "plain"))

# Đính kèm file
with open("baocao.pdf", "rb") as f:
    file = MIMEApplication(f.read(), name="baocao.pdf")
    msg.attach(file)

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender, password)
    server.send_message(msg)
