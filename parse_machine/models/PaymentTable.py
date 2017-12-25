# from sqlalchemy import bindparam, update, and_

from models.models import Payment
from plugins.core.TableBase import TableBase
from plugins.core.DbSqlAlchemy import DbSqlAlchemy
# from plugins.core.SqlAlchemySession import SqlAlchemySession


class PaymentTable(TableBase):
    TABLE_NAME = 'payment'
    COLUMNS = ['id', 'title', 'price', 'date']

    COLUMNS_NOT_NULL = []
    DATE_COLUMNS = [0]

    def __init__(self):
        super(PaymentTable, self).__init__(self.TABLE_NAME,
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

