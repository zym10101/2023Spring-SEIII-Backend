import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.Env import SENDER_EMAIL, SENDER_PASSWD


def send_email(receiver_email, subject, message):
    # 创建一个MIMEMultipart对象
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # 添加邮件内容
    body = MIMEText(message, 'plain')
    msg.attach(body)

    try:
        # 连接到QQ邮箱的SMTP服务器
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        # 登录到您的发件人邮箱
        server.login(SENDER_EMAIL, SENDER_PASSWD)
        # 发送邮件
        server.send_message(msg)
        print("邮件发送成功！")
    except Exception as e:
        print("邮件发送失败:", str(e))
    finally:
        # 关闭连接
        server.quit()


def send_crawling_completed(receiver_email, repo_name, req_time):
    subject = '数据爬取完成通知'
    message_template = '您在{}请求的关于{}仓库的数据已成功爬取！请返回页面完成后续操作'
    message = message_template.format(req_time, repo_name)
    send_email(receiver_email, subject, message)


if __name__ == '__main__':
    send_crawling_completed('940900298@qq.com', 'apache/tomcat', '五百年以前')
