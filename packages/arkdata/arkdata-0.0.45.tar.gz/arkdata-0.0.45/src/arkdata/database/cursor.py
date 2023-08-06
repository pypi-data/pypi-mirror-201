from flask import Flask
from flask.ctx import AppContext
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database, drop_database
from arkdata.database.configuration import DATABASE_URI, TEST_DATABASE_URI
from sqlalchemy.engine.reflection import Inspector
from enum import Enum


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

test_app = Flask(__name__)
test_app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI
test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class DatabaseType(Enum):
    production_database = DATABASE_URI
    test_database = TEST_DATABASE_URI


class Database:
    def __init__(self):
        self.database_type = DatabaseType.production_database
        self.production_app: Flask = app
        self.production_db: SQLAlchemy = SQLAlchemy(app)
        self.test_app: Flask = test_app
        self.test_db: SQLAlchemy = SQLAlchemy(test_app)


    @property
    def app(self) -> Flask:
        if self.database_type == DatabaseType.production_database:
            return self.production_app
        else:
            return self.test_app

    @property
    def db(self) -> SQLAlchemy:
        if self.database_type == DatabaseType.production_database:
            if not database_exists(DATABASE_URI):
                create_database(DATABASE_URI)
            return self.production_db
        elif self.database_type == DatabaseType.test_database:
            if not database_exists(TEST_DATABASE_URI):
                create_database(TEST_DATABASE_URI)
            return self.test_db

    def is_connected(self):
        with self.app_context():
            return self.db.engine is not None

    def set_test_database(self) -> None:
        self.database_type = DatabaseType.test_database

    def set_production_database(self) -> None:
        self.database_type = DatabaseType.production_database

    def app_context(self) -> AppContext:
        if self.database_type == DatabaseType.production_database:
            return self.production_app.app_context()
        else:
            return self.test_app.app_context()

    def has_table(self, table_name: str):
        with self.app_context():
            engine = self.db.engine
            inspector = Inspector.from_engine(engine)
            return inspector.has_table(table_name)

    def create_database(self):
        if not self.database_exists():
            if self.database_type == DatabaseType.production_database:
                create_database(DATABASE_URI)
            else:
                create_database(TEST_DATABASE_URI)

    def database_exists(self) -> bool:
        if self.database_type == DatabaseType.production_database:
            return database_exists(DATABASE_URI)
        else:
            return database_exists(TEST_DATABASE_URI)

    def drop_database(self) -> None:
        if self.database_exists():
            if self.database_type == DatabaseType.production_database:
                drop_database(DATABASE_URI)
            else:
                drop_database(TEST_DATABASE_URI)

    def rollback(self) -> None:
        with self.app_context():
            self.db.session.rollback()

    def commit(self) -> None:
        with self.app_context():
            sqlalchemy.db.session.commit()

    def add_record(self, item) -> None:
        with self.app_context():
            sqlalchemy.db.session.add(item)
            sqlalchemy.db.session.commit()

    def add_records(self, items: list) -> None:
        with self.app_context():
            for item in items:
                sqlalchemy.db.session.add(item)
            sqlalchemy.db.session.commit()


sqlalchemy = Database()
