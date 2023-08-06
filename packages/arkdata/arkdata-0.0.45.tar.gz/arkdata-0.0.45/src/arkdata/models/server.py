from arkdata.database.cursor import sqlalchemy
from arkdata.database.table import Table
from sqlalchemy import Column, String, Integer


class Server(sqlalchemy.db.Model, Table):

    name = Column(String(100), unique=False, nullable=False, default="UNKNOWN")
    xuid = Column(String(100), unique=True, nullable=True, default=None)
    player_id = Column(String(100), unique=False, nullable=True, default=None)
    nitrado_id = Column(String(100), unique=False, nullable=True, default=None)
    map = Column(String(100), unique=False, nullable=True, default=None)
    address = Column(String(100), unique=False, nullable=False)

    def users(self):
        # Gets all users in this server
        pass

    def commands(self):
        # Gets all commands from this server
        pass

