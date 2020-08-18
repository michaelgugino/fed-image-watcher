class SaveMessage(object):
    """
    A fedora-messaging consumer that saves the message to a file.

    A single configuration key is used from fedora-messaging's
    "consumer_config" key, "path", which is where the consumer will save
    the messages::

        [consumer_config]
        path = "/tmp/fedora-messaging/messages.txt"
    """

    def __init__(self):
        print("starting up\n")

    def __call__(self, message):
        """
        Invoked when a message is received by the consumer.

        Args:
            message (fedora_messaging.api.Message): The message from AMQP.
        """
        print("got message")
        print(message)
