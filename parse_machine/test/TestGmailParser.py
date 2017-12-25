import json

import pandas
from unipath import Path
from unittest import TestCase

from parse_machine.GmailParser import GmailParser


class TestGmailParser(TestCase):
    STEAM_PARSER_SPEC = Path(Path(__file__).parent, 'steam_parser_specs.csv')
    EBAY_PARSER_SPEC = Path(Path(__file__).parent, 'ebay_parser_specs.csv')

    def setUp(self):
        parser_specs = pandas.read_csv(self.STEAM_PARSER_SPEC, engine='python',
                                       encoding='utf-8')
        self.parser = GmailParser(parser_specs)
        self.message = self.open_json('{}_message.json'.format('steam'))

    def test_parse_platform_steam(self):
        self.check_message_steam_platform('steam', 'Steam')

    def test_title_message(self):
        title = self.parser.get_title(self.message)
        self.assertEqual(title, 'Thank you for your Steam purchase!')

    def test_title_date(self):
        date = self.parser.get_date(self.message)
        self.assertEqual(date, 'Sat, 02 Dec 2017 01:56:31 -0800')

    def test_parse_message_reciever(self):
        email_found = self.parser.get_reciever_email(message=self.message)
        self.assertEqual('shusterilyaman@gmail.com', email_found)

    def check_message_steam_platform(self, platform, check_value):
        message = self.open_json('{}_message.json'.format(platform))
        platform_found = self.parser.get_platform(message=message)
        self.assertEqual(check_value, platform_found)

    def test_message_ebay_title(self):
        parser_specs = pandas.read_csv(self.EBAY_PARSER_SPEC, engine='python',
                                       encoding='utf-8')
        parser = GmailParser(parser_specs)
        message = self.open_json('{}_message.json'.format('ebay'))
        title = parser.get_title(message)
        self.assertEqual(title,
                         'Fw: ✅ ORDER CONFIRMED: LED Adjustable Stand...',
                         msg=title)
    #
    # def test_message_ebay_platform(self):
    #     parser_specs = pandas.read_csv(self.EBAY_PARSER_SPEC, engine='python',
    #                                    encoding='utf-8')
    #     parser = GmailParser(parser_specs)
    #     message = self.open_json('{}_message.json'.format('ebay'))
    #     title = parser.get_title(message)
    #     self.assertEqual(title,
    #                      'Fw: ✅ ORDER CONFIRMED: LED Adjustable Stand...',
    #                      msg=title)

    def open_json(self, filename):
        with open(Path(Path(__file__).parent, filename)) as data_file:
            return json.load(data_file)
