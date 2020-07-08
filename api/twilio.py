from twilio.rest import Client
import os


class Twilio:
    # ACCOUNT_SID = os.getenv("ACCOUNT_SID")
    # AUTH_TOKEN = os.getenv("AUTH_TOKEN")
    # client = Client(ACCOUNT_SID, AUTH_TOKEN)

    def send_message(self, receiver, message):
        # message = self.client.messages.create(,,

        print('a')
