from arkdata.database.cursor import sqlalchemy, app
from sqlalchemy import Integer, Column
import json
from pathlib import Path


class Table:
    id = Column(Integer, primary_key=True, autoincrement=True)

    @classmethod
    def all(cls):
        return sqlalchemy.db.session.query(cls).all()

    @classmethod
    def find_by(cls, **kwargs):
        args = [cls.__dict__[param] == arg for param, arg in kwargs.items()]
        record = sqlalchemy.db.session.query(cls).filter(*args).first()
        cls.commit()
        return record

    @classmethod
    def find_all_by(cls, **kwargs):
        args = [cls.__dict__[param] == arg for param, arg in kwargs.items()]
        record = sqlalchemy.db.session.query(cls).filter(*args).all()
        cls.commit()
        return record

    @classmethod
    def columns(cls):
        return cls.metadata.tables[cls.__tablename__].columns.keys()

    @classmethod
    def first(cls):
        return sqlalchemy.db.session.query(cls).first()

    @classmethod
    def length(cls):
        return sqlalchemy.db.session.query(cls).count()

    @classmethod
    def bulk_insert(cls, values: list):
        bulk = []
        for items in values:
            item = cls(**items)
            sqlalchemy.db.session.add(item)
            bulk.append(item)
        cls.commit()
        return bulk

    @classmethod
    def drop_table(cls):
        cls.commit()
        inspector = sqlalchemy.db.inspect(sqlalchemy.db.engine)
        if inspector.has_table(cls.__tablename__):
            sqlalchemy.db.session.execute(f'DROP TABLE {cls.__tablename__}')

    @classmethod
    def create_table(cls):
        inspector = sqlalchemy.db.inspect(sqlalchemy.db.engine)
        if not inspector.has_table(cls.__tablename__):
            cls.__table__.create(sqlalchemy.db.session.bind, checkfirst=True)

    @classmethod
    def clear_table(cls):
        inspector = sqlalchemy.db.inspect(sqlalchemy.db.engine)
        if inspector.has_table(cls.__tablename__):
            sqlalchemy.db.session.execute(f'TRUNCATE TABLE {cls.__tablename__}')

    @classmethod
    def table_exists(cls):
        inspector = sqlalchemy.db.inspect(sqlalchemy.db.engine)
        return inspector.has_table(cls.__tablename__)

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
    def commit(cls):
        sqlalchemy.db.session.commit()

    @classmethod
    def group_by(cls):
        # TODO: add a group by
        # need execution to consoladate because
        # not all bots in the same server
        # e.g. group_by server_id
        pass

    def commit_initialization(self):
        sqlalchemy.db.session.add(self)
        self.commit()

    def delete(self):
        sqlalchemy.db.session.delete(self)

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
