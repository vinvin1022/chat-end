from datetime import datetime
from extensions import db


class Chats(db.Model):
    __tablename__ = "chats"
    id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String, nullable=False)
    parent = db.Column(db.String, nullable=False)
    children = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return "<Chats %r>" % self.id

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


@db.event.listens_for(Chats, "before_insert")
def set_created_at(mapper, connection, target):
    target.created_at = datetime.now()


@db.event.listens_for(Chats, "before_update")
def set_updated_at(mapper, connection, target):
    target.updated_at = datetime.now()
