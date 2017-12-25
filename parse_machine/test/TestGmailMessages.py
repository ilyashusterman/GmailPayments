import json
from unittest import TestCase
from unipath import Path

from parse_machine.GmailApi import GmailApi


class TestGmailApi(TestCase):
    def setUp(self):
        with open(Path(Path(__file__).parent, 'messages.json')) as data_file:
            self.loaded_messages = json.load(data_file)
        self.gmail = GmailApi(authenticate=False)

    def test_google_total_messages(self):
        messages = self.gmail.get_snippet_messages(query='purchase')
        self.assertEqual(len(messages), 9, msg=messages)
        self.assertEqual(len(self.loaded_messages['messages']), 7, msg=messages)
        # self.assertEqual(len(messages), len(self.loaded_messages['messages']))

