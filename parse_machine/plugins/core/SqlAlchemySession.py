from __future__ import absolute_import

from plugins.core.DbSqlAlchemy import DbSqlAlchemy


class SqlAlchemySession(object):
    _cached_session = None

    @classmethod
    def get_session(cls):
        if not cls._cached_session:
            cls._cached_session = SqlAlchemySession()
        return cls._cached_session

    def __init__(self):
        self.db = DbSqlAlchemy()
        self.db.connect()

    def __del__(self):
        self._cached_session = None
        self.db.disconnect()
