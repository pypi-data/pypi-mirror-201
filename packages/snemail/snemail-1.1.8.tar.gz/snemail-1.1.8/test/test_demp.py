from snemail import SnEmail

if __name__ == '__main__':
    server  = 'smtp.sina.net'
    port    = 465
    sn = SnEmail(server,port)
    
    # 设置邮件主题
    sn.mail_title(title="测试邮件")

    # 设置邮件内容
    sn.mail_content("这是测试内容")
    
    # 邮件正文图片
    sn.mail_image(image_path="")

    # 设置附件
    sn.mail_file([r"C:\Users\manji\Downloads\全量商品列表.xlsx"])

    # 登录邮箱
    print(sn.login(user="",password=""))

    # 发送邮件
    print(sn.mail_send(emailTo=['']))