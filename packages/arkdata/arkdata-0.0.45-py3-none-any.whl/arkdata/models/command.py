from arkdata.database.cursor import sqlalchemy
from arkdata.database.table import Table
from sqlalchemy import Column, String, Integer, Boolean


class Command(sqlalchemy.db.Model, Table):

    xuid = Column(String(100), unique=False, nullable=True)
    operation = Column(String(100), unique=False, nullable=False, default="OTHER")
    operation_id = Column(Integer, unique=False, nullable=True, default=None)
    code = Column(String(100), unique=False, nullable=False)
    executed = Column(Boolean, unique=False, nullable=False, default=False)

    # Admin's player id
    player_id = Column(String(100), unique=False, nullable=True, default=None)
    # Game Server IP Address or URL
    address = Column(String(100), unique=False, nullable=True, default=None)
    # Server id
    server_id = Column(Integer, unique=False, nullable=True, default=None)

    def __init__(
            self,
            xuid=None,
            operation=None,
            operation_id=None,
            code=None,
            executed=None,
            player_id=None,
            address=None,
            server_id=None
    ):
        self.xuid = xuid
        self.operation = operation
        self.operation_id = operation_id
        self.code = code
        self.executed = executed
        self.player_id = player_id
        self.address = address
        self.server_id = server_id

    @classmethod
    def execute_all(cls):
        pass

    @classmethod
    def executes(cls, **where):
        pass

    def server(self):
        pass

    def execute(self):
        pass

    def product(self):
        pass

    def user(self):
        pass

