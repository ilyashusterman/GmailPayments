import json

import pandas
from unipath import Path
from unittest import TestCase

from parse_machine.SteamParser import SteamParser


class TestSteamParser(TestCase):
    PARSER_SPEC = Path(Path(__file__).parent, 'steam_parser_specs.csv')
    HTML_SPEC = Path(Path(__file__).parent, 'html_parser_specs.csv')

    def setUp(self):
        parser_specs = pandas.read_csv(self.PARSER_SPEC, engine='python',
                                       encoding='utf-8')
        html_specs = pandas.read_csv(self.HTML_SPEC, engine='python',
                                     encoding='utf-8')
        self.parser = SteamParser(parser_specs, html_specs)
        self.message = self.open_json('{}_message.json'.format('steam'))

    def open_json(self, filename):
        with open(Path(Path(__file__).parent, filename)) as data_file:
            return json.load(data_file)

    def test_price_message(self):
        price = self.parser.get_price(message=self.message)
        self.assertEqual(price, '129.99')
