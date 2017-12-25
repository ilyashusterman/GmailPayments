from unittest import TestCase

import pandas

from parse_machine.models.PaymentTable import PaymentTable


class TestPaymentTable(TestCase):
    def setUp(self):
        self.title = 'Thank you for your purchase'
        self.test_payment = pandas.DataFrame([{
            'platform_id': 1,
            'user_id': 1,
            'title': self.title,
            'price': 8.99,
            'date': '10.01.17 15:10:00'
        }])
        self.payment_table = PaymentTable()

    def test_insert_payment(self):
        self.payment_table.insert_data_frame(self.test_payment)
        self.payment_table.remove_payment(title=self.title)

    def test_insert_payment_with_user_and_platform(self):

        self.payment_table.insert_data_frame(self.test_payment)