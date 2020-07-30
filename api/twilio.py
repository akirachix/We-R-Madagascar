from twilio.rest import Client
import os


class Twilio:
    ACCOUNT_SID = os.getenv("ACCOUNT_SID")
    AUTH_TOKEN = os.getenv("AUTH_TOKEN")
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    def send_message(self, receiver, message):
        message = self.client.messages.create(  # message = self.client.messages.create(,,
            from_="whatsapp:+9779818817052",
            body=message,
            to=receiver
        )
        print(message.sid)
