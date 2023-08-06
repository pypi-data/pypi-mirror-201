

import smtplib
from smtplib import SMTPAuthenticationError

"""
# 邮件对象（真正被发送的东西）使用MIMEMultipart来标示
这个邮件是多个部分组成的，然后attach各个部分。如果是附件，则add_header加入附件的声明。
"""
from email.mime.multipart import MIMEMultipart 
from email.header import Header                 # 邮件的头部（主题）
from email.mime.text import MIMEText            # 构建文本内容/或者文本附件
from email.mime.image import MIMEImage          # 导入图片库 发送本地图片邮件时用
from email.header import  make_header           # 处理中文附件名时使用
import os                                       # 循环读取文件路劲
import sys

class SnEmail():

    def __init__(self,server="",port=0) -> None:
        """
        新浪企业邮箱
        sever smtp.sina.net
        port  465
        """
        self.server     =   server
        self.port       =   port


        # 2、准备数据 
        # 1）创建邮件对象 MIMEMultipart（‘mixed’）类型；
        # MIMEMultipart(‘alternative’)；MIMEMultipart(‘related’)类型
    
        self.msg = MIMEMultipart() 

    def mail_login(self,user="",password=""):
        """登录邮箱"""

        self.emailCome = user       # 邮件的时间发送人（发邮件的时候调用）
        self.loginStatus = False    # 登录结果状态
        try:
            # 1、链接邮箱服务器(带 SSL 启用安全机制) # 端口号：465/25
            # 1.1 判断python版本
            vamax = sys.version_info.major   #  大版本号例如3.6.8  则表示3
            vsmin = sys.version_info.minor   #  小版本号例如3.6.8  则表示6

            if vamax == 3 and vsmin < 10:  #  python 版本号大于3

                self.con = smtplib.SMTP_SSL(self.server,self.port) 

            else:
                """ Python 3.10 及以上版本使用"""
                import ssl
                ctx = ssl.create_default_context()
                ctx.set_ciphers('DEFAULT')
                self.con = smtplib.SMTP_SSL(self.server,port=self.port, context = ctx)

            # 2、登录邮箱 # 链接对象.login(账号、密码)
            self.con.login(user,password) 
            self.loginStatus = True
            return '邮箱登录成功'
        except SMTPAuthenticationError as e:
            return '登录失败，请检查账户密码是否正确，或者尝试授权码登录%s'%repr(e)
        except Exception as error:
            return '邮箱登录遇到错误：%s'%repr(error)
       
    def mail_title(self,title='无主题邮件',encode='utf-8'):
        """设置邮件主题"""
        self.msg['Subject'] = Header(title,encode).encode() # 创建邮件标题 # Header(标题，编码方式)

    def mail_content(self,content="",ctype='plain',encode='utf-8'):
        """
        添加邮件内容
        content : 邮件内容
        ctype   : 邮件类型 plain 文本类型；html 为HTML类型；base64(二进制文件，也就是附件)
        encode  : 编码方式，默认 'utf-8'
        """
        text = MIMEText(content +'\n',ctype,encode) # 设置邮件正文（邮件需要发送的内容） # 普通文本： MIMEText(文字内容，文本类型，编码方式) # 文本类型 - plain(普通文字) ； html(超链接) ；base64(二进制文件，也就是附件)
        self.msg.attach(text)

    def mail_image(self,image_path=""):
        """将图片以内容形式添加到邮件正文"""
        image_data2 = open(image_path,'rb')         # 打开图片文件
        image2      = MIMEImage(image_data2.read()) # MIMEImage(图片二进制数据)
        image_data2.close()                         # 关闭打开的图片文件
        image2.add_header('Content-ID','<tupian2>')  # 定于图片ID 在html中使用  image2.add_header('Content-ID','<XXXXX>')
        self.msg.attach(image2)
        content = """<p><img src = 'cid:tupian2'>\n</p>"""
        html = MIMEText(content,ctype='html',encode='utf-8')
        self.msg.attach(html)

    def mail_file(self,files=[]):
        """ 添加邮件附件（中英文文件名都支持），传入参数 files 必须是列表  """
        if len(files) != 0:  # 循环读取文件列表
            for i in range(len(files)):
                if os.path.isfile(files[i]):
                    file_open = open(files[i],'rb')
                    file_content = file_open.read()
                    file_open.close()
                    file1 = MIMEText(file_content,'base64','utf-8')
                    fileName = os.path.basename(files[i]) # 文件名称

                    # 声明这个是个二进制文件，菜鸟教程中有这段代码,也可以不加
                    file1["Content-Type"]        = 'application/octet-stream;name="%s"'% make_header([(fileName,'UTF-8')]).encode('UTF-8') 

                    # 设置附件名，中英文文件名都能支持
                    file1["Content-Disposition"] = 'attachment;filename= "%s"' % make_header([(fileName, 'UTF-8')]).encode('UTF-8')

                    # 添加附件
                    self.msg.attach(file1)    

    def mail_send(self,emailTo=[],emailCC=[],emailNoSend=[],emailComeShow =""):
        """
        发送邮件
        emailTo       收件人列表
        emailCC       抄送人列表
        emailNoSend   不发送的对象（会显示，实际不发送）
        emailComeShow 显示的发件人（和实际发件人可能不是同一个）
        """

        if emailComeShow == "":
            self.msg['From']    = self.emailCome            # 设置邮件显示的发送人
        else:
            self.msg['From']    = emailComeShow 

        self.msg['To']      = ";".join(emailTo)    # 显示的收件人 # ’收件人1；收件人2；收件人3....‘
        self.msg['cc']      = ";".join(emailCC)    # 显示的抄送人 用; 分割
        emailToTure = ";".join(set(emailTo + emailCC ) - set(emailNoSend))  # 实际发送的邮件列表

        # 发送邮件
        try:
            if self.loginStatus:
                self.con.sendmail(self.emailCome,emailToTure,self.msg.as_string())
                self.con.quit()
                return "发送邮件已完成"
            return "跳过邮件发送(未识别登录状态)"
        except Exception as error:
            return "发送邮件遇到错误：%s" %repr(error)



if __name__ == '__main__':
    server  = 'smtp.sina.net'
    port    = 465
    sn = SnEmail(server,port)
    
    # 设置邮件主题
    sn.mail_title(title="测试邮件")

    # 设置邮件内容
    sn.mail_content("这是测试内容")
    
    # 设置附件
    sn.mail_file([r"C:\Users\manji\Downloads\全量商品列表.xlsx"])

    # 登录邮箱
    print(sn.mail_login(user="",password=""))

    # 发送邮件
    print(sn.mail_send(emailTo=['']))