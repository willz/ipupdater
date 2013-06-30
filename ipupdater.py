import urllib2
import smtplib
from email.mime.text import MIMEText
import socket
import json
import os
import time

def internet_on():
    try:
        res = urllib2.urlopen('http://baidu.com')
        return True
    except urllib2.URLError as err:
        pass
    return False

def get_ip():
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    return ip

def is_ip_changed():
    js = json.load(open('./config.json'))
    ip_file = js['ip_file']
    if os.path.exists(ip_file):
        old_ip = open(ip_file).read()
        return old_ip != get_ip()
    # ip file not exists, create one
    f = open(ip_file, 'w')
    f.write(get_ip())
    f.close()
    return True

def send_mail(receiver, content):
    js = json.load(open('./config.json'))
    sender = js['sender']
    session = smtplib.SMTP(js['smtp_server'], port = js['smtp_port'])
    session.set_debuglevel(True)
    session.login(sender, js['passwd'])
    msg = MIMEText(content)
    msg['Subject'] = 'IP Update'
    msg['From'] = sender
    msg['To'] = receiver
    session.sendmail(sender, receiver, msg.as_string())
    session.quit()

def main():
    js = json.load(open('./config.json'))
    receiver = js['receiver']
    while True:
        if not internet_on():
            # for arch linux
            os.system('sudo systemctl restart dhcpd@eth0.service')
        elif is_ip_changed():
            # connected to Internet and ip changed
            send_mail(receiver, get_ip())
        time.sleep(60)

if __name__ == '__main__':
    main()
