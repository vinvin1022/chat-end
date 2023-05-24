from datetime import datetime
from extensions import db


class Conversations(db.Model):
    __tablename__ = "conversations"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    cid = db.Column(db.String)
    role = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    parent = db.Column(db.String, nullable=False)
    children = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    chatid = db.Column(db.Integer, db.ForeignKey("chats.id"))
    chat = db.relationship("Chats", backref=db.backref("conversations", lazy=True))

    def __repr__(self):
        return "<Conversations %s>" % self.id

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


@db.event.listens_for(Conversations, "before_insert")
def set_created_at(mapper, connection, target):
    target.created_at = datetime.now()


@db.event.listens_for(Conversations, "before_update")
def set_updated_at(mapper, connection, target):
    target.updated_at = datetime.now()
