import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_email_adik(user_email, username, password):

    fromaddr = "wayupkg01@gmail.com"
    toaddr = user_email
    mypass = "327844Wap"

    body = f'''Вы или кто то другой зарегистрировались на сайте "Коди Руй" со следующими данными: 

Логин: {username}

Пароль: {password}

------------------------------------------------------------------------
Это сообщение было сформировано автоматически, не надо отвечать на него.
"Коди Куй" '''

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Коди Руй"

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, mypass)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def get_email_note(user_email, first_name, last_name, theme, start_data, end_date):

    fromaddr = "wayupkg01@gmail.com"
    toaddr = user_email
    mypass = "327844Wap"

    body = f'''Здравствуйте  {str(first_name)} {str(last_name)}: 

Истекает срок вашей заметки с названием - {theme}

Заметка был создан - {start_data} до {end_date}

Сайт: http://127.0.0.1:5000/note_page
-----------------------------------------------------
Это сообщение было сформировано автоматически, не надо отвечать на него.
"Коди Куй" 
           '''

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Коди Руй"


    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, mypass)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


# def key_email():
#     chars = '1234567890'
#     key_regis =''
#
#     for i in range(6):
#         key_regis += random.choice(chars)
#
#     return int(key_regis)


