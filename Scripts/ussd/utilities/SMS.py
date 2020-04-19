from __future__ import print_function

import africastalking

class SMS:
    def __init__(self):
        self.username = "sandbox"
        self.api_key = "d14da11eaa567f7055f712b2336bf97bb59051d22f1fd83be042adda56d07584"
        # Initialize the SDK
        africastalking.initialize(self.username, self.api_key)
        # Get the SMS service
        self.sms = africastalking.SMS

    def send_sms_sync(self, recipients, message):
        sender="86387"
        try:
            # That’s it, hit send and we’ll take care of the rest
            response = self.sms.send(message, recipients,sender)
            print(response)
        except Exception as e:
            print ('Encountered an error while sending: %s' % str(e))