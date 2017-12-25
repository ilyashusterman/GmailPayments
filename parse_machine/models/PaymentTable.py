from sqlalchemy import bindparam, delete, and_, func

from models.models import Payment
from plugins.core.TableBase import TableBase
from plugins.core.DbSqlAlchemy import DbSqlAlchemy
from plugins.core.SqlAlchemySession import SqlAlchemySession


class PaymentTable(TableBase):
    TABLE_NAME = 'payment'
    COLUMNS = ['id', 'title', 'price', 'date', 'user_id', 'platform_id']

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

    def remove_payment(self, title):
        sql_alchemy = SqlAlchemySession.get_session()
        sql_alchemy.db.session.query(func.count(Payment.id)) \
            .filter(Payment.title == title).delete()
        sql_alchemy.db.session.commit()