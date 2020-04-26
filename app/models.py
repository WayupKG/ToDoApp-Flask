from flask_login import UserMixin
from datetime import datetime

from app import db, manager, set_email


# Создание базы данных для заметок -------------------------------
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1024), nullable=False)
    start_date = db.Column(db.String(12))
    end_date = db.Column(db.String(12))
    status = db.Column(db.String(24))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    date = datetime.now().strftime("%Y-%m-%d")

    # функция для определения статуса заметки -------------------------------
    def date_now(self, note_id, user_id):
        self.id = note_id
        self.user_id = user_id
        self.note = Message.query.filter_by(id=self.id).first()
        self.user = User.query.filter_by(id=self.user_id).first()

        if self.note.end_date == self.date:
            return "Равно"

        elif self.note.end_date < self.date and self.note.status == "В ожидании":
            self.note.status = 'Не сделан'
            db.session.commit()

            # Если статус в ожидании и срок истек то отпровляет пользователю по майлу эту заметку
            set_email.get_email_note(self.user.email,
                                     self.user.first_name,
                                     self.user.last_name,
                                     self.note.text,
                                     self.note.start_date,
                                     self.note.end_date,)
            return "Меньше"

        elif self.note.end_date > self.date:
            return "Больше"


# Создание базы данных для пользователей ------------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    status = db.Column(db.String(240))
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    avatar = db.Column(db.String(80))
    my_note = db.relationship('Message', backref='author', lazy='dynamic')


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
