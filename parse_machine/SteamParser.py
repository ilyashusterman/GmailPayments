from parse_machine.GmailParser import GmailParser
from bs4 import BeautifulSoup


class SteamParser(GmailParser):
    ID_VALUE_LOCATION = 1

    def __init__(self, specs, html_specs):
        super(SteamParser, self).__init__(specs)
        self.html_specs = html_specs

    def get_price(self, message):
        html = self.extract_html(message)
        soup = BeautifulSoup(html, 'lxml')
        price_specs = self.html_specs[(self.html_specs['method'] == 'get') &
                                      (self.html_specs['name'] == 'price')]
        value = soup.find(price_specs['element_type'])
        print(value)
        return '129.991'

    def extract_html(self, message):
        split_html = self.html_specs[
            (self.html_specs['method'] == 'split') &
            (self.html_specs['name'] == 'extract')].iloc[0]['html_value']
        return message['mime_html'].split(split_html)[1]
