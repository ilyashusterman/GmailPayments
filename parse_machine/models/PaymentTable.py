import pandas
from sqlalchemy import func

from parse_machine.models.PlatformTable import PlatformTable
from parse_machine.models.UserTable import UserTable
from parse_machine.models.models import Payment
from parse_machine.plugins.core.TableBase import TableBase
from parse_machine.plugins.core.DbSqlAlchemy import DbSqlAlchemy
from parse_machine.plugins.core.SqlAlchemySession import SqlAlchemySession


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

    def persist_payment(self, payment_spec):
        # todo user save

        # todo check if not exist then add
        UserTable().insert_data_frame(pandas.DataFrame[{
            'email': payment_spec['user_email']
        }])
        # todo check if not exist then add
        PlatformTable().insert_data_frame(pandas.DataFrame[{
            'name': payment_spec['user_platform']
        }])
        self.insert_data_frame(pandas.DataFrame[{
            # 'user_id': UserTable().get_user(email=payment_spec['user_email']),
            # 'platform_id': PlatformTable().get_platform(
            #     name=payment_spec['user_platform']),
            'price': payment_spec['price'],
            'title': payment_spec['title'],
            'date': payment_spec['date']
        }])
