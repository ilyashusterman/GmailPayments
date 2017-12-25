from unittest import TestCase, skip

import pandas

# from parse_machine.models.PaymentTable import PaymentTable


class TestPaymentTable(TestCase):
    def setUp(self):
        self.title = 'Steam Thank you for your purchase'
        self.test_payment = pandas.DataFrame([{
            'platform_id': 1,
            'user_id': 1,
            'title': self.title,
            'price': 8.99,
            'date': '10.01.17 15:10:00'
        }])
        # self.payment_table = PaymentTable()
        self.payment_table = None

    @skip
    def test_insert_payment(self):
        self.payment_table.insert_data_frame(self.test_payment)
        self.payment_table.remove_payment(title=self.title)

    @skip
    def test_insert_payment_with_user_and_platform(self):
        payment_spec_persist = {
            'user_email': 'test@gmail.com',
            'payment_title': self.title,
            'payment_platform': 'Steam',
            'price': 129.99,
            'date': '10.01.17 15:10:00'
        }