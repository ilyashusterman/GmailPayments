from sqlalchemy import bindparam, delete, and_, func

from models.models import Payment
from plugins.core.TableBase import TableBase
from plugins.core.DbSqlAlchemy import DbSqlAlchemy
from plugins.core.SqlAlchemySession import SqlAlchemySession


class UserTable(TableBase):
    TABLE_NAME = 'user'
    COLUMNS = ['id', 'email']

    COLUMNS_NOT_NULL = []
    DATE_COLUMNS = [0]

    def __init__(self):
        super(UserTable, self).__init__(self.TABLE_NAME,
                                        self.COLUMNS,
                                        self.COLUMNS_NOT_NULL,
                                        ['date'],
                                        date_parser=
                                        TableBase.make_date_parser
                                        ('%Y-%m-%d'))

    @staticmethod
    def test():
        db = DbSqlAlchemy()
        db.connect()
        selected = db.session.query(Payment)
        for row in selected:
            print(row.market_name)
        db.disconnect()
