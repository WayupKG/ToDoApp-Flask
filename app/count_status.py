from app.models import Message, User
from app import set_img
from datetime import datetime


def did(message, user_id):
    notes = Message.query.all()
    user = User.query.filter_by(id=user_id).first_or_404()

    date = datetime.now().strftime("%Y-%m-%d")

    count_status = []

    for note in notes:
        if note.status == message and note.user_id == user_id:
            count_status.append(note.id)

        if message == "Сделан":
            len_ = len(count_status)
            if len_ >= 3:
                set_img.certificate(user.username, user.first_name, user.last_name, date)
    return len(count_status)
