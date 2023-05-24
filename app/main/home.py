from flask import render_template
from extensions import db
from app.models.conversations import Conversations
from app.models.chats import Chats

from . import bp


@bp.route("/")
def index():
    conversations = [c.to_json() for c in db.session.query(Conversations).all()]
    chats = [c.to_json() for c in db.session.query(Chats).all()]

    # print(conversations)
    # print(chats)

    conversation = db.session.query(Conversations).first()
    print(conversation.chat.title, conversation.chat.id)

    chat = db.session.query(Chats).first()
    print(chat.to_json())

    # for i in chat.conversations:
    #     print(i.to_json())

    return render_template("index.html", conversations=conversations, chats=chats)
