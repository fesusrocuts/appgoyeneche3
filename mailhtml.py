import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def sendmailhtml(sender_email, receiver_email, Subject, text, html):

    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "{}".format(Subject)
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Create the plain-text and HTML version of your message
    text = """\
    {}""".format(text)
    html = """\
    {}
    """.format(html)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("mail.s415.sureserver.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )


"""
sender_email = "contabilidad@comercializadoragyl.com"
receiver_email = "contabilidad@comercializadoragyl.com"
password = input("Type your password and press enter:")
sendmailhtml(sender_email, receiver_email, 'Test html', 'Hi, The next message you see correctly with html format','<html><body><TABLE BORDER="1" style="width:100%;"><TR><TH>FECHA</TH><TH>VENCE</TH><TH>CMP</TH><TH>DOC No</TH><TH>SIN VENCER</TH><TH>1-30 DIAS</TH><TH>31-60 DIAS</TH><TH>61-90 DIAS</TH><TH>91-120 DIAS</TH><TH>+ DE 120 DIAS</TH><TH>TOTAL</TH></TR><TR><TD>26 JUL. 2019</TD><TD>24 SEP. 2019</TD><TD>FC</TD><TD>0000028246</TD><TD></TD><TD></TD><TD></TD><TD>881314.0</TD><TD></TD><TD></TD><TD>881314.0</TD></TR><TR><TD>01 AGO. 2019</TD><TD>30 SEP. 2019</TD><TD>FC</TD><TD>0000028376</TD><TD></TD><TD></TD><TD>27370.0</TD><TD></TD><TD></TD><TD></TD><TD>27370.0</TD></TR></TABLE></body></html>')
"""
sender_email = "contabilidad@comercializadoragyl.com"
receiver_email = "contabilidad@comercializadoragyl.com"
password = "3175141592"#input("Type your password and press enter:")
#sendmailhtml(sender_email, receiver_email, 'Test html', 'Hi, The next message you see correctly with html format','<html><body><TABLE BORDER="1" style="width:100%;"><TR><TH>FECHA</TH><TH>VENCE</TH><TH>CMP</TH><TH>DOC No</TH><TH>SIN VENCER</TH><TH>1-30 DIAS</TH><TH>31-60 DIAS</TH><TH>61-90 DIAS</TH><TH>91-120 DIAS</TH><TH>+ DE 120 DIAS</TH><TH>TOTAL</TH></TR><TR><TD>26 JUL. 2019</TD><TD>24 SEP. 2019</TD><TD>FC</TD><TD>0000028246</TD><TD></TD><TD></TD><TD></TD><TD>881314.0</TD><TD></TD><TD></TD><TD>881314.0</TD></TR><TR><TD>01 AGO. 2019</TD><TD>30 SEP. 2019</TD><TD>FC</TD><TD>0000028376</TD><TD></TD><TD></TD><TD>27370.0</TD><TD></TD><TD></TD><TD></TD><TD>27370.0</TD></TR></TABLE></body></html>')
