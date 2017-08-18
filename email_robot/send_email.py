from email.mime.text import MIMEText
import smtplib

from_addr = "anotherme@aliyun.com"
password = "a411867400"
to_addr = "411867400@qq.com"
smtp_server = "smtp.aliyun.com"
msg = MIMEText('测试邮件内容', 'plain', 'utf-8')
server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()

