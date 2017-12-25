from parse_machine.GmailParser import GmailParser
from bs4 import BeautifulSoup


class EbayParser(GmailParser):
    ID_VALUE_LOCATION = 1

    def __init__(self, specs, html_specs):
        super(EbayParser, self).__init__(specs)
        self.html_specs = html_specs

    def get_price(self, message):

        return '8.99'

    def extract_html(self, message):
        split_html = self.html_specs[
            (self.html_specs['method'] == 'split') &
            (self.html_specs['name'] == 'extract')].iloc[0]['html_value']
        return message['mime_html'].split(split_html)[1]
