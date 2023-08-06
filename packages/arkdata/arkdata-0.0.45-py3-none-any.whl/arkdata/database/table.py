from arkdata.database.cursor import sqlalchemy
from sqlalchemy import Integer, Column
from sqlalchemy.sql import text
import json
from pathlib import Path


class Table:
    id = Column(Integer, primary_key=True, autoincrement=True)

    @classmethod
    def all(cls):
        with sqlalchemy.app_context():
            return sqlalchemy.db.session.query(cls).all()

    @classmethod
    def find_by(cls, **kwargs):
        args = [cls.__dict__[param] == arg for param, arg in kwargs.items()]
        with sqlalchemy.app_context():
            record = sqlalchemy.db.session.query(cls).filter(*args).first()
            return record

    @classmethod
    def find_all_by(cls, **kwargs):
        args = [cls.__dict__[param] == arg for param, arg in kwargs.items()]
        with sqlalchemy.app_context():
            record = sqlalchemy.db.session.query(cls).filter(*args).all()
            return record

    @classmethod
    def columns(cls):
        return cls.metadata.tables[cls.__tablename__].columns.keys()

    @classmethod
    def first(cls):
        with sqlalchemy.app_context():
            return sqlalchemy.db.session.query(cls).first()

    @classmethod
    def length(cls):
        with sqlalchemy.app_context():
            return sqlalchemy.db.session.query(cls).count()

    @classmethod
    def bulk_insert(cls, values: list):
        bulk = [cls(**item) for item in values]
        sqlalchemy.add_records(bulk)
        return bulk

    @classmethod
    def bulk_delete(cls, items: list):
        with sqlalchemy.app_context():
            for item in items:
                sqlalchemy.db.session.delete(item)
            sqlalchemy.db.session.commit()

    @classmethod
    def drop_table(cls):
        if cls.table_exists():
            with sqlalchemy.app_context():
                cls.__table__.drop(sqlalchemy.db.engine)

    @classmethod
    def create_table(cls):
        if not cls.table_exists():
            with sqlalchemy.app_context():
                cls.__table__.create(sqlalchemy.db.engine, checkfirst=True)

    @classmethod
    def clear_table(cls):
        if cls.table_exists():
            cls.drop_table()
            cls.create_table()

    @classmethod
    def table_exists(cls):
        return sqlalchemy.has_table(cls.__tablename__)

    @classmethod
    def _seed_table(cls, path: Path or str):
        if not cls.table_exists():
            cls.create_table()
        file = Path(path)
        if not file.exists():
            raise FileNotFoundError(f'Could not find: {str(file)}')
        with open(file, 'r') as r:
            values = json.load(r)
            assert isinstance(values, list)
            cls.bulk_insert(values)

    @classmethod
    def seed_table(cls):
        ...

    @classmethod
    def commit(cls) -> None:
        sqlalchemy.commit()

    @classmethod
    def group_by(cls):
        # TODO: add a group by
        # need execution to consoladate because
        # not all bots in the same server
        # e.g. group_by server_id
        pass

    def commit_initialization(self):
        sqlalchemy.add_record(self)

    def delete(self):
        with sqlalchemy.app_context():
            sqlalchemy.db.session.delete(self)
            sqlalchemy.db.session.commit()

    def keys(self) -> list:
        return self.columns()

    def values(self) -> list:
        return [getattr(self, key) for key in self.keys()]

    def items(self):
        for key in self.columns():
            yield key, getattr(self, key)

    def __getitem__(self, key):
        assert key in self.keys(), f"'{key}' must be of {self.columns()}"
        return getattr(self, key)

    def __call__(self, *args, **kwargs):
        difference = set(kwargs.keys()).difference(set(self.columns()))
        error_message = f"{difference} are not Columns of '{self.__tablename__}': {self.columns()}"
        assert len(difference) == 0, error_message
        for key, val in kwargs.items():
            setattr(self, key, val)
        return self

    def __str__(self):
        table_name = self.__tablename__.title().replace("_", "")
        items = []
        for k, v in dict(self).items():
            items.append(f"\033[34m{k}\033[90m=\033[0m{repr(v)}\033[0m")
        args = ', '.join(items)
        return f'<\033[96m{table_name}\033[0m({args})>\033[0m'

    def __repr__(self):
        table_name = self.__tablename__.title().replace("_", "")
        items = []
        for k, v in dict(self).items():
            items.append(f"{k}={repr(v)}")
        args = ', '.join(items)
        return f'{table_name}({args})'
