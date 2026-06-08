import json
from azure.servicebus import ServiceBusClient, ServiceBusMessage

from utilities.allure_report import AllureReport
from utilities.config_reader import ConfigReader


class AzureServiceBusHelper:

    def __init__(self, connection_string):
        self.connection_string = connection_string

    def _peek_all_messages(self, topic_name, subscription_name, batch_size=50):

        client = ServiceBusClient.from_connection_string(
            self.connection_string
        )

        all_messages = []
        last_sequence_number = 0

        with client:

            receiver = client.get_subscription_receiver(
                topic_name=topic_name,
                subscription_name=subscription_name
            )

            with receiver:

                while True:
                    print("ASB topic connection established and peeking messages successfully","ASB Topic: "+topic_name+" Subscription: "+subscription_name)
                    #AllureReport.attach_text("ASB topic connection established and peeking messages successfully", "ASB Topic: "+topic_name+" Subscription: "+subscription_name)

                    batch = receiver.peek_messages(
                        max_message_count=batch_size,
                        sequence_number=last_sequence_number
                    )

                    if not batch:
                        break

                    all_messages.extend(batch)

                    last_sequence_number = (
                        batch[-1].sequence_number + 1
                    )

        return all_messages

    def _get_last_message(self, topic_name, subscription_name):

        messages = self._peek_all_messages(
            topic_name,
            subscription_name
        )

        if not messages:
            return None

        return messages[-1]

    def get_last_message_json(self, topic_name, subscription_name):

        last_message = self._get_last_message(
            topic_name,
            subscription_name
        )
        AllureReport.attach_text("ASB topic connection established and peeking messages successfully", "ASB Topic: "+topic_name+" Subscription: "+subscription_name)

        if not last_message:
            return None

        body = b"".join(last_message.body).decode("utf-8")

        return json.loads(body)

    def get_last_message_id(self, topic_name, subscription_name):

        message_json = self.get_last_message_json(
            topic_name,
            subscription_name
        )

        if not message_json:
            return None
        AllureReport.attach_text(message_json, "ASB Topic fetch last Message body")
        return message_json.get("id")

    # Send message to ASB consume topic
    # ====================================================
    # SEND MESSAGE TO TOPIC
    # ====================================================

    def send_message_to_topic(
            self,
            payload_data,
            topic_name
    ):

        client = ServiceBusClient.from_connection_string(
            self.connection_string
        )

        sender = client.get_topic_sender(
            topic_name=topic_name
        )

        message = ServiceBusMessage(
            body=payload_data,
            content_type="application/json"
        )

        with client:
            with sender:
                print(
                    f"Publishing message "
                    f"to ASB Topic '{topic_name}'..."
                )

                sender.send_messages(message)

                print("Message successfully enqueued!")

                AllureReport.attach_text(
                    payload_data,
                    "ASB Payload message sent to topic: "+topic_name
                )