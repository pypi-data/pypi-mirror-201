from sqlalchemy import Column, String, Boolean
from arkdata.database.cursor import sqlalchemy
from arkdata.database.table import Table
from secrets import token_urlsafe
import bcrypt
from arkdata import models


class Session(sqlalchemy.db.Model, Table):
    xuid = Column(String(100), nullable=False, unique=True)
    session_token = Column(String(100), default=None)
    security_token = Column(String(100), default=None)
    authenticated = Column(Boolean, default=False)

    def __init__(self, xuid=None, session_token=None, security_token=None, authenticated=False):
        self.xuid = xuid
        self.session_token = session_token
        self.security_token = security_token
        self.authenticated = authenticated

    @classmethod
    def login(cls, gamertag: str, password: str) -> 'User' or None:
        user = models.User.find_by(gamertag=gamertag)
        if user is None:
            return
        is_password_valid = bcrypt.checkpw(password.encode(), user.password_digest.encode())
        if not is_password_valid:
            return
        session = Session.find_by(xuid=user.xuid)
        session.new_session_token()
        return user

    @classmethod
    def authenticate_security_token(cls, security_token: str) -> 'User' or None:
        session = Session.find_by(security_token=security_token)
        if session is not None:
            session.new_security_token()
            return models.User.find_by(xuid=session.xuid)

    def logout(self) -> None:
        self.session_token = token_urlsafe(64)
        self.commit()

    def new_security_token(self):
        self.security_token = token_urlsafe(64)
        self.commit()
        # TODO: Send token to xbox account

