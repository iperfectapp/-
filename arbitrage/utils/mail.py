# Python 网易邮箱简单发送邮件
# -*- coding: utf-8 -*-


import smtplib  # 导入PyEmail
from email.mime.text import MIMEText


# 邮件构建

def send(subject, content):
    sender = "newton520@163.com"  # 发送方
    recver = "252489079@qq.com"  # 接收方
    password = "DPERENVSFRRXENRT"  # 邮箱密码
    message = MIMEText(content, "plain", "utf-8")
    # content 发送内容     "plain"文本格式   utf-8 编码格式

    message['Subject'] = subject  # 邮件标题
    message['To'] = recver  # 收件人
    message['From'] = sender  # 发件人

    smtp = smtplib.SMTP_SSL("smtp.163.com", 994)  # 实例化smtp服务器
    smtp.login(sender, password)  # 发件人登录

    # as_string 对 message 的消息进行了封装
    smtp.sendmail(sender, [recver], message.as_string())
    smtp.close()
    print("发送邮件成功！！")
