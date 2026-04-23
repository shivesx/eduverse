import smtplib
from email.mime.text import MIMEText


EMAIL="shiveshpatel853@gmail.com"
PASSWORD="kidhweaakbgxkyoo"

def send_otp_email(to_email:str,otp:str):
    subject="Email Verification OTP"
    body=f"Your OTP is: {otp} This OTP is valid for 5 minutes."

    msg=MIMEText(body)
    msg['Subject']=subject
    msg['From']=EMAIL
    msg['To']=to_email

    with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
        server.login(EMAIL,PASSWORD)
        server.sendmail(EMAIL,to_email,msg.as_string())

