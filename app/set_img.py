from PIL import Image, ImageFont, ImageDraw


def certificate(username_fille, first_name, last_name, date):

    img = Image.open('app/static/img/certificate/base-cer.jpg')
    idrew = ImageDraw.Draw(img)

    font_username = ImageFont.truetype('app/static/Font/BOOKOS.TTF', size=35)
    font_text = ImageFont.truetype('app/static/Font/BOOKOS.TTF', size=20)
    font_date = ImageFont.truetype('app/static/Font/BOOKOS.TTF', size=18)

    username = f"{first_name} {last_name}"

    text = '''Выбери профессию, которую ты любишь,
— и тебе не придется работать ни дня 
в твоей жизни.'''

    date = date

    idrew.text((90, 260), username, font=font_username, fill='#1E3440')

    idrew.text((90, 320), text, font=font_text, fill='#088C75')

    idrew.text((110, 473), date, font=font_date, fill='#088C75')

    idrew.text((130, 503), "Дата", font=font_date, fill='#088C75')
    #
    # idrew.text((110, 473), date, font=font_date, fill='#009EAA')
    # idrew.text((110, 473), date, font=font_date, fill='#009EAA')


    img.save(f'app/static/img/{username_fille}3.png')