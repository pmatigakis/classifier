from uuid import uuid4
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="pk_users"),
        db.UniqueConstraint("username", name="uq_users_username"),
    )

    USERNAME_SIZE = 20
    JTI_SIZE = 32

    id = db.Column(db.Integer, db.Sequence("users_id_seq"), nullable=False)
    username = db.Column(db.String(USERNAME_SIZE), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    jti = db.Column(db.String(JTI_SIZE), nullable=False)
    registered_at = db.Column(db.DateTime, nullable=False)

    @classmethod
    def create(cls, username, password):
        user = cls(
            username=username,
            password=generate_password_hash(password),
            jti=uuid4().hex,
            registered_at=datetime.now()
        )

        db.session.add(user)

        return user

    @classmethod
    def get_by_id(cls, user_id):
        return db.session.query(cls).get(user_id)

    @classmethod
    def get_by_username(cls, username):
        return db.session.query(cls).filter_by(username=username).one_or_none()

    @classmethod
    def authenticate_using_jti(cls, user_id, jti):
        return db.session.query(User) \
                         .filter_by(id=user_id, jti=jti) \
                         .one_or_none()

    @classmethod
    def authenticate(cls, username, password):
        user = cls.get_by_username(username)

        if user is not None and check_password_hash(user.password, password):
            return user

        return None

    def change_password(self, password):
        self.password = generate_password_hash(password)
        self.jti = uuid4().hex

    def delete(self):
        db.session.delete(self)
