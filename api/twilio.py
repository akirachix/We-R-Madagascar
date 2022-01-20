from twilio.rest import Client
import os
from decouple import config


class Twilio:
    ACCOUNT_SID = config("ACCOUNT_SID")
    AUTH_TOKEN = config("AUTH_TOKEN")
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    def send_report_reply(self,receiver,reply,category,complain):
        message = """'{}' is a reply for the complaint you reported to us under the category '{}' stating '{}'
        """.format(reply,category,complain)

        self.send_message(receiver,message)

    def send_message(self, receiver, message):
        if receiver:
            message = self.client.messages.create(  # message = self.client.messages.create(,,
                from_="whatsapp:+9779818817052",
                body=message,
                to=receiver
            )
            print(message.sid)
