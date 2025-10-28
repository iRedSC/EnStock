

from typing import Optional
from enstock.database import Database


class BaseModel:
    _database: Optional[Database]
    _create_table_statement: Optional[str] = None

    @classmethod
    def database(cls):
        assert cls._database is not None
        return cls._database

    @classmethod
    def create(cls):
        if not cls._create_table_statement:
            return
        cls.database().execute(cls._create_table_statement)