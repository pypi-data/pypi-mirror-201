from arkdata.database.cursor import sqlalchemy
from arkdata.database.table import Table
from sqlalchemy import Column, String, Integer
from pathlib import Path
import os
import arkdata
from secrets import token_urlsafe


class Account(sqlalchemy.db.Model, Table):
    xuid = Column(String(100), nullable=False, unique=True)
    player_name = Column(String(100), nullable=True, default=None)
    ark_player_id = Column(Integer, nullable=True, default=None)
    berry_bush_seeds = Column(Integer, nullable=False, default=0)
    api_token = Column(String(100), nullable=True, default=token_urlsafe)

    def __init__(self, xuid=None, player_name=None, ark_player_id=None, berry_bush_seeds=0, api_token=None):
        self.xuid = xuid
        self.player_name = player_name
        self.ark_player_id = ark_player_id
        self.berry_bush_seeds = berry_bush_seeds
        self.api_token = api_token

    @classmethod
    def seed_table(cls):
        directory = Path(os.path.dirname(arkdata.__file__))
        path = directory / Path('seeds/accounts.json')
        super()._seed_table(path)

    def generate_api_token(self):
        self.api_token = token_urlsafe()

