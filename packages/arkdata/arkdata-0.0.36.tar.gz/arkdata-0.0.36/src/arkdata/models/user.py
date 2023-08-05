from sqlalchemy import Column, String
from arkdata.database.cursor import sqlalchemy
from arkdata.database.table import Table
from pathlib import Path
import os
import arkdata
from arkdata import models
from secrets import token_urlsafe
import bcrypt


class User(sqlalchemy.db.Model, Table):
    xuid = Column(String(100), nullable=False, unique=True)
    gamertag = Column(String(100))
    password_digest = Column(String(100))

    def __init__(self, xuid=None, gamertag=None, password_digest=None):
        self.xuid = xuid
        self.gamertag = gamertag
        self.password_digest = password_digest

    @classmethod
    def create_user(cls, gamertag=None, password=None):
        xuid = token_urlsafe()
        password_digest = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = cls(xuid=xuid, gamertag=gamertag, password_digest=password_digest)
        user.commit_initialization()
        session = models.Session(xuid=xuid)
        session.commit_initialization()
        session.new_session_token()
        return user

    @classmethod
    def seed_table(cls):
        dir = Path(os.path.dirname(arkdata.__file__))
        path = dir / Path('seeds/users.json')
        super()._seed_table(path)

    def session(self):
        return models.Session.find_by(xuid=self.xuid)

    def account(self):
        return models.Account.find_by(xuid=self.xuid)

    def cart_items(self):
        return models.CartItem.find_all_by(xuid=self.xuid)

    def orders(self):
        return models.OrderItem.find_all_by(xuid=self.xuid)

