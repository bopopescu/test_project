# coding:utf-8
import os
import smtplib
import time
import unittest
from HTMLTestRunner import HTMLTestRunner

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from data import test_data
from config import read_email_config

# 当前脚本所在真实地址
cur_path = os.path.dirname(os.path.realpath(__file__))


def add_case(caseName="case", rule="test_*.py"):
    """加载所有case目录下开头为test的测试用例"""
    case_path = os.path.join(cur_path, caseName)
    if not os.path.exists(case_path): os.mkdir(case_path)

    # 加载所有测试用例
    discover = unittest.defaultTestLoader.discover(case_path, pattern=rule, top_level_dir=None)
    return discover


def run_case(all_case, report_name="report"):
    now = time.strftime("%Y_%m_%d_%H_%M_%S")
    report_path = os.path.join(cur_path, report_name)
    if not os.path.exists(report_path): os.mkdir(report_path)
    report_abspath = os.path.join(report_path, now + "result.html")
    print("report path %s" % report_abspath)

    fp = open(report_abspath, "wb")
    runner = HTMLTestRunner(stream=fp, title="自动化接口测试报告，测试结果如下：", description="用例执行情况")

    runner.run(all_case)
    fp.close()


def get_report_file(report_path):
    """获取最新的测试报告"""
    lists = os.listdir(report_path)
    lists.sort(key=lambda fn: os.path.getmtime(os.path.join(report_path, fn)))
    print("最新报告：" + lists[-1])
    report_file = os.path.join(report_path, lists[-1])
    return report_file


def send_email(report_file, sender, psw, receiver, smtpserver, port):
    with open(report_file, "rb") as f:
        mail_body = f.read()
    # 使用email构造邮件
    msg = MIMEMultipart()
    body = MIMEText(mail_body, _subtype="html", _charset="utf-8")
    msg["Subject"] = "自动化测试报告"
    msg["from"] = sender
    msg["to"] = receiver
    msg.attach(body)

    # 添加附件
    att = MIMEText(open(report_file, "rb").read(), "base64", "utf-8")
    att["Content-type"] = "application/octet-stream"
    att["Content-Disposition"] = "attachment;filename = 'report.html'"
    msg.attach(att)

    try:
        smtp = smtplib.SMTP_SSL(smtpserver, port)
    except:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver, port)

    smtp.login(sender, psw)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    print("邮件发送成功！")


if __name__ == "__main__":
    test_data.init_data()
    all_case = add_case()
    run_case(all_case)
    report_file = get_report_file(os.path.join(cur_path, "report"))

    # 邮件配置
    sender = read_email_config.sender
    receiver = read_email_config.receiver
    psw = read_email_config.psw
    smtp_server = read_email_config.smtp_server
    port = read_email_config.port
    send_email(report_file, sender, psw, receiver, smtp_server, port)
