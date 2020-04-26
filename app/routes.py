from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from flask_babel import _, get_locale
from flask import g
import random
import re
import qrcode


from app import app, db, set_email, count_status
from app.models import Message, User

# Не нужные переменые
# first_name = ''
# last_name = ''
# email = ''
# username = ''
# password = ''
# secret_key = ''


# Главная страница ------------------------------------------
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# Страница - Добавить заметку --------------------------------------
@app.route('/add_note', methods=['GET'])
@login_required
def add_note():
    return render_template('note_add.html', messages=Message.query.all())


'''Страница - Добавить заметку, отправляеть запрос на эту страницу 
через action="/add_message" на эту страницу /add_message а эта страница обрабатывает запрос 
через request.form['']  ---------------------------------------------------------------------------------------'''
@app.route('/add_message', methods=['POST'])
@login_required
def add_message():
    text = request.form['text']
    end_date_time = request.form['end_date']
    start_date = datetime.now().strftime("%Y-%m-%d")

    if not text:
        flash(_("Text не заполнен"))
    elif not end_date_time:
        flash(_("Окончание работы не установлен"))
    else:
        new_note = Message(text=text,
                           start_date=start_date,
                           end_date=end_date_time,
                           status="В ожидании",
                           user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
    return redirect(url_for('add_note'))


# Страница - Заметкии ------------------------------------------------------

@app.route('/note_page', methods=['GET', 'POST'])
@login_required
def note_page():
    return render_template('note_page.html', messages=Message.query.all())


# Страница - Редактора ------------------------------------------------------
'''динамическая ссылка <int:note_id>  
Он нужен для того чтобы оредлить какою заметку мы хотим изменить'''

@app.route('/note/<int:note_id>', methods=['GET', 'POST'])
@login_required
def note_update(note_id):
    note = Message.query.filter_by(id=note_id).first_or_404()
    btn = request.form.get('btn')
    update_id = request.form.get('note_id')
    new_text = request.form.get('text_update')
    new_end_date = request.form.get('end_date_update')
    new_status = request.form.getlist('status_select')

    pattern = re.compile("[[']|[]]")
    res = pattern.split(str(new_status))

    if request.method == "POST":

        if btn =='remove':
            update_note_db = Message.query.filter_by(id=update_id).first()
            db.session.delete(update_note_db)
            db.session.commit()
            return redirect(url_for('note_page'))

        if btn == 'update':
            if not update_id:
                flash(_("ID не заполнен"))
            elif not new_text:
                flash(_("Текст не заполнен"))
            elif not new_end_date:
                flash(_("Окончание работы не установлен"))
            else:
                update_note_db = Message.query.filter_by(id=update_id).first()
                if update_note_db.user_id == current_user.id:
                    update_note_db.text = new_text
                    update_note_db.end_date = new_end_date
                    update_note_db.status = str(res[2])
                    db.session.commit()
                elif not update_note_db:
                    flash(_("Такой ID Нет "))
                else:
                    flash(_("Извените, на вашем заметке такой ID нет "))

    return render_template('update_note.html', id=note_id, note=note)


# Страница Профиль ---------------------------------------------------
@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def profil(username):
    user = User.query.filter_by(username=username).first_or_404()
    # notes = Message.query.all()


    # did = []
    # work = []
    # pending = []
    # not_done = []
    #
    # for note in notes:
    #     if note.status == "Сделан" and note.user_id == user.id:
    #         did.append(note.id)
    #
    #     if note.status == "Работаю" and note.user_id == user.id:
    #         work.append(note.id)
    #
    #     if note.status == "В Ожидании" and note.user_id == user.id:
    #         pending.append(note.id)
    #
    #     if note.status == "Не сделанные" and note.user_id == user.id:
    #         not_done.append(note.id)

    return render_template("_lenta.html", username=username, note=count_status)


# Страница Мои данные ----------------------------------------------
@app.route('/user/<username>/my_data', methods=['GET', 'POST'])
@login_required
def my_data_profil(username):
    user = User.query.filter_by(username=username).first_or_404()

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    user_status = request.form.get('status')

    if request.method == 'POST':
        if not first_name:
            flash(_("Напишите имю"))
        elif not last_name:
            flash(_("Напишите фамилию"))
        elif not email:
            flash(_("Напишите email"))
        else:
            update_user = User.query.filter_by(id=current_user.id).first_or_404()
            if not update_user:
                flash(_("Нет такого пользователя"))
            else:
                update_user.first_name = first_name
                update_user.last_name = last_name
                update_user.email = email
                update_user.status = user_status
                db.session.commit()

    return render_template('_my_data.html', username=username, user=user, note=count_status)


# Страница - Все заметки ---------------------------------------
@app.route('/user/<username>/all_notes', methods=['GET', 'POST'])
@login_required
def all_notes_profil(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('_all_notes.html', username=username, user=user,
                           messages=Message.query.all(), note=count_status)


# Страница - Сделанные -----------------------------------
@app.route('/user/<username>/did', methods=['GET', 'POST'])
@login_required
def profil_did(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('_did.html', username=username, user=user,
                           messages=Message.query.all(), note=count_status)


# Страница - Работаю -----------------------------------------------
@app.route('/user/<username>/work', methods=['GET', 'POST'])
@login_required
def profil_work(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('_work.html', username=username, user=user,
                           messages=Message.query.all(), note=count_status)


# Страница - В ожидании -------------------------------------------
@app.route('/user/<username>/pending', methods=['GET', 'POST'])
@login_required
def profil_pending(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('_pending.html', username=username, user=user,
                           messages=Message.query.all(), note=count_status)


# Страница - Не сделанные ---------------------
@app.route('/user/<username>/not_done', methods=['GET', 'POST'])
@login_required
def profil_not_done(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('_not_done.html', user_link=username, user=user,
                           messages=Message.query.all(), note=count_status)


# Страница Пользователи --------------------------
@app.route('/user/<username>/users', methods=['GET', 'POST'])
@login_required
def profil_users(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('_users.html', username=username, user=user,
                           users=User.query.all(), note=count_status)


@app.route('/profil/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template("__user.html", username=username, user=user)


# Страница Логина ----------------------------------------------------------
@app.route("/login", methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(username=login).first_or_404()

        if user and check_password_hash(user.password, password):
            login_user(user)

            next_page = request.args.get('next')
            if not next_page:
                return redirect('/')
            return redirect(next_page)

        else:
            flash(_('Неверный логин или пароль'))

    else:
        flash(_('Пожалуйста, заполните поля логин и пароль'))

    return render_template('login.html')

# Страница Регистрации -------------------------------------------------------------------
'''Тут использован метод Пост и request.form.get('Name_input') '''

@app.route("/register", methods=['GET', 'POST'])
def register():
    new_first_name = request.form.get('first_name')
    new_last_name = request.form.get('last_name')
    new_email = request.form.get('email')
    new_login = request.form.get('login')
    new_password = request.form.get('password')
    new_password2 = request.form.get('password2')

    def QR_CDE(frist_name, last_name, email, username):
        value = f'''
        Имя: {frist_name}
        Фамилия: {last_name}
        Email: {email}
        '''
        img = qrcode.make(value)
        img.save(f'app/static/img/QR-CODE/{username}.png')


    # Этот функция рандомна выбирает аватар для нового пользователя
    def avatar_fun():
        rand = random.randrange(1, 15)
        return f"http://kodypai.mcdir.ru/wp-content/uploads/2020/04/kodypai-avatar-{rand}.png"

    user = User.query.filter_by(username=new_login).first()

    if request.method == 'POST':

        if not (new_login or new_password or new_password2 or new_last_name or new_first_name or new_email):
            flash(_('Пожалуйста заполните все поля!'))

        elif user:
            flash(_("Такой логин уже есть"))

        elif new_password != new_password2:
            flash(_('Пароли не равны!'))

        else:
            QR_CDE(new_first_name, new_last_name, new_email, new_login)
            av = avatar_fun()
            hash_pwd = generate_password_hash(new_password)
            new_user = User(first_name=new_first_name, last_name=new_last_name, email=new_email,
                            username=new_login, password=hash_pwd, avatar=av, status="Привет, я тут новичок.")
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page')), set_email.get_email_adik(new_email, new_login, new_password)

    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# Страница - 404 -------------------------------------------
@app.route('/page_404', methods=['GET', 'POST'])
def page_404():
    return render_template("404.html")


# Вылавливает ошибку по response.status_code ----------------------
@app.after_request
def redirect_to_sign(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)

    elif response.status_code == 404:
        return redirect(url_for('page_404') + '?next=' + request.url)

    return response


@app.before_request
def before_request():
    g.locale = str(get_locale())