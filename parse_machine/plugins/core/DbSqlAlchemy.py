#!/usr/bin/env python

import logging
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from plugins.core.dbsettings import DATABASES


class DbSqlAlchemy(object):
    def __init__(self):
        self.engine = None
        self.connection = None
        self.cursor = None
        self._session = None
        self._sessionmaker = None

    def connect(self, settings=None):
        # if not settings:
        #     settings = DATABASES
        connection_name = 'default'
        config = DATABASES[connection_name]
        # assert 'mysql' in config['ENGINE']
        url = 'mysql+pymysql://{username}:{password}@{host}/{db}' \
            .format(username=config['USER'],
                    password=config['PASSWORD'],
                    host=config['HOST'],
                    db=config['NAME'],
                    port=config['PORT'])
        self.engine = sqlalchemy.create_engine(url)
        self.connection = self.engine.connect()
        self.cursor = self.connection
        assert self.connection

    def disconnect(self):
        if self.cursor is not None:
            self.connection.close()
            self.connection = None
            self.cursor = None

    @property
    def session(self):
        if self._session is None:
            self._sessionmaker = sessionmaker(bind=self.engine)
            self._session = self._sessionmaker()
            assert self._session
        return self._session

    def __del__(self):
        # Make sure the database connection is properly closed
        if self.connection:
            logging.info('Auto-terminating MySQL connection from __del__()')
            self.connection.close()


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s\t%(levelname)-10s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    logging.info('Trying database connect-disconnect to test connection.')
    db = DbSqlAlchemy()
    db.connect()
    db.disconnect()
    logging.info('All well.')


if __name__ == "__main__":
    main()
