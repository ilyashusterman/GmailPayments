from copy import deepcopy


class GmailParser(object):
    TYPES = {
        'list': [],
        'str': ''
    }

    def __init__(self, specs):
        self.specs = specs

    def get_platform(self, message):
        return self.parse_message(message, 'platform')

    def get_title(self, message):
        return self.parse_message(message, 'title')

    def get_date(self, message):
        return self.parse_message(message, 'date')

    def get_reciever_email(self, message):
        return self.parse_message(message, 'email')

    def parse_message(self, message, spec_attribute):
        spec = self.specs[self.specs['attribute'] == spec_attribute].iloc[0]
        message_keys = spec['message_key'].split('-')
        message_key_values = self.get_message_key_values(message, message_keys)
        value_name = spec['message_name']
        return self.parse_value(value_name,
                                message_key_values,
                                value_type=spec['type'])

    def get_message_key_values(self, message, message_keys):
        value_message = deepcopy(message)
        for key in message_keys:
            value_message = value_message[key]
        return value_message

    def parse_value(self, value_name, message_key_values, value_type):
        filtered_values = None
        if isinstance(self.TYPES[value_type], list):
            filtered_values = [value for value in message_key_values
                               if value['name'] == value_name]
            if len(filtered_values) > 0:
                filtered_values = filtered_values[0]['value']
        elif isinstance(message_key_values, dict):
            filtered_values = message_key_values['value'] \
                if message_key_values['name'] == value_name else None
        elif isinstance(message_key_values, str):
            filtered_values = message_key_values
        return filtered_values
