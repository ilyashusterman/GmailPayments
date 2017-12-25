import argparse
import logging
from unipath import Path
import pandas

from GmailApi import GmailApi
from GmailParser import GmailParser
from models.PaymentTable import PaymentTable


class PaymentParseMachine(object):
    QUERY = 'purchase'
    PARSER_SPEC = Path(Path(__file__).parent, 'steam_parser_specs.csv')

    def __init__(self, dry_run=None):
        self.message_spec = pandas.read_csv(self.PARSER_SPEC, engine='python',
                                            encoding='utf-8')
        self.dry_run = dry_run

    @classmethod
    def main(cls):
        parser = argparse.ArgumentParser()
        commands = parser.add_mutually_exclusive_group(required=True)
        commands.add_argument('--process-payment', action='store_true')
        parser.add_argument('--dry-run', action='store_true',
                            help='Parse the data but not effecting database')
        args = parser.parse_args()
        payment_machine = cls(args.dry_run)
        if args.apply_dynamic_margin:
            payment_machine.proccess_payments()
        elif args.insert:
            raise NotImplementedError()
        else:
            logging.info('Nothing to do.')

    def proccess_payments(self):
        gmail_api = GmailApi()
        messages = gmail_api.get_messages(query=self.QUERY)
        gmail_parser = GmailParser(self.message_spec)
        for message in messages:
            payment_spec = {
                'date': gmail_parser.get_date(message),
                'price': gmail_parser.get_platform(message),
                'user_platform': gmail_parser.get_platform(message),
                'user_email': gmail_parser.get_reciever_email(message),
                'title': gmail_parser.get_title(message),
            }
            if not self.dry_run:
                PaymentTable().persist_payment(payment_spec)
            logging.info('added payment record={}'.format(payment_spec))


if __name__ == '__main__':
    # Margin.activate()
    # exit(0)
    logging.basicConfig(level=logging.INFO)
    PaymentParseMachine.main()
