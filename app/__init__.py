from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdfgfdgdfhfdsdsvvsdgddfh'  # Ключ
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mynote.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
manager = LoginManager(app)
db = SQLAlchemy(app)
babel = Babel(app)
migrate = Migrate(app, db)


@babel.localeselector
def get_locale():
    # return request.accept_languages.best_match(app.config['LANGUAGES'])
    return 'en'


from app import models, routes

db.create_all()
