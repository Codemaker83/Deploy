#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email import Encoders
from os.path import basename

def send_mail(info, files):
    msg = MIMEMultipart()
    msg["From"] = info['from']
    msg["To"] = ",".join(info['to'])
    msg["Subject"] = info['subject']
    msg.attach(MIMEText(info["message"]))
    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(fil.read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % basename(f))
            msg.attach(part)
    
    server = smtplib.SMTP(info['server'])
    server.starttls()
    server.login(info['from'], info['pswd'])
    problems = server.sendmail(info['from'], info['to'], msg.as_string())
    server.quit()

def mail_body():
    res = """
Hi,

The build you requested have finished, you can inspect the instance in
the following url:

http://bardock.vauxoo.com:8069

Attached to this mail you can find the log files genereted during the process.

Regards.

"""
    return res

def main():

    mail_info = {'from': 'coward@vauxoo.com',
                 'to': ['tulio@vauxoo.com'],
                 'pswd': 'c0w4Rdvazz4l',
                 'subject': 'Build complete - Vauxoo 8.0',
                 'server': "smtp.gmail.com:587"}
    body = mail_body()
    mail_info.update({'message': body})
    send_mail(mail_info, ["/tmp/build_logs.tar.bz2", "/tmp/branches-info.json"])

if __name__ == '__main__':
    main()
