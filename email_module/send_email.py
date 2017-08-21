from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

FROM_ADDR = 'anotherme@aliyun.com'
PASSWORD = 'a411867400'
SMTP_SERVER = 'smtp.aliyun.com'
SMTP_PORT = 25


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


class EmailSender(object):
    def __init__(self, head, to_addrs):
        self.msg = MIMEMultipart()
        self.msg['From'] = _format_addr(FROM_ADDR)
        self.msg['To'] = _format_addr(','.join(to_addrs))
        self.msg['Subject'] = Header(head, 'utf-8').encode()

    def attach_text(self, text):
        self.msg.attach(MIMEText(text, 'plain', 'utf-8'))

    def attach_png(self, path, name):
        with open(path, 'rb') as f:
            mime = MIMEBase('image', 'png', filename='test.png')
            mime.add_header('Content-Disposition', 'attachment', filename=name)
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            self.msg.attach(mime)

    def send_email(self):
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.set_debuglevel(1)
        server.login(FROM_ADDR, PASSWORD)
        server.sendmail(self.msg['From'], [self.msg['To']], self.msg.as_string())
        server.quit()


if __name__ == "__main__":
    em = EmailSender(u'png test 5 =  =', ['411867400@qq.com'])
    em.attach_text(u'= 3 =')
    em.attach_png('C:\\Users\\Administrator\\Desktop\\test.png', 'test.png')
    em.attach_png('C:\\Users\\Administrator\\Desktop\\test.png', 'test2.png')
    em.send_email()

# msg = MIMEText('', 'plain', 'utf-8')
# msg['From'] = _format_addr(from_addr)
# msg['To'] = _format_addr(to_addr)
# msg['Subject'] = Header(u'', 'utf-8').encode()
# server = smtplib.SMTP(smtp_server, 25)
# server.set_debuglevel(1)
# server.login(from_addr, password)#
# server.sendmail(from_addr, [to_addr], msg.as_string())
# server.quit()
