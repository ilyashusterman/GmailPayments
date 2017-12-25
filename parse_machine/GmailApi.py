from argparse import Namespace
import base64
import email
import httplib2
import os
import json

from apiclient import errors
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'
USER_ID = 'me'


class GmailApi(object):
    def __init__(self, authenticate=True):
        self.authenticate = authenticate
        self.email = None

    def get_credentials(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'gmail-python-quickstart.json')
        store = Storage(credential_path)
        credentials = store.get() if self.authenticate else None
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            flags = Namespace(auth_host_name='localhost',
                              auth_host_port=[8080, 8090],
                              logging_level='ERROR',
                              noauth_local_webserver=False)
            credentials = tools.run_flow(flow, store, flags)
        return credentials

    def get_email(self):
        service = self.get_service()
        response = service.users().getProfile(userId=USER_ID).execute()
        return response['emailAddress']

    @staticmethod
    def get_flags():
        try:
            import argparse
            flags = argparse.ArgumentParser(
                parents=[tools.argparser]).parse_args()
        except ImportError:
            flags = None
        return flags

    def get_messages(self, query):
        service = self.get_service()
        messages = self.get_messages_matching_query(service, user_id=USER_ID,
                                                    query=query)
        loaded_messages = []
        for message in messages:
            content = self.get_message(service, USER_ID, message['id'])
            # print(content['snippet'])
            loaded_messages.append(content)
        return loaded_messages

    def get_snippet_messages(self, query):
        return [message['snippet'] for message in self.get_messages(query)]

    def get_service(self):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)
        return service

    def get_message(self, service, user_id, msg_id):
        try:
            message = service.users().messages().get(userId=user_id,
                                                     id=msg_id).execute()
            message_raw = service.users().messages().get(userId=user_id,
                                                         id=msg_id,
                                                         format='raw').execute()
            msg_str = base64.urlsafe_b64decode(
                message_raw['raw'].encode('ASCII'))
            mime_html = email.message_from_string(msg_str.decode())
            mime_msg = email.message_from_string(message_raw['raw'])
            message.update({
                'raw': str(msg_str),
                'mime_html': str(mime_html),
                'mime_msg': str(mime_msg)
            })
            return message
        except errors.HttpError as e:
            print('An error occurred: %s' % e)
            raise e

    def get_messages_matching_query(self, service, user_id, query=''):
        try:
            response = service.users().messages().list(userId=user_id,
                                                       q=query).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = service.users().messages(). \
                    list(userId=user_id,
                         q=query,
                         pageToken=page_token).execute()
                messages.extend(response['messages'])

            return messages
        except errors.HttpError as e:
            print('An error occurred: %s' % e)
            raise e


if __name__ == '__main__':
    api = GmailApi(False)
    # print(api.get_messages(query='purchase')[0])
    with open('messages.json', 'w') as f:
        json.dump({'messages': api.get_messages(query='purchase')}, f)
        # api.email = api.get_email()
        # print(api.get_email())
